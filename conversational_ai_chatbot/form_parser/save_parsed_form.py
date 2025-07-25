import json
import os
from datetime import datetime

def save_form_data(form_type, form_url_or_name, questions):
    data = {
        "form_type": form_type,
        "form_url_or_name": form_url_or_name,
        "questions": questions,
        "timestamp": datetime.now().isoformat()
    }
    
    # Ensure form_data directory exists
    save_dir = "../form_data"
    os.makedirs(save_dir, exist_ok=True)
    
    # Create filename safely
    safe_name = form_type + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    save_path = os.path.join(save_dir, safe_name)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ Form data saved to {save_path}")

# Example usage:
if __name__ == "__main__":
    form_type = input("Enter form type (google_form/typeform/microsoft_form): ")
    form_url_or_name = input("Enter form URL or name: ")
    # Example questions
    questions = [
        "What is your name?",
        "What is your email?",
        "What is your department?"
    ]
    save_form_data(form_type, form_url_or_name, questions)
