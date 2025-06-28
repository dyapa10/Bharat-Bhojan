import streamlit as st
import requests
import json
from typing import Optional

# Multiple model configurations
MODELS = {
    "Qwen3-0.6B": {
        "url": "https://api-inference.huggingface.co/models/Qwen/Qwen3-0.6B",
        "description": "Latest Qwen model - excellent for multilingual chat and reasoning",
        "max_length": 512,
        "temperature": 0.7
    },
    "Qwen2.5-7B-Instruct": {
        "url": "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct",
        "description": "Instruction-tuned Qwen model - great for following complex instructions",
        "max_length": 1024,
        "temperature": 0.6
    },
    "Llama-3.1-8B-Instruct": {
        "url": "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct",
        "description": "Meta's Llama 3.1 - excellent for chat and multilingual tasks",
        "max_length": 1024,
        "temperature": 0.7
    },
    "Mistral-7B-Instruct": {
        "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
        "description": "Mistral's efficient model - fast and reliable for conversations",
        "max_length": 512,
        "temperature": 0.7
    },
    "CodeLlama-7B-Instruct": {
        "url": "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-Instruct-hf",
        "description": "Code-specialized model - great for recipe formatting and structured responses",
        "max_length": 1024,
        "temperature": 0.5
    },
    "Zephyr-7B-Beta": {
        "url": "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        "description": "Optimized for helpful, harmless conversations about various topics",
        "max_length": 512,
        "temperature": 0.7
    },
    "Gemma-2B-Instruct": {
        "url": "https://api-inference.huggingface.co/models/google/gemma-2b-it",
        "description": "Google's lightweight model - fast responses for food queries",
        "max_length": 512,
        "temperature": 0.8
    }
}

def query_huggingface_model(prompt: str, model_name: str) -> Optional[str]:
    """Query any Hugging Face model using API key from Streamlit secrets"""
    try:
        # Read API key from Streamlit Cloud secrets
        api_key = st.secrets["HF_API_KEY"]
    except KeyError:
        return "API key not found in Streamlit secrets. Please add 'HF_API_KEY' to your app secrets."
    except Exception as e:
        return f"Error accessing secrets: {str(e)}"
    
    model_config = MODELS.get(model_name, MODELS["Qwen3-0.6B"])
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Adjust payload based on model type
    if "Qwen" in model_name or "Llama" in model_name or "Mistral" in model_name:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": model_config["max_length"],
                "temperature": model_config["temperature"],
                "do_sample": True,
                "return_full_text": False
            }
        }
    else:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": model_config["max_length"],
                "temperature": model_config["temperature"],
                "do_sample": True
            }
        }
    
    try:
        response = requests.post(model_config["url"], headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                # Handle different response formats
                if "generated_text" in result[0]:
                    return result[0]["generated_text"].strip()
                elif "text" in result[0]:
                    return result[0]["text"].strip()
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"].strip()
        elif response.status_code == 503:
            return "Model is loading, please try again in a few moments..."
        return f"Error: {response.status_code} - {response.text[:200]}"
    except requests.exceptions.Timeout:
        return "Request timed out. The model might be busy, please try again."
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
    },
    "Tamil Nadu": {
        "staple": "Rice, lentils, and coconut with extensive use of tamarind.",
        "famous_dishes": ["Sambar", "Rasam", "Dosa", "Idli", "Chettinad Chicken"],
        "restaurants": {
            "Chennai": ["Saravana Bhavan", "Murugan Idli Shop", "Anjappar"],
            "default": ["Dakshin", "South Indian Coffee House"]
        },
        "specialty": "Temple cuisine traditions, fermented foods, and complex spice blends."
    },
    "Maharashtra": {
        "staple": "Rice, wheat, and jowar with extensive use of peanuts and sesame.",
        "famous_dishes": ["Vada Pav", "Misal Pav", "Puran Poli", "Bhel Puri"],
        "restaurants": {
            "Mumbai": ["Trishna", "Mahesh Lunch Home", "Kyani & Co"],
            "default": ["Maharashtrian Bhojnalaya", "Vithal Kamats"]
        },
        "specialty": "Street food culture, coastal seafood, and festival-specific sweets."
    }
}

# Streamlit App UI
st.set_page_config(page_title="Indian Food Explorer", page_icon="🇮🇳", layout="wide")

st.title("🇮🇳 Advanced Indian Food Explorer with Multiple AI Models")
st.write("Discover regional cuisines and get AI-powered food recommendations using cutting-edge language models!")

# Check API key status in sidebar
with st.sidebar:
    st.header("🤖 AI Model Selection")
    
    try:
        # Check if API key exists in secrets
        api_key = st.secrets["HF_API_KEY"]
        if api_key:
            st.success("✅ API key configured and ready!")
            
            # Model selection
            selected_model = st.selectbox(
                "Choose AI Model:",
                list(MODELS.keys()),
                help="Different models have different strengths - experiment to find your favorite!"
            )
            
            # Display model information
            model_info = MODELS[selected_model]
            st.info(f"**{selected_model}**\n\n{model_info['description']}")
            
        else:
            st.error("❌ API key is empty in secrets")
            selected_model = "Qwen3-0.6B"
    except KeyError:
        st.error("❌ API key not found in Streamlit secrets")
        st.markdown("**To enable AI chat:**")
        st.markdown("1. Go to your Streamlit Cloud app settings")
        st.markdown("2. Navigate to 'Secrets' section")
        st.markdown("3. Add the following:")
        st.code('''HF_API_KEY = "your_huggingface_api_token_here"''')
        st.markdown("4. Get your token from: https://huggingface.co/settings/tokens")
        selected_model = "Qwen3-0.6B"
    except Exception as e:
        st.error(f"❌ Error accessing secrets: {str(e)}")
        selected_model = "Qwen3-0.6B"
    
    st.markdown("---")
    st.info("💡 Try different models for varied responses! Some are better for recipes, others for cultural insights.")

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
    
    # Check if API key is available before showing chat interface
    try:
        api_key_check = st.secrets["HF_API_KEY"]
        api_available = bool(api_key_check)
    except:
        api_available = False
    
    if not api_available:
        st.warning("⚠️ AI chat is disabled. Please configure HF_API_KEY in Streamlit secrets to enable AI features.")
        st.info("See the sidebar for setup instructions.")
    else:
        # Chat interface
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for i, (user_msg, bot_msg, model_used) in enumerate(st.session_state.chat_history):
                st.write(f"**You:** {user_msg}")
                st.write(f"**AI ({model_used}):** {bot_msg}")
                st.write("---")
        
        # Quick suggestion buttons
        st.subheader("🚀 Quick Questions")
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🍛 Recipe suggestions"):
                user_question = f"Give me 3 authentic {state} recipes that are beginner-friendly"
                st.session_state.quick_question = user_question
            if st.button("🌶️ Spice guide"):
                user_question = f"What are the key spices used in {state} cuisine and how to use them?"
                st.session_state.quick_question = user_question
        
        with col_b:
            if st.button("🥘 Cooking tips"):
                user_question = f"Share cooking techniques specific to {state} cuisine"
                st.session_state.quick_question = user_question
            if st.button("🍽️ Food pairing"):
                user_question = f"What foods pair well with {', '.join(food_data[state]['famous_dishes'][:2])}?"
                st.session_state.quick_question = user_question
        
        # Chat input
        user_question = st.text_input("Ask the AI about Indian food, recipes, or cooking tips:", 
                                     placeholder="e.g., How do I make authentic biryani? What spices go with fish curry?",
                                     value=st.session_state.get('quick_question', ''))
        
        if st.button("Ask AI", type="primary") and user_question:
            # Create context-aware prompt
            context = f"You are an expert on Indian cuisine with deep knowledge of regional specialties. "
            if state:
                selected_dishes = ", ".join(food_data[state]["famous_dishes"][:3])
                context += f"The user is currently exploring {state} cuisine, known for dishes like {selected_dishes}. "
            
            # Enhanced prompt based on model type
            if "Qwen" in selected_model:
                full_prompt = f"{context}\n\nUser question: {user_question}\n\nPlease provide a detailed, helpful response about Indian food with specific tips and cultural context:"
            elif "Llama" in selected_model:
                full_prompt = f"[INST] {context}\n\nUser question: {user_question}\n\nProvide a comprehensive answer about Indian cuisine. [/INST]"
            elif "Mistral" in selected_model:
                full_prompt = f"<s>[INST] {context}\n\nUser question: {user_question} [/INST]"
            else:
                full_prompt = f"{context}\n\nUser question: {user_question}\n\nResponse:"
            
            with st.spinner(f"AI ({selected_model}) is thinking..."):
                ai_response = query_huggingface_model(full_prompt, selected_model)
            
            # Add to chat history with model info
            st.session_state.chat_history.append((user_question, ai_response, selected_model))
            
            # Clear quick question
            if 'quick_question' in st.session_state:
                del st.session_state.quick_question
            
            st.rerun()

# Model comparison section
st.header("🔬 Model Comparison Guide")
col3, col4 = st.columns(2)

with col3:
    st.subheader("🎯 Best Models For:")
    st.write("""
    **Recipe Instructions:** CodeLlama-7B-Instruct, Qwen2.5-7B-Instruct
    
    **Cultural Context:** Llama-3.1-8B-Instruct, Qwen3-0.6B
    
    **Quick Responses:** Gemma-2B-Instruct, Mistral-7B-Instruct
    
    **Detailed Analysis:** Qwen2.5-7B-Instruct, Zephyr-7B-Beta
    """)

with col4:
    st.subheader("⚡ Model Characteristics:")
    st.write("""
    **Qwen Series:** Multilingual capabilities, excellent reasoning
    
    **Llama 3.1:** Strong chat interactions, supports multiple languages
    
    **Mistral:** Fast inference, efficient responses
    
    **CodeLlama:** Structured output, great for formatted recipes
    """)

# Additional features
st.header("📊 Application Statistics")
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("States Covered", len(food_data))
with col6:
    total_dishes = sum(len(data["famous_dishes"]) for data in food_data.values())
    st.metric("Famous Dishes", total_dishes)
with col7:
    st.metric("AI Models", len(MODELS))
with col8:
    if 'chat_history' in st.session_state:
        st.metric("Chat Messages", len(st.session_state.chat_history))
    else:
        st.metric("Chat Messages", 0)

# Instructions
with st.expander("📋 How to use this app"):
    st.write("""
    **🗺️ Explore Regional Food:**
    - Select a state to learn about its cuisine
    - Enter your city for local restaurant recommendations
    
    **🤖 AI Assistant Features:**
    - Choose from 7 different AI models
    - Use quick question buttons for instant suggestions
    - Ask about recipes, cooking techniques, spice usage, food pairing
    
    **🔬 Model Selection Guide:**
    - **Qwen models**: Best for multilingual and reasoning tasks
    - **Llama 3.1**: Excellent for conversational responses
    - **Mistral**: Fast and efficient for quick queries
    - **CodeLlama**: Great for structured recipe formatting
    - **Gemma**: Lightweight and speedy responses
    - **Zephyr**: Optimized for helpful conversations
    
    **⚙️ Setup Requirements:**
    - Get a free Hugging Face API token from: https://huggingface.co/settings/tokens
    - Add 'HF_API_KEY' to your Streamlit Cloud app secrets
    - Some models may need a few moments to load initially
    """)

# Clear chat history button
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for Indian food lovers | Powered by Multiple Hugging Face AI Models")
st.markdown("*Try different models to see varied perspectives on the same questions!*")
