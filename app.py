import streamlit as st
import requests

# Hugging Face API setup
HF_API_KEY = st.secrets["HF_API_KEY"]

API_URLS = {
    "Qwen-2B": "https://api-inference.huggingface.co/models/Qwen/Qwen1.5-2B",
    "Mistral": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
    "LLaMA-2": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
}

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# Streamlit UI
st.title("🤖 Chatbot with Hugging Face Models")

# Sidebar: Choose model
model_choice = st.selectbox("Choose a model", list(API_URLS.keys()))
st.write(f"Model selected: {model_choice}")

# Chat interface
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", key="user_input")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        # Display user message
        st.session_state.history.append(("You", user_input))

        # Call Hugging Face API
        payload = {
            "inputs": {
                "text": user_input
            }
        }

        with st.spinner("Thinking..."):
            response = requests.post(API_URLS[model_choice], headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                # Attempt to get generated text from known response format
                if isinstance(result, list) and "generated_text" in result[0]:
                    bot_reply = result[0]["generated_text"]
                elif isinstance(result, dict) and "generated_text" in result:
                    bot_reply = result["generated_text"]
                else:
                    bot_reply = "Response received, but couldn't parse the output."
            else:
                bot_reply = f"Error: {response.status_code} - {response.text}"

        st.session_state.history.append((model_choice, bot_reply))

# Display chat history
st.divider()
for sender, msg in st.session_state.history:
    st.markdown(f"**{sender}:** {msg}")
