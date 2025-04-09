import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, GenerationConfig
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Tuple, Union

# Set device to CPU
device = torch.device("cpu")
print(f"loading sql model...")
# Load the fine-tuned SQL model and tokenizer
sql_model_name = "tscholak/3vnuv1vf" # "/data/finetuned_sql_model"
tokenizer = AutoTokenizer.from_pretrained(sql_model_name)
tokenizer.pad_token = tokenizer.eos_token
sql_model = AutoModelForSeq2SeqLM.from_pretrained(sql_model_name).to(device)
sql_model.config.pad_token_id = sql_model.config.eos_token_id

print(f"loading response model...")
# Load the response generation model and tokenizer
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

Table Columns:
- publications: id (INTEGER PRIMARY KEY), title (TEXT), journal_id (INTEGER), publication_date (TEXT, format like 'April 2024' or '2023')
- publication_authors: publication_id (INTEGER), author_id (INTEGER)
- journals: id (INTEGER PRIMARY KEY), name (TEXT)
- authors: id (INTEGER PRIMARY KEY), name (TEXT)

Query Guidelines:
1. For publication counts ALWAYS use publications table.
2. When counting rows, use COUNT(*) without a table alias (e.g., NOT t1.COUNT(*), but COUNT(*)).
3. Only use publication_authors when explicitly asked about:
   - Authorship details
   - Author-specific counts
4. Use journals table only when journal names/filtering are needed.
5. When joining publications and publication_authors, use publications.id = publication_authors.publication_id.

Table Relationships:
- publications.journal_id → journals.id
- publication_authors.publication_id → publications.id
- publication_authors.author_id → authors.id

Optimization:
- Prefer EXISTS over JOINs when possible.
- Use COUNT(DISTINCT ) when dealing with junction tables.

Example Queries:
1. How many publications? → SELECT COUNT(*) FROM publications
2. How many authors per publication? → SELECT p.id, COUNT(pa.author_id) FROM publications p JOIN publication_authors pa ON p.id = pa.publication_id GROUP BY p.id
3. Publications by journal? → SELECT j.name, COUNT(p.id) FROM publications p JOIN journals j ON p.journal_id = j.id GROUP BY j.name
'''

def generate_sql_query(question: str) -> str:
    """
    Generate SQL query from natural language question.

    Args:
        question (str): Natural language question.

    Returns:
        str: The generated SQL query.
    """
    input_text = f"""Schema: {schema}
    Current Question: {question}
    Generate ONLY the SQL SELECT query:"""
    
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = sql_model.generate(**inputs, generation_config=sql_gen_config)
    
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    return sql_query

def execute_sql_query(db: Session, sql_query: str) -> Tuple[list, Union[str, None]]:
    """Execute the SQL query using the provided database session and return the results or an error message.
    
    Args:
        db (Session): The database session for the current request.
        sql_query (str): The SQL query to execute.

    Returns:
        tuple[list, str | None]: A tuple containing the query results and an error message (str or None).
    """
    if not sql_query.upper().startswith("SELECT"):
        return [], "Invalid SQL query generated. Skipping execution."

    try:
        result = db.execute(text(sql_query))
        results = result.fetchall()
        return results, None
    except Exception as e:
        return [], f"Database error: {str(e)}"

def generate_response(question: str, results: list) -> str:
    """
    Generate a natural language response based on the question and SQL query results.

    Args:
        question (str): The user's question.
        results (list): The results from the database query.

        Returns:
        str: A natural language response.
    """
    if not results:
        return "No relevant data available."

    # Convert results to a string context
    context = "\n".join([", ".join(map(str, row)) for row in results])

    response_prompt = f"""Interpret these database results for a non-technical user:
    
    Question: {question}
    Raw Results: {context}

    Generate a concise, natural language response:"""

    response_inputs = response_tokenizer(response_prompt, return_tensors="pt").to(device)
    response_outputs = response_model.generate(**response_inputs, generation_config=response_gen_config)
    response = response_tokenizer.decode(response_outputs[0], skip_special_tokens=True)
    return response

def generate_visualization(question: str, result: List) -> None:
    """Generate a visualization (placeholder for web adaptation).

    Args:
        question (str): The user's question.
        results (list): The results from the database query.
    """
    # For web use, consider returning a base64 image or serving via an endpoint
    pass