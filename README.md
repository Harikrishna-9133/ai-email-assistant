# AI Email Assistant ✉️

An AI-powered email writing assistant built with Python, Streamlit, and Google's Gemini API. Generate professional emails from simple text instructions or voice input.

## 🚀 Features

- **AI Email Generation:** Create professional emails from natural-language prompts.
- **Voice Input:** Provide instructions using your microphone.
- **Streaming Responses:** View generated email content as it arrives.
- **Editable Output:** Review and edit the generated email before using it.
- **Download Emails:** Download generated emails as `.txt` files.
- **Simple Interface:** Use the application through a clean Streamlit web interface.

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **AI Model:** Google Gemini (`gemini-3.1-flash-lite`)
- **Voice Input:** Streamlit Mic Recorder
- **Environment Variables:** python-dotenv

## 📁 Project Structure

```text
ai-email-assistant/
├── app.py
├── requirements.txt
├── .env                 # Create locally; never upload
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Harikrishna-9133/ai-email-assistant.git
cd ai-email-assistant
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. Keep this file private and never commit it to GitHub.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, where you can use the application.

## 🔐 Security

- Store your Gemini API key in the `.env` file locally.
- Never commit API keys, credentials, or other secrets.
- Keep `.env` and `.venv/` excluded through `.gitignore`.

## 🎯 Future Enhancements

- Email tone and style selection.
- Support for multiple languages.
- Email templates for job applications and professional communication.
- Integration with email services for sending messages.

## 👨‍💻 Author

**Hari Krishna Digiventi**

GitHub: [Harikrishna-9133](https://github.com/Harikrishna-9133)

---

*Built to make professional email writing faster and easier with AI.*
