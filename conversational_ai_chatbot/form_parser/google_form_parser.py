import requests
from bs4 import BeautifulSoup
from save_parsed_form import save_form_data

def parse_google_form(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch form: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    questions = []

    for div in soup.find_all('div', {'role': 'listitem'}):
        question = div.get_text(separator=' ', strip=True)
        if question:
            questions.append(question)

    return questions

if __name__ == "__main__":
    form_url = input("Enter Google Form preview URL: ")
    questions = parse_google_form(form_url)
    save_form_data("google_form", form_url, questions)
    for idx, q in enumerate(questions, 1):
        print(f"{idx}. {q}")
