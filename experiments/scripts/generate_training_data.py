"""
Generate LoRA fine-tuning training data.
Uses the existing CodeTutor-ITS system to generate high-quality tutoring responses.
"""

import json
import os
import sys
import time
import httpx
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config

API_BASE_URL = "http://localhost:8000"

# Extended question bank: 200+ questions across 10 topics
QUESTION_BANK = {
    "python_basics": [
        "What is a variable in Python?",
        "Explain the difference between local and global variables.",
        "What are Python's built-in data types?",
        "How does type casting work in Python?",
        "What is the difference between `is` and `==` in Python?",
        "Explain string formatting in Python (f-strings, format, %).",
        "What are escape characters in Python strings?",
        "How do you handle multi-line strings in Python?",
        "What is the difference between `remove`, `pop`, and `del` for lists?",
        "Explain tuple unpacking in Python.",
        "What are augmented assignment operators (+=, -=, etc.)?",
        "How does the `in` keyword work in Python?",
        "What is the difference between `sort()` and `sorted()`?",
        "Explain the `range()` function and its parameters.",
        "What are f-strings and how do they work?",
        "How do you merge two dictionaries in Python?",
        "What is the `zip()` function used for?",
        "Explain the `enumerate()` function.",
        "What is the difference between `append()` and `extend()`?",
        "How do you check if a key exists in a dictionary?",
    ],
    "control_flow": [
        "What is the difference between for loop and while loop?",
        "How does the `break` statement work?",
        "Explain the `continue` statement with an example.",
        "What is the `else` clause in a loop?",
        "How do you use nested loops effectively?",
        "Explain match-case (structural pattern matching) in Python 3.10+.",
        "What is a ternary operator in Python?",
        "How does the `pass` statement work?",
        "Explain the `assert` statement and its use cases.",
        "What are short-circuit operators (and, or)?",
        "How do you implement a do-while loop in Python?",
        "What is the walrus operator (:=)?",
        "How does exception handling work with try-except-else-finally?",
        "What is the difference between `raise` and `assert`?",
        "How do you create custom exceptions?",
    ],
    "functions": [
        "What is a function in Python? How do you define one?",
        "Explain default parameters and keyword arguments.",
        "What are *args and **kwargs?",
        "What is a lambda function? When should you use it?",
        "Explain closures in Python.",
        "What are decorators? Give an example.",
        "What is recursion? Give an example.",
        "Explain the difference between mutable and immutable default arguments.",
        "What is a generator function? How does `yield` work?",
        "What are higher-order functions?",
        "Explain the `map()`, `filter()`, and `reduce()` functions.",
        "What is function overloading in Python?",
        "How do you type-hint function parameters and return values?",
        "What is the `functools.wraps` decorator used for?",
        "Explain partial functions using `functools.partial`.",
    ],
    "data_structures": [
        "Explain the difference between lists and tuples.",
        "What is a dictionary in Python?",
        "How do sets work in Python?",
        "What is a stack and how do you implement it?",
        "What is a queue and how do you implement it?",
        "Explain linked lists and their Python implementation.",
        "What is a binary tree? How do you traverse it?",
        "Explain the difference between BFS and DFS.",
        "What is a hash table? How does Python's dict use it?",
        "What is a heap? How do you use `heapq` in Python?",
        "Explain graph representations (adjacency list vs matrix).",
        "What is a deque and when should you use it?",
        "How do you implement a binary search tree?",
        "What are the time complexities of common list operations?",
        "Explain the difference between a tuple and a named tuple.",
    ],
    "algorithms": [
        "Explain the binary search algorithm.",
        "What is bubble sort? What is its time complexity?",
        "Explain the merge sort algorithm.",
        "What is quicksort? How does it work?",
        "Explain time complexity and Big-O notation.",
        "What is a greedy algorithm? Give an example.",
        "Explain dynamic programming with an example.",
        "What is the two-pointer technique?",
        "Explain the sliding window technique.",
        "What is backtracking? Give an example.",
        "Explain the divide and conquer paradigm.",
        "What is memoization? How does it differ from tabulation?",
        "How do you find the longest common subsequence?",
        "Explain Dijkstra's shortest path algorithm.",
        "What is the knapsack problem? How do you solve it?",
    ],
    "oop": [
        "What is encapsulation in OOP?",
        "Explain inheritance in Python.",
        "What is polymorphism? Give an example.",
        "What are dunder (magic) methods?",
        "Explain the difference between class and instance variables.",
        "What is the `super()` function used for?",
        "How do abstract classes work in Python?",
        "What is multiple inheritance? How does MRO work?",
        "Explain the @property decorator.",
        "What are dataclasses in Python?",
        "What is the difference between `__str__` and `__repr__`?",
        "How does `__slots__` work and why use it?",
        "Explain the factory design pattern in Python.",
        "What is composition vs inheritance?",
        "How do you implement operator overloading?",
    ],
    "modules_packages": [
        "How do you import modules in Python?",
        "What is the difference between `import` and `from...import`?",
        "Explain the `__init__.py` file.",
        "What is `__name__` and `__main__`?",
        "How do you create and install a Python package?",
        "What is a virtual environment? Why use one?",
        "Explain the `sys.path` and module search order.",
        "What are relative imports in Python?",
        "How does `pip` work? What is `requirements.txt`?",
        "What is the difference between a module and a package?",
    ],
    "file_io": [
        "How do you read and write files in Python?",
        "Explain the `with` statement for file handling.",
        "What is the difference between text and binary mode?",
        "How do you read a CSV file in Python?",
        "How do you work with JSON files in Python?",
        "Explain file modes (r, w, a, r+, etc.).",
        "How do you handle file paths across operating systems?",
        "What is the `pathlib` module?",
        "How do you read a large file line by line efficiently?",
        "How do you work with Excel files in Python?",
    ],
    "error_handling": [
        "How do you handle exceptions in Python?",
        "What is the difference between SyntaxError and Exception?",
        "Explain the try-except-else-finally pattern.",
        "How do you create custom exceptions?",
        "What is exception chaining?",
        "How do you log exceptions properly?",
        "What is the `warnings` module?",
        "How do you handle multiple exceptions?",
        "What is the `raise` statement?",
        "Explain the context manager protocol for error handling.",
    ],
    "advanced_python": [
        "What are list comprehensions?",
        "Explain dictionary and set comprehensions.",
        "What is a generator expression?",
        "How does garbage collection work in Python?",
        "What is the GIL (Global Interpreter Lock)?",
        "Explain threading vs multiprocessing in Python.",
        "What are coroutines and async/await?",
        "How does Python's memory management work?",
        "What is metaclass programming?",
        "Explain descriptors in Python.",
        "What is monkey patching?",
        "How do you profile Python code?",
        "What are contextlib utilities?",
        "Explain the itertools module.",
        "What is type checking with mypy?",
    ],
    "web_basics": [
        "What is HTTP? Explain GET and POST methods.",
        "What is a REST API?",
        "How do you make HTTP requests in Python?",
        "What is Flask? How do you create a basic web app?",
        "What is FastAPI? How does it differ from Flask?",
        "Explain the concept of middleware.",
        "What are HTTP status codes?",
        "How does authentication work in web applications?",
        "What is CORS and why does it matter?",
        "What is JSON and how is it used in web development?",
    ],
    "database": [
        "What is SQL? What are the basic commands?",
        "Explain the difference between SQL and NoSQL databases.",
        "What is SQLAlchemy and how does it work?",
        "How do you connect to a SQLite database in Python?",
        "What is an ORM? What are its advantages?",
        "Explain database normalization.",
        "What are SQL joins? Explain different types.",
        "How do you prevent SQL injection?",
        "What is a database migration?",
        "Explain ACID properties of databases.",
    ],
    "testing": [
        "What is unit testing? How do you write tests in Python?",
        "Explain the `unittest` module.",
        "What is pytest? How does it differ from unittest?",
        "What are test fixtures?",
        "How do you mock dependencies in tests?",
        "What is test-driven development (TDD)?",
        "How do you measure code coverage?",
        "What are integration tests vs unit tests?",
        "How do you test API endpoints?",
        "What is parametrized testing?",
    ],
    "version_control": [
        "What is Git? Explain basic Git commands.",
        "What is the difference between git merge and git rebase?",
        "How do you resolve merge conflicts?",
        "What is a Git branch? How do you manage branches?",
        "Explain git stash and its use cases.",
        "What is a pull request?",
        "How do you undo a commit in Git?",
        "What is .gitignore and how does it work?",
        "Explain the difference between git pull and git fetch.",
        "What are Git hooks?",
    ],
}


def generate_question_variations(base_questions: dict, target_count: int = 250) -> list:
    """Generate question variations to reach target count."""
    all_questions = []

    for topic, questions in base_questions.items():
        for q in questions:
            all_questions.append({"topic": topic, "question": q})

    # If we need more, create variations
    variations = [
        "Can you explain {topic} in Python with a simple example?",
        "What are the best practices for {topic} in Python?",
        "How would you explain {topic} to a beginner?",
        "What are common mistakes when working with {topic} in Python?",
        "Compare different approaches to {topic} in Python.",
    ]

    topic_names = {
        "python_basics": "variables and data types",
        "control_flow": "loops and conditionals",
        "functions": "function definition and usage",
        "data_structures": "data structures",
        "algorithms": "algorithm design",
        "oop": "object-oriented programming",
        "modules_packages": "module management",
        "file_io": "file operations",
        "error_handling": "error handling",
        "advanced_python": "advanced Python features",
        "web_basics": "web development",
        "database": "database operations",
        "testing": "code testing",
        "version_control": "version control",
    }

    while len(all_questions) < target_count:
        topic = random.choice(list(topic_names.keys()))
        template = random.choice(variations)
        q = template.format(topic=topic_names[topic])
        all_questions.append({"topic": topic, "question": q})

    random.shuffle(all_questions)
    return all_questions[:target_count]


def query_tutor(question: str, session_id: str) -> str:
    """Query the tutoring system."""
    try:
        with httpx.Client(timeout=180.0) as client:
            response = client.post(
                f"{API_BASE_URL}/api/tutor/chat",
                json={
                    "message": question,
                    "session_id": session_id,
                    "mode": "tutor",
                    "programming_language": "python",
                },
            )
            response.raise_for_status()
            return response.json().get("response", "")
    except Exception as e:
        print(f"  Error: {e}")
        return ""


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", "-n", type=int, default=250, help="Number of training examples")
    parser.add_argument("--output", "-o", default="experiments/data/training_data.jsonl")
    args = parser.parse_args()

    print(f"Generating {args.count} training examples...")
    questions = generate_question_variations(QUESTION_BANK, args.count)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    success = 0
    with open(args.output, "w", encoding="utf-8") as f:
        for i, item in enumerate(questions):
            q = item["question"]
            topic = item["topic"]
            print(f"[{i+1}/{len(questions)}] [{topic}] {q[:60]}...")

            response = query_tutor(q, session_id=f"train_{topic}_{i}")

            if response and len(response) > 50:
                # Format as instruction-following for LoRA training
                training_example = {
                    "messages": [
                        {"role": "system", "content": config.SYSTEM_PROMPTS["tutor"]},
                        {"role": "user", "content": q},
                        {"role": "assistant", "content": response},
                    ]
                }
                f.write(json.dumps(training_example, ensure_ascii=False) + "\n")
                success += 1
                print(f"  OK ({len(response)} chars)")
            else:
                print(f"  SKIPPED (empty or too short)")

            # Small delay to not overwhelm the backend
            time.sleep(1)

    print(f"\nDone! {success}/{len(questions)} examples saved to {args.output}")


if __name__ == "__main__":
    main()
