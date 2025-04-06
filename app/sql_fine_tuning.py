from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, EarlyStoppingCallback
import torch

# Set device to CPU (avoid GPU memory issues)
device = torch.device("cpu")

# Load the dataset
dataset = load_from_disk("/data/hf_sql_dataset")

# Load the pre-trained SQL Generation Model and tokenizer
sql_model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(sql_model_name)
tokenizer.pad_token = tokenizer.eos_token # Pre-set pad_token


# Define the model to fine-tune
#sql_model = AutoModelForSeq2SeqLM.from_pretrained(sql_model_name, torch_dtype=torch.float16).to(device)
sql_model = AutoModelForSeq2SeqLM.from_pretrained(sql_model_name).to(device)

# Define tokenization function
def tokenize_function(examples):
    #print(f"DEBUG: First input = {examples['input'][0]}")
    #print(f"DEBUG: First target = {examples['output'][0]}")

    #inputs = [f"Schema: {example['input']}\nQuestion: {example['instruction']}" for example in examples["input"]]
    #inputs = [f"{schema}" for schema in examples["input"]]
    inputs = examples["input"]
    targets = examples["output"]

    model_inputs = tokenizer(inputs, max_length=256, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=64, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]

    # Debug statements
    #print(f"Tokenized inputs: {model_inputs}")
    #print(f"Tokenized labels: {labels}")

    return model_inputs

# Tokenize the dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=2,
    num_train_epochs=6,
    weight_decay=0.001,
    logging_dir="./logs",
    logging_steps=5,
    #save_steps=100,
    save_total_limit=2,
    fp16=False,
    gradient_accumulation_steps=6,
    max_grad_norm=0.2, # Gradient clipping
    warmup_ratio=0.1,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    #warmup_steps=10,
)

# Define the trainer
trainer = Seq2SeqTrainer(
    model=sql_model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    #tokenizer=tokenizer,
    processing_class=tokenizer,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
)

# Start the fine-tuning process
try:
    trainer.train()
except Exception as e:
    print(f"Training failed: {e}")

# Save the fine-tuned model
sql_model.save_pretrained("/data/finetuned_sql_model")
tokenizer.save_pretrained("/data/finetuned_sql_model")