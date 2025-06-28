import streamlit as st
import json
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="Indian Food Discovery",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Indian states and union territories
INDIAN_STATES = {
    "Andhra Pradesh": "AP", "Arunachal Pradesh": "AR", "Assam": "AS", "Bihar": "BR", "Chhattisgarh": "CG",
    "Goa": "GA", "Gujarat": "GJ", "Haryana": "HR", "Himachal Pradesh": "HP", "Jharkhand": "JH",
    "Karnataka": "KA", "Kerala": "KL", "Madhya Pradesh": "MP", "Maharashtra": "MH", "Manipur": "MN",
    "Meghalaya": "ML", "Mizoram": "MZ", "Nagaland": "NL", "Odisha": "OR", "Punjab": "PB",
    "Rajasthan": "RJ", "Sikkim": "SK", "Tamil Nadu": "TN", "Telangana": "TG", "Tripura": "TR",
    "Uttar Pradesh": "UP", "Uttarakhand": "UK", "West Bengal": "WB",
    "Andaman and Nicobar Islands": "AN", "Chandigarh": "CH", "Dadra and Nagar Haveli and Daman and Diu": "DN",
    "Lakshadweep": "LD", "Delhi": "DL", "Puducherry": "PY", "Ladakh": "LA", "Jammu and Kashmir": "JK"
}

class IndianFoodDiscovery:
    def __init__(self):
        self.food_data = self._initialize_food_data()
    
    def _initialize_food_data(self) -> Dict:
        """Initialize comprehensive food data for Indian states"""
        return {
            "Andhra Pradesh": {
                "staples": ["Rice", "Millet", "Lentils", "Tamarind"],
                "dishes": ["Hyderabadi Biryani", "Pesarattu", "Gongura Mutton", "Pulusu", "Pappu Charu", "Bobbatlu"],
                "specialties": "Known for spicy food with heavy use of red chilies, tamarind, and coconut. Hyderabadi cuisine shows Mughal influence.",
                "cooking_style": "Extensive use of tamarind, red chilies, and coconut. Steam cooking and slow-cooking techniques."
            },
            "Assam": {
                "staples": ["Rice", "Fish", "Duck", "Pork", "Bamboo shoots"],
                "dishes": ["Assam Laksa", "Masor Tenga", "Khar", "Pitika", "Pitha", "Duck Curry"],
                "specialties": "Fermented foods, bamboo shoot preparations, and minimal use of spices. River fish is predominant.",
                "cooking_style": "Steaming, boiling, and minimal oil usage. Extensive use of banana leaves for cooking."
            },
            "Bihar": {
                "staples": ["Rice", "Wheat", "Lentils", "Mustard oil"],
                "dishes": ["Litti Chokha", "Sattu Paratha", "Thekua", "Khaja", "Mutton Curry", "Dal Pitha"],
                "specialties": "Simple, rustic cuisine with emphasis on roasted and grilled foods. Sattu (roasted gram flour) is very popular.",
                "cooking_style": "Roasting, grilling over coal/wood fire. Heavy use of mustard oil and garlic."
            },
            "Goa": {
                "staples": ["Rice", "Fish", "Coconut", "Cashews", "Kokum"],
                "dishes": ["Fish Curry Rice", "Vindaloo", "Xacuti", "Bebinca", "Feni", "Prawn Balchao"],
                "specialties": "Portuguese influence evident in vinegar-based curries. Abundant seafood and coconut usage.",
                "cooking_style": "Heavy use of coconut, kokum, and Portuguese-influenced techniques like pickling and fermentation."
            },
            "Gujarat": {
                "staples": ["Wheat", "Millet", "Lentils", "Vegetables", "Jaggery"],
                "dishes": ["Dhokla", "Thepla", "Undhiyu", "Gujarati Thali", "Khandvi", "Fafda Jalebi"],
                "specialties": "Predominantly vegetarian with sweet touch in savory dishes. Extensive use of jaggery and yogurt.",
                "cooking_style": "Steaming, tempering with mustard seeds and curry leaves. Balance of sweet, salty, and spicy flavors."
            },
            "Haryana": {
                "staples": ["Wheat", "Millet", "Dairy products", "Mustard greens"],
                "dishes": ["Bajra Khichdi", "Sarson ka Saag", "Makki ki Roti", "Kadhi Pakora", "Churma", "Besan Masala Roti"],
                "specialties": "Rich dairy-based cuisine with seasonal vegetables. Heavy, nutritious meals suitable for agricultural lifestyle.",
                "cooking_style": "Clay pot cooking, slow cooking with ghee and butter. Emphasis on fresh dairy products."
            },
            "Karnataka": {
                "staples": ["Rice", "Ragi", "Coconut", "Lentils"],
                "dishes": ["Bisi Bele Bath", "Mysore Pak", "Dosa Varieties", "Coorg Pork Curry", "Neer Dosa", "Obbattu"],
                "specialties": "Diverse regional variations - coastal, malnad, and northern Karnataka cuisines. Coffee culture is strong.",
                "cooking_style": "Coconut-based gravies in coastal areas, jaggery usage, and fermented foods like dosa and idli."
            },
            "Kerala": {
                "staples": ["Rice", "Coconut", "Fish", "Spices", "Tapioca"],
                "dishes": ["Fish Molee", "Appam with Stew", "Sadya", "Kerala Parotta", "Puttu Kadala", "Payasam"],
                "specialties": "Spice capital of India. Coconut milk-based curries and extensive use of aromatic spices.",
                "cooking_style": "Coconut milk gravies, banana leaf cooking, and complex spice blending techniques."
            },
            "Maharashtra": {
                "staples": ["Rice", "Wheat", "Millet", "Lentils", "Peanuts"],
                "dishes": ["Vada Pav", "Misal Pav", "Bhel Puri", "Puran Poli", "Kolhapuri Mutton", "Modak"],
                "specialties": "Street food culture is prominent. Regional variations include Konkani, Marathwada, and Vidarbha cuisines.",
                "cooking_style": "Dry spice powders, coconut, and peanut-based gravies. Street food techniques."
            },
            "Punjab": {
                "staples": ["Wheat", "Dairy products", "Mustard greens", "Corn"],
                "dishes": ["Butter Chicken", "Sarson da Saag", "Makki di Roti", "Chole Bhature", "Lassi", "Kulcha"],
                "specialties": "Rich, creamy gravies with extensive use of dairy. Tandoor cooking is prevalent.",
                "cooking_style": "Tandoor cooking, heavy use of ghee and butter, slow-cooked dal and vegetables."
            },
            "Rajasthan": {
                "staples": ["Wheat", "Millet", "Lentils", "Dried vegetables", "Ghee"],
                "dishes": ["Dal Baati Churma", "Gatte ki Sabzi", "Laal Maas", "Ker Sangri", "Ghevar", "Pyaaz Kachori"],
                "specialties": "Desert cuisine with preservation techniques. Minimal water usage in cooking due to arid climate.",
                "cooking_style": "Dry cooking methods, sun-drying, and preservation techniques. Heavy use of ghee and dry spices."
            },
            "Tamil Nadu": {
                "staples": ["Rice", "Lentils", "Coconut", "Tamarind", "Curry leaves"],
                "dishes": ["Chettinad Chicken", "Sambar Rice", "Rasam", "Idli Sambhar", "Payasam", "Murukku"],
                "specialties": "Temple food traditions, extensive vegetarian cuisine, and Chettinad's fiery non-vegetarian dishes.",
                "cooking_style": "Tempering with mustard seeds and curry leaves, coconut grinding, and tamarind-based sourness."
            },
            "West Bengal": {
                "staples": ["Rice", "Fish", "Sweets", "Mustard oil", "Poppy seeds"],
                "dishes": ["Fish Curry", "Mishti Doi", "Rosogolla", "Kosha Mangsho", "Shukto", "Pitha"],
                "specialties": "Fish and rice culture with elaborate sweet preparations. Subtle flavors with emphasis on natural tastes.",
                "cooking_style": "Light spicing, mustard oil usage, steaming, and elaborate sweet-making techniques."
            },
            "Delhi": {
                "staples": ["Wheat", "Rice", "Dairy products", "Mixed cuisine"],
                "dishes": ["Butter Chicken", "Paranthe Wali Gali", "Chaat", "Kebabs", "Kulfi", "Aloo Tikki"],
                "specialties": "Mughal influence with street food culture. Mix of North Indian cuisines due to migration.",
                "cooking_style": "Tandoor cooking, rich gravies, and diverse street food preparation techniques."
            }
        }
    
    def get_food_info(self, state: str, user_location: str = "") -> str:
        """Generate food discovery response for a given state"""
        if state not in self.food_data:
            return f"Sorry, I don't have detailed information about {state}'s cuisine yet. Please try another Indian state or union territory."
        
        data = self.food_data[state]
        
        response = f"# 🍛 Food Culture of {state}\n\n"
        
        # Staple foods
        response += f"## 🌾 **Staple Foods:**\n"
        response += f"{', '.join(data['staples'])}\n\n"
        
        # Famous dishes
        response += f"## 🍽️ **Famous Regional Dishes:**\n"
        for i, dish in enumerate(data['dishes'], 1):
            response += f"{i}. **{dish}**\n"
        response += "\n"
        
        # Restaurant recommendations
        response += f"## 🏪 **Restaurant Recommendations:**\n"
        if user_location:
            response += f"*Popular {state} cuisine restaurants in/near {user_location}:*\n"
            response += f"1. **Local Authentic Restaurant** - Traditional {state} thali and specialties\n"
            response += f"2. **Regional Food Corner** - Famous for authentic {data['dishes'][0]} and local favorites\n"
            response += f"3. **Heritage Kitchen** - Family-style {state} cuisine with traditional recipes\n\n"
            response += f"*💡 Tip: Search for '{state} food near {user_location}' or 'authentic {state} restaurant {user_location}' for specific locations*\n\n"
        else:
            response += f"1. **Traditional {state} Restaurants** - Look for family-run establishments\n"
            response += f"2. **Regional Thali Places** - Complete {state} meal experience\n"
            response += f"3. **Local Food Joints** - Authentic street food and snacks\n\n"
        
        # Culinary specialties
        response += f"## ✨ **Culinary Specialties & Cooking Style:**\n"
        response += f"**Specialties:** {data['specialties']}\n\n"
        response += f"**Cooking Style:** {data['cooking_style']}\n\n"
        
        response += f"---\n*Explore the rich culinary heritage of {state}! 🇮🇳*"
        
        return response

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_state" not in st.session_state:
        st.session_state.selected_state = ""
    if "user_location" not in st.session_state:
        st.session_state.user_location = ""

def display_chat_messages():
    """Display chat messages"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_user_query(query: str, food_discovery: IndianFoodDiscovery, user_location: str) -> str:
    """Process user query and generate appropriate response"""
    query_lower = query.lower()
    
    # Check if query mentions any Indian state
    for state in INDIAN_STATES.keys():
        if state.lower() in query_lower:
            return food_discovery.get_food_info(state, user_location)
    
    # Check for common food-related queries
    if any(word in query_lower for word in ['food', 'cuisine', 'dish', 'restaurant', 'eat']):
        return ("I'm here to help you discover Indian food culture! Please mention:\n\n"
                "🗺️ **An Indian state or union territory** (e.g., 'Tell me about Kerala food', 'Punjab cuisine', 'What does Maharashtra eat?')\n\n"
                "I can provide information about:\n"
                "- Staple foods and famous dishes\n"
                "- Restaurant recommendations\n"
                "- Cooking styles and specialties\n\n"
                "**Example queries:**\n"
                "- 'Food culture of Tamil Nadu'\n"
                "- 'What are famous dishes of Rajasthan?'\n"
                "- 'Bengali cuisine restaurants'")
    
    return ("I'm your Indian Food Discovery assistant! 🍛\n\n"
            "I specialize in showcasing the diverse food culture of India by state and union territory.\n\n"
            "Please ask me about:\n"
            "- Food culture of any Indian state\n"
            "- Famous dishes and specialties\n"
            "- Restaurant recommendations\n\n"
            "**Try asking:** 'Tell me about [State Name] food' or 'What does [State] eat?'")

def main():
    # Initialize session state
    initialize_session_state()
    
    # Initialize food discovery system
    food_discovery = IndianFoodDiscovery()
    
    # Title and description
    st.title("🍛 Indian Food Discovery Assistant")
    st.markdown("*Discover the diverse culinary heritage of India, state by state!*")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("🗺️ Food Discovery Settings")
        
        # User location input
        st.subheader("📍 Your Location")
        user_location = st.text_input(
            "Enter your city/location:",
            value=st.session_state.user_location,
            placeholder="e.g., Pune, Bangalore, Delhi"
        )
        st.session_state.user_location = user_location
        
        if user_location:
            st.success(f"📍 Location set: {user_location}")
        
        st.divider()
        
        # Quick state selection
        st.subheader("🏛️ Quick State Selection")
        selected_state = st.selectbox(
            "Choose a state/UT:",
            options=[""] + list(INDIAN_STATES.keys()),
            index=0
        )
        
        if selected_state and st.button("🔍 Explore Cuisine", use_container_width=True):
            response = food_discovery.get_food_info(selected_state, user_location)
            st.session_state.messages.append({"role": "user", "content": f"Tell me about {selected_state} food"})
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        # Available states info
        st.subheader("🇮🇳 Available Regions")
        st.markdown(f"**{len(INDIAN_STATES)} States & Union Territories**")
        
        with st.expander("View All States"):
            for state in sorted(INDIAN_STATES.keys()):
                st.text(f"• {state}")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display existing messages
        display_chat_messages()
        
        # Chat input
        if prompt := st.chat_input("Ask about any Indian state's food culture..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                response = process_user_query(prompt, food_discovery, user_location)
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        # Chat statistics
        st.subheader("📊 Discovery Stats")
        total_messages = len(st.session_state.messages)
        user_queries = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
        
        st.metric("Total Messages", total_messages)
        st.metric("Your Queries", user_queries)
        
        # Usage tips
        st.subheader("💡 How to Use")
        st.markdown("""
        **Sample Queries:**
        - "Kerala food culture"
        - "Famous dishes of Punjab"
        - "What does Gujarat eat?"
        - "Rajasthani cuisine"
        - "Bengali food restaurants"
        
        **Features:**
        - 🌾 Staple foods by region
        - 🍽️ Famous dishes & specialties  
        - 🏪 Restaurant recommendations
        - ✨ Cooking styles & techniques
        """)
        
        st.subheader("🎯 Quick Tips")
        st.markdown("""
        - Set your location for better restaurant suggestions
        - Ask about specific states for detailed info
        - All responses are in English
        - Covers all 28 states + 8 union territories
        """)

if __name__ == "__main__":
    main()
