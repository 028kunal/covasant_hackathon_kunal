import csv
from save_parsed_form import save_form_data

def parse_microsoft_form_csv(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Header row contains questions
        for header in headers:
            if header.strip():
                questions.append(header.strip())
    return questions

if __name__ == "__main__":
    file_path = input("Enter the path to Microsoft Forms CSV export: ")
    questions = parse_microsoft_form_csv(file_path)
    save_form_data("microsoft_form", file_path, questions)
    for idx, question in enumerate(questions, 1):
        print(f"{idx}. {question}")
