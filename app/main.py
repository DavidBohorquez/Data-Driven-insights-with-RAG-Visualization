from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#from sqlcoder import generate_response
#from sqlcoder import generate_visualization

app = FastAPI()

# Mount static files and templates
print("Mounting static files and templates...")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": ""})

'''@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, question: str = Form(...)):
    #sql_query = generate_response(question)
    print(f"Received question: {question}")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": response,
        "question": question
    })'''