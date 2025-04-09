from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Dict, Any
from models.database import get_db
from sqlcoder import generate_sql_query, execute_sql_query, generate_response

app = FastAPI()
print(f"Starting FastAPI app...")
# Mount static files and templates
print("Mounting static files and templates...")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "response": ""})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, question: str = Form(...), db: Session = Depends(get_db)):
    try:
        # Generate SQL query
        sql_query = generate_sql_query(question)
        # Execute the query using the provided database session
        results, error = execute_sql_query(db, sql_query)
        if error:
            response = f"Error: {error}"
        else:
            # Generate natural language response
            response = generate_response(question, results)
    except Exception as e:
        sql_query = "Error generating SQL query"
        response = f"Error: {str(e)}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": response,
        "sql_query": sql_query
        })