from bs4 import BeautifulSoup

def parse_html_form(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    questions = []

    # Extract <label> tags
    labels = soup.find_all('label')
    for label in labels:
        text = label.get_text(separator=' ', strip=True)
        if text:
            questions.append(text)

    # Extract placeholders if labels not found
    inputs = soup.find_all(['input', 'textarea'])
    for inp in inputs:
        placeholder = inp.get('placeholder')
        if placeholder and placeholder not in questions:
            questions.append(placeholder)

    return questions

if __name__ == "__main__":
    file_path = input("Enter path to HTML file: ")
    questions = parse_html_form(file_path)
    for idx, q in enumerate(questions, 1):
        print(f"{idx}. {q}")
