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

def get_api_token() -> Optional[str]:
    """
    Get API token from Streamlit Cloud app settings only
    """
    try:
        # Check for HUGGINGFACE_API_TOKEN in Streamlit secrets (Cloud settings)
        if hasattr(st, 'secrets') and "HUGGINGFACE_API_TOKEN" in st.secrets:
            return st.secrets["HUGGINGFACE_API_TOKEN"]
        
        # Fallback: Check for HF_TOKEN 
        if hasattr(st, 'secrets') and "HF_TOKEN" in st.secrets:
            return st.secrets["HF_TOKEN"]
        
        return None
        
    except Exception as e:
        st.error(f"Error accessing app settings: {str(e)}")
        return None

def display_cloud_setup_instructions():
    """Display setup instructions for Streamlit Cloud only"""
    st.error("❌ Hugging Face API Token not found in app settings")
    
    with st.expander("📖 Streamlit Cloud Setup Instructions", expanded=True):
        st.markdown("""
        ### How to Add Your API Token in Streamlit Cloud:
        
        1. **Go to your Streamlit Cloud dashboard**
        2. **Find your deployed app** and click on it
        3. **Click on the ⚙️ Settings button** (usually in the top right)
        4. **Navigate to the "Secrets" tab**
        5. **Add your token** in the text area:
        
        ```toml
        HUGGINGFACE_API_TOKEN = "your_actual_token_here"
        ```
        
        ### How to Get Your Hugging Face Token:
        1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
        2. Click **"New token"**
        3. Give it a name (e.g., "Streamlit Chatbot")
        4. Select **"Read"** permissions
        5. Click **"Generate a token"**
        6. **Copy the token** and paste it in your Streamlit Cloud app settings
        
        ### ⚠️ Important Notes:
        - Replace `"your_actual_token_here"` with your real token (keep the quotes)
        - After saving, your app will automatically restart
        - The token should start with `hf_`
        
        ### Alternative Token Name:
        You can also use `HF_TOKEN` instead of `HUGGINGFACE_API_TOKEN`:
        ```toml
        HF_TOKEN = "your_actual_token_here"
        ```
        """)
    
    st.info("💡 **Tip**: After adding your token in Streamlit Cloud settings, the app will restart automatically.")

class HuggingFaceChatbot:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.base_url = "https://api-inference.huggingface.co/models/"
    
    def test_connection(self) -> bool:
        """Test if the API token is valid"""
        try:
            # Test with a simple model
            test_url = f"{self.base_url}gpt2"
            test_payload = {"inputs": "test"}
            
            response = requests.post(
                test_url, 
                headers=self.headers, 
                json=test_payload,
                timeout=10
            )
            
            # Token is valid if we don't get a 401/403
            return response.status_code not in [401, 403]
            
        except Exception:
            return False
    
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
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            # Handle specific error cases
            if response.status_code == 401:
                st.error("❌ Invalid API token. Please check your token in Streamlit Cloud app settings.")
                return None
            elif response.status_code == 403:
                st.error("❌ Access forbidden. Your token may not have the required permissions.")
                return None
            elif response.status_code == 503:
                st.warning("⏳ Model is loading. Please try again in a moment.")
                return None
            
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
            
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")
            return None
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
    if "token_validated" not in st.session_state:
        st.session_state.token_validated = False

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
    
    # Get API token from Streamlit Cloud settings
    api_token = get_api_token()
    
    if not api_token:
        display_cloud_setup_instructions()
        st.stop()
    
    # Initialize chatbot
    chatbot = HuggingFaceChatbot(api_token)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Token status
        st.subheader("🔐 API Status")
        
        # Validate token on first run or when explicitly requested
        if not st.session_state.token_validated or st.button("🔍 Test Connection"):
            with st.spinner("Validating token..."):
                if chatbot.test_connection():
                    st.success("✅ API Token is valid")
                    st.session_state.token_validated = True
                else:
                    st.error("❌ API Token validation failed")
                    st.session_state.token_validated = False
                    st.error("Please check your token in Streamlit Cloud app settings.")
        elif st.session_state.token_validated:
            st.success("✅ API Token is valid")
        
        # Show masked token for verification
        masked_token = f"{api_token[:8]}...{api_token[-4:]}" if len(api_token) > 12 else "***"
        st.code(f"Token: {masked_token}")
        
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
        
        # Quick setup reminder
        with st.expander("🔧 Setup Reminder"):
            st.markdown("""
            **Token Location**: Streamlit Cloud App Settings → Secrets
            
            **Format**:
            ```toml
            HUGGINGFACE_API_TOKEN = "hf_your_token_here"
            ```
            """)
    
    # Only show chat interface if token is validated
    if not st.session_state.token_validated:
        st.warning("⚠️ Please validate your API token using the Test Connection button in the sidebar.")
        return
    
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
