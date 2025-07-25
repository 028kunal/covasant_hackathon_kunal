from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

from chat_flow_generator import generate_conversation_flow
from fastapi.middleware.cors import CORSMiddleware
from chat_engine import proceed_chat



app = FastAPI()

# Ensure form_data folder exists relative to this script
data_folder = os.path.join(os.path.dirname(__file__), "form_data")
os.makedirs(data_folder, exist_ok=True)

# ✅ GLOBAL sessions dict to store chat sessions in memory
sessions = {}

class FormURL(BaseModel):
    url: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Backend is working. Visit /docs to test the API."}

@app.post("/forms/parse_url")
async def parse_form_url(form: FormURL):
    try:
        response = requests.get(form.url)
        soup = BeautifulSoup(response.text, "html.parser")

        possible_question_selectors = [
            "div.freebirdFormviewerComponentsQuestionBaseTitle",
            "div.office-form-question-title",
            "label",
            "span",
        ]

        questions = []
        seen = set()

        for selector in possible_question_selectors:
            for element in soup.select(selector):
                text = element.get_text(strip=True)
                if text and text not in seen and len(text) > 3:
                    questions.append(text)
                    seen.add(text)

        if not questions:
            raise HTTPException(status_code=400, detail="No questions found. Check form URL or adjust parser.")

        data = {
            "form_url": form.url,
            "questions": questions,
            "parsed_at": datetime.now().isoformat()
        }

        filename = os.path.join(
            data_folder, f"parsed_form_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return {"message": "Form parsed and saved", "file": filename, "questions": questions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_flow")
async def generate_flow(file_name: str = Query(..., description="Parsed form JSON filename inside form_data")):
    try:
        file_path = os.path.join(data_folder, file_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Parsed form file not found.")

        generated_file = generate_conversation_flow(file_path)
        return {"message": "Conversation flow generated successfully", "file": generated_file}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/start")
async def start_chat(
    file_name: str = Query(..., description="Chat flow JSON filename inside form_data"),
    session_id: str = Query(..., description="Unique session identifier")
):
    try:
        result = proceed_chat(file_name, session_id)
        if "question" in result:
            return {
                "message": "Chat session started",
                "session_id": session_id,
                "question": result["question"]
            }
        else:
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/answer")
async def answer_chat(
    session_id: str = Query(..., description="Session identifier"),
    file_name: str = Query(..., description="Chat flow JSON filename inside form_data"),
    answer: str = Body(..., embed=True, description="User's answer")
):
    try:
        result = proceed_chat(file_name, session_id, user_answer=answer)
        if "question" in result:
            return {
                "message": "Next question",
                "session_id": session_id,
                "question": result["question"]
            }
        else:
            return {
                "message": "Chat completed",
                "session_id": session_id,
                "transcript_file": result["transcript_file"]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))