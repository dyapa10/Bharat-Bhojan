import streamlit as st
import requests
import json
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Available models
AVAILABLE_MODELS = {
    "Qwen/Qwen2-1.5B-Instruct": "Qwen 2 1.5B",
    "Qwen/Qwen2-7B-Instruct": "Qwen 2 7B", 
    "microsoft/DialoGPT-medium": "DialoGPT Medium",
    "microsoft/DialoGPT-large": "DialoGPT Large",
    "facebook/blenderbot-400M-distill": "BlenderBot 400M",
    "facebook/blenderbot-1B-distill": "BlenderBot 1B",
    "google/flan-t5-base": "Flan-T5 Base",
    "google/flan-t5-large": "Flan-T5 Large"
}

class HuggingFaceChatbot:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.base_url = "https://api-inference.huggingface.co/models/"
    
    def generate_response(self, model_name: str, prompt: str, max_length: int = 150, temperature: float = 0.7) -> Optional[str]:
        """Generate response from Hugging Face model"""
        url = f"{self.base_url}{model_name}"
        
        # Prepare payload based on model type
        if "qwen" in model_name.lower() or "flan" in model_name.lower():
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_length,
                    "temperature": temperature,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
        else:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": temperature,
                    "do_sample": True
                }
            }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    generated_text = result[0]["generated_text"]
                    # Remove the original prompt if it's included
                    if generated_text.startswith(prompt):
                        generated_text = generated_text[len(prompt):].strip()
                    return generated_text
                elif "text" in result[0]:
                    return result[0]["text"]
            
            return "Sorry, I couldn't generate a response."
            
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error processing response: {str(e)}")
            return None

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = list(AVAILABLE_MODELS.keys())[0]

def display_chat_messages():
    """Display chat messages"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    # Initialize session state
    initialize_session_state()
    
    # Title and description
    st.title("🤖 AI Chatbot with Hugging Face")
    st.markdown("Chat with various AI models powered by Hugging Face!")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Token input
        api_token = st.text_input(
            "Hugging Face API Token",
            type="password",
            help="Get your token from https://huggingface.co/settings/tokens"
        )
        
        if not api_token:
            st.warning("Please enter your Hugging Face API token to continue.")
            st.stop()
        
        st.divider()
        
        # Model selection
        st.subheader("🎯 Model Selection")
        selected_model_key = st.selectbox(
            "Choose a model:",
            options=list(AVAILABLE_MODELS.keys()),
            format_func=lambda x: AVAILABLE_MODELS[x],
            index=list(AVAILABLE_MODELS.keys()).index(st.session_state.selected_model)
        )
        
        st.session_state.selected_model = selected_model_key
        
        st.divider()
        
        # Model parameters
        st.subheader("🔧 Parameters")
        max_length = st.slider("Max Response Length", 50, 500, 150)
        temperature = st.slider("Temperature", 0.1, 2.0, 0.7, 0.1)
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # Model info
        st.subheader("ℹ️ Current Model")
        st.info(f"**{AVAILABLE_MODELS[selected_model_key]}**\n\n`{selected_model_key}`")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display existing messages
        display_chat_messages()
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    chatbot = HuggingFaceChatbot(api_token)
                    
                    # Format prompt for better context
                    if len(st.session_state.messages) > 1:
                        # Include some conversation context
                        context_messages = st.session_state.messages[-3:-1]  # Last 2 exchanges
                        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context_messages])
                        formatted_prompt = f"{context}\nuser: {prompt}\nassistant:"
                    else:
                        formatted_prompt = f"user: {prompt}\nassistant:"
                    
                    response = chatbot.generate_response(
                        selected_model_key, 
                        formatted_prompt, 
                        max_length, 
                        temperature
                    )
                    
                    if response:
                        st.markdown(response)
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        error_msg = "Sorry, I encountered an error. Please try again."
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    with col2:
        # Chat statistics
        st.subheader("📊 Chat Stats")
        total_messages = len(st.session_state.messages)
        user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
        assistant_messages = len([msg for msg in st.session_state.messages if msg["role"] == "assistant"])
        
        st.metric("Total Messages", total_messages)
        st.metric("Your Messages", user_messages)
        st.metric("AI Responses", assistant_messages)
        
        # Tips
        st.subheader("💡 Tips")
        st.markdown("""
        - **Clear prompts** get better responses
        - **Adjust temperature** for creativity:
          - Lower (0.1-0.5): More focused
          - Higher (0.8-1.5): More creative
        - **Try different models** for varied styles
        - **Longer context** helps with follow-ups
        """)

if __name__ == "__main__":
    main()
