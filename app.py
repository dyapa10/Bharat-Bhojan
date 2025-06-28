import streamlit as st
import requests
import json
from typing import Optional

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
# API key will be stored securely in Streamlit Cloud secrets
HF_API_KEY = st.secrets.get("HF_API_KEY", "")

def query_huggingface_chat(prompt: str, api_key: str = None) -> Optional[str]:
    """Query Hugging Face chat model"""
    # Use provided API key or fall back to secrets
    key_to_use = api_key or st.secrets.get("HF_API_KEY", "")
    
    if not key_to_use:
        return "API key not configured. Please add it in Streamlit Cloud secrets or enter manually."
    
    headers = {"Authorization": f"Bearer {key_to_use}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 150,
            "temperature": 0.7,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
        return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error connecting to Hugging Face: {str(e)}"

# Enhanced food data with more states
food_data = {
    "Punjab": {
        "staple": "Wheat-based items such as roti, paratha, and lassi.",
        "famous_dishes": ["Butter Chicken", "Sarson da Saag with Makki di Roti", "Chole Bhature", "Amritsari Kulcha"],
        "restaurants": {
            "Amritsar": ["Kesar Da Dhaba", "Bharawan Da Dhaba", "Beera Chicken House"],
            "default": ["Punjab Grill", "Pind Balluchi", "Baba Chicken"]
        },
        "specialty": "Rich use of dairy, tandoori cooking, and hearty meals with community-style dining."
    },
    "West Bengal": {
        "staple": "Rice and fish form the core of the Bengali diet.",
        "famous_dishes": ["Shorshe Ilish", "Macher Jhol", "Shukto", "Rasgulla", "Sandesh"],
        "restaurants": {
            "Kolkata": ["6 Ballygunge Place", "Bhojohori Manna", "Aminia"],
            "default": ["Oh! Calcutta", "Bengali Sweet House"]
        },
        "specialty": "Mustard oil cooking, use of poppy seeds, balance of sweet and spicy flavors."
    },
    "Kerala": {
        "staple": "Rice, coconut, and spices are fundamental to Kerala cuisine.",
        "famous_dishes": ["Fish Curry", "Appam with Stew", "Beef Fry", "Puttu", "Payasam"],
        "restaurants": {
            "Kochi": ["Dhe Puttu", "Gokul Oottupura", "Cassava"],
            "default": ["Sadhya", "Coconut Lagoon"]
        },
        "specialty": "Extensive use of coconut, curry leaves, and traditional cooking in banana leaves."
    },
    "Rajasthan": {
        "staple": "Wheat, lentils, and dairy products with minimal use of water.",
        "famous_dishes": ["Dal Baati Churma", "Gatte ki Sabzi", "Laal Maas", "Pyaaz Kachori"],
        "restaurants": {
            "Jaipur": ["Chokhi Dhani", "Handi Restaurant", "Rawat Mishthan Bhandar"],
            "default": ["Rajdhani Thali Restaurant", "Sankalp"]
        },
        "specialty": "Desert cuisine with long shelf-life foods, minimal water usage, and intense spicing."
    }
}

# Streamlit App UI
st.set_page_config(page_title="Indian Food Explorer", page_icon="🇮🇳", layout="wide")

st.title("🇮🇳 Regional Indian Food Explorer with AI Chat")
st.write("Discover staple foods, famous dishes, and iconic restaurants across India's diverse regions - now with AI-powered food recommendations!")

# Sidebar for API key (optional - can also use secrets)
with st.sidebar:
    st.header("🤖 AI Chat Settings")
    
    # Check if API key is already in secrets
    has_secret_key = bool(st.secrets.get("HF_API_KEY", ""))
    
    if has_secret_key:
        st.success("✅ API key configured in Streamlit secrets")
        api_key = st.secrets["HF_API_KEY"]
        show_input = st.checkbox("Override with manual key")
        if show_input:
            api_key = st.text_input("Manual Hugging Face API Key", type="password")
    else:
        st.info("💡 Add HF_API_KEY to Streamlit secrets for permanent storage")
        api_key = st.text_input("Hugging Face API Key", type="password", 
                               help="Get your free API key from https://huggingface.co/settings/tokens")
    
    st.markdown("---")
    st.markdown("**How to add to Streamlit secrets:**")
    st.code('''
# In your Streamlit Cloud app settings:
[secrets]
HF_API_KEY = "your_actual_api_key_here"
    ''')
    st.info("💡 The AI can help with recipe suggestions, cooking tips, and food recommendations!")

# Main content in two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📍 Regional Food Information")
    
    state = st.selectbox("Select a State or Union Territory", list(food_data.keys()))
    location = st.text_input("Enter your city or location (optional)")

    if state:
        region_info = food_data.get(state, {})
        
        st.subheader(f"🍚 Staple Food of {state}")
        st.write(region_info.get("staple", "Information not available."))

        st.subheader(f"🍛 Famous Dishes from {state}")
        dishes = region_info.get("famous_dishes", [])
        for dish in dishes:
            st.write(f"• {dish}")

        st.subheader(f"🍽️ Popular Restaurants")
        if location and location in region_info["restaurants"]:
            restaurants = region_info["restaurants"][location]
        else:
            restaurants = region_info["restaurants"].get("default", [])
        for res in restaurants:
            st.write(f"• {res}")

        st.subheader("🌟 Culinary Specialty")
        st.write(region_info.get("specialty", "Details not available."))

with col2:
    st.header("🤖 AI Food Assistant")
    
    # Chat interface
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
            st.write(f"**You:** {user_msg}")
            st.write(f"**AI:** {bot_msg}")
            st.write("---")
    
    # Chat input
    user_question = st.text_input("Ask the AI about Indian food, recipes, or cooking tips:", 
                                 placeholder="e.g., How do I make authentic biryani? What spices go with fish curry?")
    
    if st.button("Ask AI") and user_question:
        # Use API key from secrets or manual input
        current_api_key = api_key if 'api_key' in locals() else st.secrets.get("HF_API_KEY", "")
        
        if not current_api_key:
            st.error("Please configure your Hugging Face API key in Streamlit secrets or enter it manually in the sidebar.")
        else:
            # Create context-aware prompt
            context = f"You are an expert on Indian cuisine. "
            if state:
                selected_dishes = ", ".join(food_data[state]["famous_dishes"][:3])
                context += f"The user is currently exploring {state} cuisine, known for dishes like {selected_dishes}. "
            
            full_prompt = f"{context}\n\nUser question: {user_question}\n\nProvide a helpful, informative response about Indian food:"
            
            with st.spinner("AI is thinking..."):
                ai_response = query_huggingface_chat(full_prompt, current_api_key)
            
            # Add to chat history
            st.session_state.chat_history.append((user_question, ai_response))
            st.rerun()

# Additional features
st.header("🔍 Quick Food Facts")
col3, col4, col5 = st.columns(3)

with col3:
    st.metric("States Covered", len(food_data))
with col4:
    total_dishes = sum(len(data["famous_dishes"]) for data in food_data.values())
    st.metric("Famous Dishes", total_dishes)
with col5:
    st.metric("AI Model", "DialoGPT-medium")

# Instructions
with st.expander("📋 How to use this app"):
    st.write("""
    1. **Explore Regional Food**: Select a state to learn about its cuisine
    2. **Get AI Help**: Add your Hugging Face API key and ask questions about:
       - Recipe suggestions and cooking tips
       - Ingredient substitutions
       - Food pairing recommendations
       - Cultural context of dishes
    3. **Location-specific Info**: Enter your city for local restaurant recommendations
    
    **Getting your API Key:**
    - Visit https://huggingface.co/settings/tokens
    - Create a free account and generate a new token
    - Paste it in the sidebar to enable AI chat
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for Indian food lovers | Powered by Hugging Face AI")
