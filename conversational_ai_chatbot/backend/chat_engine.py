import json
import os
from fastapi import HTTPException

current_dir = os.path.dirname(__file__)
data_folder = os.path.join(current_dir, "form_data")
sessions_folder = os.path.join(current_dir, "sessions")
os.makedirs(sessions_folder, exist_ok=True)

def load_flow(flow_file):
    path = os.path.join(data_folder, flow_file)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Chat flow file not found.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_session(session_id):
    path = os.path.join(sessions_folder, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"responses": {}, "current_question": 0}

def save_session(session_id, session_data):
    path = os.path.join(sessions_folder, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=4, ensure_ascii=False)

def proceed_chat(flow_file, session_id, user_answer=None):
    flow_data = load_flow(flow_file)
    session = load_session(session_id)

    # If user answered previous question, save it
    if user_answer is not None and session["current_question"] > 0:
        question_id = session["current_question"]
        session["responses"][str(question_id)] = user_answer

    # Check if completed
    if session["current_question"] >= len(flow_data["flow"]):
        # Save transcript on completion
        transcript_file = os.path.join(
            data_folder, f"chat_transcript_{session_id}.json"
        )
        with open(transcript_file, "w", encoding="utf-8") as f:
            json.dump(session, f, indent=4, ensure_ascii=False)
        return {"message": "Chat completed", "transcript_file": transcript_file}

    # Move to next question
    next_question = flow_data["flow"][session["current_question"]]
    session["current_question"] += 1
    save_session(session_id, session)

    return {"question_id": next_question["id"], "question": next_question["question"]}
