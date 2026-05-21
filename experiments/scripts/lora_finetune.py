"""
LoRA Fine-tuning Script for Qwen2.5-7B-Instruct
Optimized for RTX 3090 (24GB VRAM).
"""

import json
import os
import sys
import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)
from peft import LoraConfig, get_peft_model, TaskType

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
import config


def load_training_data(filepath: str) -> Dataset:
    """Load JSONL training data."""
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line.strip())
            data.append(item)
    print(f"Loaded {len(data)} training examples")
    return Dataset.from_list(data)


def preprocess(example, tokenizer, max_length=1024):
    """Convert messages to model input format."""
    messages = example["messages"]
    # Apply chat template
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False
    )
    # Tokenize
    encodings = tokenizer(text, truncation=True, max_length=max_length, padding=False)
    encodings["labels"] = encodings["input_ids"].copy()
    return encodings


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-d", default="experiments/data/training_data.jsonl")
    parser.add_argument("--output", "-o", default="experiments/models/qwen2.5-7b-lora")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--lora-rank", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=1024)
    args = parser.parse_args()

    # Load model
    print(f"Loading model from {config.LLM_MODEL_PATH}...")
    tokenizer = AutoTokenizer.from_pretrained(
        config.LLM_MODEL_PATH, trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        config.LLM_MODEL_PATH,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.enable_input_require_grads()

    # LoRA config
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=args.lora_rank,
        lora_alpha=args.lora_rank * 2,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load and preprocess data
    dataset = load_training_data(args.data)
    tokenized_dataset = dataset.map(
        lambda x: preprocess(x, tokenizer, args.max_length),
        remove_columns=dataset.column_names,
        num_proc=1,
    )

    # Split train/eval (90/10)
    split = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = split["train"]
    eval_dataset = split["test"]
    print(f"Train: {len(train_dataset)}, Eval: {len(eval_dataset)}")

    # Training arguments
    os.makedirs(args.output, exist_ok=True)
    training_args = TrainingArguments(
        output_dir=args.output,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        weight_decay=0.01,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=50,
        save_strategy="steps",
        save_steps=50,
        save_total_limit=3,
        fp16=True,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        report_to="none",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
    )

    # Data collator
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        padding=True,
        max_length=args.max_length,
    )

    # Train
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
    )

    print("Starting LoRA fine-tuning...")
    trainer.train()

    # Save final model
    final_path = os.path.join(args.output, "final")
    model.save_pretrained(final_path)
    tokenizer.save_pretrained(final_path)
    print(f"Model saved to {final_path}")

    # Print training summary
    train_loss = trainer.state.log_history[-1].get("train_loss", "N/A")
    print(f"Final train loss: {train_loss}")
    print("Done!")


if __name__ == "__main__":
    main()
