from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend import rag

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

RAGAgent = rag.LocalRAGAgent()

@app.get("/", response_class=HTMLResponse)
def rag_demo(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def rag_demo(request: Request, query: str = Form()):
    answer = RAGAgent.invoke(query)
    return templates.TemplateResponse("index.html", {"request": request, "query": query, "answer": answer})