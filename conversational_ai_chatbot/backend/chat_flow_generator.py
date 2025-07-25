import json
from datetime import datetime
import os

# Consistent folder placement
current_dir = os.path.dirname(__file__)
data_folder = os.path.join(current_dir, "form_data")

def generate_conversation_flow(parsed_file_path):
    with open(parsed_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = data.get("questions", [])

    flow = []
    for idx, question in enumerate(questions):
        flow.append({
            "id": idx + 1,
            "question": question,
            "expected_type": "text",   # Default type for now
            "options": []              # Empty, extendable for MCQs later
        })

    flow_data = {
        "form_url": data.get("form_url", ""),
        "flow": flow,
        "generated_at": datetime.now().isoformat()
    }

    filename = os.path.join(
        data_folder, f"chat_flow_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    )
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(flow_data, f, indent=4, ensure_ascii=False)

    return filename
