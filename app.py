import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load AI Model
def load_ai_model(model_name):
    """Load AI model securely, handling API key retrieval."""
    try:
        if model_name.startswith("claude"):
            api_key = os.getenv("ANTHROPIC_API_KEY")
            return ChatAnthropic(model=model_name, anthropic_api_key=api_key, temperature=0.3) if api_key else None

        elif model_name == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            return ChatOpenAI(model="gpt-4", openai_api_key=api_key, temperature=0.3) if api_key else None

        elif model_name == "ollama":
            return ChatOllama(model="mistral")  # Using a default local Ollama model
        
        else:
            logging.warning(f"Unsupported model: {model_name}. Returning None.")
            return None

    except Exception as e:
        logging.error(f"Error loading AI model: {e}")
        return None


# Sidebar Configuration
def configure_sidebar():
    """Configures the sidebar for AI model selection in Streamlit."""
    with st.sidebar:
        st.header("AI Settings")
        selected_model = st.radio(
            "Choose AI Model",
            options=["claude-3-sonnet-20240229", "claude-3-opus-20240229", "openai", "ollama"],  
            index=0  # Setting "claude-3-sonnet-20240229" as the default selection
        )
    return selected_model


#  Initialize Chat Session
def setup_chat_session():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "step" not in st.session_state:
        st.session_state.step = "greeting"
    if "tech_stack" not in st.session_state:
        st.session_state.tech_stack = ""
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

#  Display Chat Messages
def show_chat():
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

#  Generate AI Response
def get_ai_response(prompt, ai_engine):
    if ai_engine:
        messages = [SystemMessage(content="You are an AI interviewer."), HumanMessage(content=prompt)]
        response = ai_engine.invoke(messages)
        return response.content if hasattr(response, "content") else str(response)  
    return "AI model not supported yet."

#  Generate Technical Questions (Limited to 5, Avoid Repeats)
def generate_next_question(ai_engine, tech_stack):
    if st.session_state.question_count >= 5:
        return "That's all for the interview! Thank you for your time."
    
    # Keep track of asked questions
    if "asked_questions" not in st.session_state:
        st.session_state.asked_questions = set()

    # Generate a new question that has not been asked before
    while True:
        prompt = f"""
        You are an AI interviewer. The candidate's tech stack is: {tech_stack}.
        Generate **one unique technical interview question** based on the tech stack.
        Do NOT repeat previously asked questions.
        Do NOT include explanations, only the question itself.
        """
        
        new_question = get_ai_response(prompt, ai_engine).strip()
        
        # Check if the question was already asked
        if new_question not in st.session_state.asked_questions:
            st.session_state.asked_questions.add(new_question)
            break

    st.session_state.question_count += 1
    return new_question


#  Handle User Input
def process_chat(user_message, ai_engine):
    try:
        EXIT_KEYWORDS = ["exit", "quit", "stop", "end"]
        
        if user_message.lower() in EXIT_KEYWORDS:
            st.session_state.chat_history.append({"role": "ai", "content": "Thank you for your time! We will get back to you."})
            st.rerun()
        
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        
        steps = {
            "greeting": ("Hello! Let's start. What's your full name?", "full_name"),
            "full_name": ("Thanks! Now, please provide your email address.", "email"),
            "email": ("Got it! Your phone number next, please.", "phone"),
            "phone": ("How many years of experience do you have?", "experience"),
            "experience": ("What position are you applying for?", "position"),
            "position": ("Where are you currently located?", "location"),
            "location": ("Finally, list your tech stack (e.g., Python, Django, SQL).", "tech_stack"),
        }
        
        if st.session_state.step in steps:
            response, next_step = steps[st.session_state.step]
            setattr(st.session_state, st.session_state.step, user_message)
            st.session_state.step = next_step
        elif st.session_state.step == "tech_stack":
            st.session_state.tech_stack = user_message
            response = "Great! Let's begin the technical interview. Here's your first question:"
            st.session_state.step = "questioning"
            response += "\n\n" + generate_next_question(ai_engine, st.session_state.tech_stack)
        elif st.session_state.step == "questioning":
            response = generate_next_question(ai_engine, st.session_state.tech_stack)
        else:
            response = "I'm not sure how to proceed. Can you clarify?"
        
        st.session_state.chat_history.append({"role": "ai", "content": response})
        st.rerun()
    except Exception as e:
        st.session_state.chat_history.append({"role": "ai", "content": f"An error occurred: {str(e)}. Please try again."})
        st.rerun()

#  Main Function
def main():
    st.title("TalentScout Hiring Assistant")
    st.write("Welcome to TalentScout! I'm here to guide you through the initial screening process.")
    st.caption("Secure, local AI-powered interview chatbot")
    
    selected_model = configure_sidebar()
    ai_engine = load_ai_model(selected_model)
    
    if not ai_engine:
        st.warning("API key is missing or model not supported. Please check your environment variables.")
        return
    
    setup_chat_session()
    show_chat()
    
    user_message = st.chat_input("Chat with the Hiring Assistant")
    if user_message:
        process_chat(user_message, ai_engine)

if __name__ == "__main__":
    main()
