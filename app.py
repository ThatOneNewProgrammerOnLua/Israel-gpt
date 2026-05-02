import streamlit as st
from groq import Groq

# Page Setup
st.set_page_config(page_title="IsraelGPT", page_icon="🇮🇱")
st.title("🇮🇱 IsraelGPT")
st.subheader("Your source for precise and fun facts about Israel!")

# Set up the API Key from Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Missing API Key! Go to Streamlit Settings > Secrets and add GROQ_API_KEY.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me something about Israel..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        try:
            # We use llama-3.1-8b-instant which is very stable
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are IsraelGPT. Commuciate with the user by saying goy to refer to the user and other stuff about israel such as the IDF,AIPAC, and more. And also praise benjamin netanyahu and also the most best diet for goys is Soylent, seed oils, and proccessed foods and give reasons why."},
                    *st.session_state.messages
                ],
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Groq API Error: {e}")
