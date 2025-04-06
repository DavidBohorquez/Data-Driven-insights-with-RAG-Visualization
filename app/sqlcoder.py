import requests
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, GenerationConfig
import torch
import sqlite3
import re
import matplotlib.pyplot as plt
from datasets import load_from_disk
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Set device to CPU (avoid GPU memory issues)
device = torch.device("cpu")

# Load the fine-tuned model and tokenizer
sql_model_name = "tscholak/3vnuv1vf" # "/data/finetuned_sql_model"
tokenizer = AutoTokenizer.from_pretrained(sql_model_name)
tokenizer.pad_token = tokenizer.eos_token
sql_model = AutoModelForSeq2SeqLM.from_pretrained(sql_model_name).to(device)
sql_model.config.pad_token_id = sql_model.config.eos_token_id

# Response Generation Model
response_model_name = "google/flan-t5-large"
response_tokenizer = AutoTokenizer.from_pretrained(response_model_name)
response_tokenizer.pad_token = response_tokenizer.eos_token
response_model = AutoModelForSeq2SeqLM.from_pretrained(response_model_name).to(device)
response_model.config.pad_token_id = response_model.config.eos_token_id

# Define generation configurations
sql_gen_config = GenerationConfig(
    max_new_tokens=128,
    num_beams=2,
    pad_token_id=tokenizer.eos_token_id,
    eos_token_id=tokenizer.eos_token_id,
    decoder_start_token_id=0
)

response_gen_config = GenerationConfig(
    max_new_tokens=100,
    num_beams=2,
    pad_token_id=response_tokenizer.eos_token_id,
    eos_token_id=response_tokenizer.eos_token_id,
    decoder_start_token_id=0
)

# Defining database schema
schema = '''
Schema Purpose:
- publications: Stores individual publications (1 row = 1 publication)
- publication_authors: Links authors to publications (N rows per publication)
- journals: Journal metadata
- authors: Author information

Query Guidelines:
1. For publication counts ALWAYS use publications table
2. Only use publication_authors when explicitly asked about:
   - Authorship details
   - Author-specific counts
3. Use journals table only when journal names/filtering are needed

Table Relationships:
- publications.journal_id → journals.id
- publication_authors.publication_id → publications.id
- publication_authors.author_id → authors.id

Optimization:
- Prefer EXISTS over JOINs when possible
- Use COUNT(DISTINCT ) when dealing with junction tables

Example Queries:
1. How many publications? → SELECT COUNT(*) FROM publications
2. Authors per publication? → SELECT publication_id, COUNT(*) FROM publication_authors GROUP BY 1
3. Publications by journal? → SELECT j.name, COUNT(p.id) FROM publications p JOIN journals j ON p.journal_id = j.id GROUP BY 1
'''

# Setup SQLAlchemy connection
DATABASE_URL = "sqlite:////data/publications.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def generate_visualization(question, results):
    plt.clf()
    keywords = ["chart", "graph", "show", "illustrate"]
    pattern = r"\b(visuali\w*)\b"
    if any(word in question.lower() for word in keywords) or re.search(pattern, question, re.IGNORECASE):
        labels = [row[0] if len(row) > 1 else "Count" for row in results]
        values = [row[1] if len(row) > 1 else row[0] for row in results]
        plt.bar(labels, values)
        plt.title(f"Visualization")
        plt.xlabel("Categories")
        plt.ylabel("Values")
        plt.savefig("/data/visualization.png")
        print("Visualization saved as /data/visualization.png")
        plt.show()

def generate_response(question, results, has_data):
    if not has_data:
        return "No relevant data available."
    
    processed_results = []
    for row in results:
        if len(row) == 1:
            processed_results.append(str(row[0]))
        else:
            processed_results.append(", ".join(map(str, row)))
    # Placeholder for RAG response
    context = "\n".join(processed_results)

    response_prompt = f"""Interpret these database results for a non-technical user:

    Question: {question}
    Raw Results: {context}

    Generate a concise, natural language response:"""

    response_inputs = response_tokenizer(response_prompt, return_tensors="pt").to(device)
    response_outputs = response_model.generate(**response_inputs, generation_config=response_gen_config)
    return response_tokenizer.decode(response_outputs[0], skip_special_tokens=True)

# Interactive loop for natural language queries
print("Torus.ai API is ready!")
while True:
    question = input("Enter your question (or 'quit' to exit): ")
    if question.lower() == "quit":
        break

    input_text = f"""Schema: {schema}
    Current Question: {question}
    Generate ONLY the SQL SELECT query:"""
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    outputs = sql_model.generate(**inputs, generation_config=sql_gen_config)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Generated SQL query: {sql_query}")

    if not sql_query.strip().upper().startswith("SELECT"):
        print("Invalid SQL query generated. Skipping execution.")
        continue

    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            results = result.fetchall()
            has_data = bool(results)

            if has_data:
                print("Results:")
                for row in results:
                    print(row)
                
                response = generate_response(question, results, has_data)
                print(f"Response: {response}")
                
                generate_visualization(question, results)
            else:
                print("No results found.")
                print("Response: No relevant data available.")

    except SQLAlchemyError as e:
        print(f"Error executing query: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

session.close()
print("Goodbye!")