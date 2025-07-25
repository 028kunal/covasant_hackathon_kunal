# 🗣️ Voice-Based Form Autofill with Generative AI

Automates online form filling using **voice commands**. Extracts form questions, generates a conversational flow, reads out questions (TTS), records answers (STT), and saves responses for auto-filling.

---

## 🚀 Features

- Parse Google/Microsoft Forms to extract questions automatically.
- Generate JSON chat flow for voice-based navigation.
- TTS (Text-to-Speech) to read questions aloud.
- STT (Speech-to-Text) to capture spoken answers.
- Stores responses in structured JSON for auto-filling.

---

## 🛠️ Tech Stack

- **FastAPI** (backend APIs)
- **BeautifulSoup** (web scraping)
- **Selenium** (web scraping)
- **React.js** (frontend)
- **Web Speech API** (TTS + STT)
- **JSON** for structured flows and responses

---

## 🧩 Workflow

1️⃣ Parse form URL → extract questions  
2️⃣ Generate chat flow JSON  
3️⃣ Voice-based Q&A (TTS + STT)  
4️⃣ Save responses in `form_data` for auto-fill

---

## 🖼️ Proof of Work

- `chat_flow_*.json` files in `form_data` (chat flows)
- `chat_responses_*.json` files in `form_data` (captured responses)
- Working backend + frontend integration

---

## ⚡ Quick Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
