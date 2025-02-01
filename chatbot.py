import os
import groq
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Now, retrieve the API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set it in the .env file.")

# Initialize Groq client with the API key
client = groq.Groq(api_key=api_key)

# System prompt
from system_prompt3 import system_prompt

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Check if GenZ mode is enabled
if "genz_enabled" not in st.session_state:
    st.session_state.genz_enabled = False

# Streamlit app
st.title("Groq AI Chatbot")

# Sliding toggle button for GenZ mode using st.checkbox
st.markdown("""
    <style>
    .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }

    .switch input { 
        opacity: 0;
        width: 0;
        height: 0;
    }

    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        transition: .4s;
        border-radius: 34px;
    }

    .slider:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        border-radius: 50%;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: .4s;
    }

    input:checked + .slider {
        background-color: #3b82f6;
    }

    input:checked + .slider:before {
        transform: translateX(26px);
    }
    </style>
    """, unsafe_allow_html=True)

# Create a checkbox styled as a toggle switch
toggle = st.checkbox('Enable GenZ', key="genz_toggle", value=st.session_state.genz_enabled)

if toggle != st.session_state.genz_enabled:
    st.session_state.genz_enabled = toggle

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Modify the system prompt based on GenZ mode
if st.session_state.genz_enabled:
    # GenZ Mode prompt (casual, informal without emojis)
    updated_system_prompt = """
    You are a friendly chatbot. Respond to user queries in a chill, informal way. Use slang and casual language, but no emojis. 
    If the user seems sad, angry, or happy, acknowledge their feelings and respond empathetically, but in a laid-back, GenZ way. 
    Keep it casual, but avoid overusing slang. Think of responding like a friend would—light and relaxed.
    """
    if st.session_state.messages[0]["content"] != updated_system_prompt:
        st.session_state.messages[0]["content"] = updated_system_prompt
else:
    # Normal Mode prompt (neutral, friendly, and mature)
    normal_system_prompt = """
    You are a friendly chatbot. Respond to user queries in a polite, friendly, and casual tone. Keep the responses neutral and professional.
    If the user seems sad, angry, or happy, acknowledge their feelings and respond empathetically, but maintain a mature, friendly tone.
    Respond in a clear, friendly, but not overly informal manner.
    """
    if st.session_state.messages[0]["content"] != normal_system_prompt:
        st.session_state.messages[0]["content"] = normal_system_prompt

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama3-8b-8192"
        )
        bot_response = response.choices[0].message.content
        st.markdown(bot_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
