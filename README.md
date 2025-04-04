# AI/ML-INTERN-ASSESSMENT

# TalentScout Hiring Assistant

TalentScout Hiring Assistant is a lightweight AI-powered interview chatbot that helps streamline the candidate screening process. Built using Streamlit and LangChain, this assistant enables interactive AI-driven interviews while ensuring privacy and efficiency.

## 🚀 Features

- **AI-Powered Interviews** – Generates dynamic, unique technical questions based on the candidate’s tech stack.
- **Supports Multiple AI Models** – Works with Claude, OpenAI GPT, and Ollama models.
- **Privacy & Security** – No sensitive data is stored or shared externally.
- **Simple & Fast Setup** – Easily configurable via environment variables.
- **Interactive Chat Interface** – Built with Streamlit for a seamless user experience.

---
## 📌 Requirements

- Python 3.10
- Ollama installed on your machine

## 🛠 Installation & Setup


###  Install Dependencies
```sh
pip install streamlit langchain_core langchain_community langchain_ollama
```

### Set API Keys (for Cloud AI Models)
If you want to use OpenAI or Claude models, export API keys as environment variables:
```sh
export ANTHROPIC_API_KEY=your_anthropic_api_key
export OPENAI_API_KEY=your_openai_api_key
```

###  Run the Application
```sh
streamlit run app.py
```

---

## ⚙️ AI Model Support
TalentScout supports multiple AI models for flexible and adaptable hiring assessments:
- **Claude (Anthropic)** – `claude-3-sonnet-20240229`, `claude-3-opus-20240229`
- **OpenAI GPT** – `gpt-4`
- **Ollama (Local AI)** – `mistral`

  
---

## 🏗 Project Structure
```
📂 LocalAI Chat
├── app.py  # Main application script
├── README.md  # Project documentation
├── requirements.txt  # Required dependencies
└── venv/  # Virtual environment (optional)
```

## 🤖 How It Works
1. Select an AI model from the sidebar.
2. Start chatting with the assistant.
3. Enjoy fast and secure local AI interactions without any cloud dependency.

## 🔗 Useful Links
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [Ollama](https://ollama.com/)


---

## 📩 Contact
For questions or contributions, feel free to reach out!
murarisen8878@gmail.com
