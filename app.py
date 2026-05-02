import streamlit as st
from groq import Groq

# 1. Setup the Page
st.set_page_config(page_title="IsraelGPT", page_icon="🇮🇱")
st.title("🇮🇱 IsraelGPT")
st.write("Ask me anything about Israel's history, tech, or culture!")

# 2. Securely get the API Key (We will set this up in Step 3)
# For local testing, you can replace this with: client = Groq(api_key="YOUR_KEY_HERE")
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input
if prompt := st.chat_input("What would you like to know about Israel?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Generate IsraelGPT Response
    with st.chat_message("assistant"):
        # We add the "System Prompt" here to force it to be IsraelGPT
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are IsraelGPT. You are an expert on Israel. Give fun, precise, and interesting facts. Be proud and informative."},
                *st.session_state.messages
            ],
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
