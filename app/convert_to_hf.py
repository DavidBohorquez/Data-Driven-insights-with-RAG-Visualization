import json
from datasets import Dataset, DatasetDict

# Load the JSON dataset
with open("/data/sql_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert the dataset inot a Hugging Face compatible format
hf_dataset = Dataset.from_list(data)

# Split the dataset into train and test sets
dataset_dict = DatasetDict({
    "train": hf_dataset.shuffle(seed=42).select(range(int(0.7*len(hf_dataset)))),
    "test": hf_dataset.shuffle(seed=42).select(range(int(0.7*len(hf_dataset)), len(hf_dataset)))
})

# Savie dataset to Hugging Face format
dataset_dict.save_to_disk("/data/hf_sql_dataset")

print("Hugging Face dataset saved successfully!")