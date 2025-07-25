import json
from save_parsed_form import save_form_data

def parse_typeform_json(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        for field in data.get('fields', []):
            title = field.get('title', '').strip()
            if title:
                questions.append(title)
    return questions

if __name__ == "__main__":
    file_path = input("Enter the path to Typeform JSON export: ")
    questions = parse_typeform_json(file_path)
    save_form_data("typeform", file_path, questions)
    for idx, question in enumerate(questions, 1):
        print(f"{idx}. {question}")
