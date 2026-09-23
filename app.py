from google import genai
import streamlit as st

st.title("✍️ 6th Grade Social Studies Tutor")
st.write(
    "Hi George! Please let me know what you need help with."
)

# Initialize the Gemini client and store it in session state to prevent client-closed errors
if "client" not in st.session_state:
  if "GEMINI_API_KEY" in st.secrets:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
  else:
    st.error("API key not found in Streamlit secrets.")
    st.stop()

# Initialize chat session with tuned, concise Socratic instructions
if "chat" not in st.session_state:
  st.session_state.chat = st.session_state.client.chats.create(
      model="gemini-2.5-flash",
      config={
          "system_instruction": (
              "You are an enthusiastic and engaging history and social studies tutor for an"
              " 11-year-old 6th-grade student. When he asks about a topic or concept,"
              " first give a short, punchy 2-sentence explanation or historical context."
              " Then, use a fun real-world analogy (like video games, sports, or nature"
              " to make it stick, and ask one quick question to check his understanding."
              " Keep your responses short and punchy so he"
              " stays engaged."
          )
      },
  )

# Render existing chat history
for message in st.session_state.chat.get_history():
  role = "user" if message.role == "user" else "assistant"
  with st.chat_message(role):
    text_content = "".join([part.text for part in message.parts if part.text])
    st.markdown(text_content)

# Handle user input
if prompt := st.chat_input("Type your sentence or question here..."):
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
      response = st.session_state.chat.send_message(prompt)
      st.markdown(response.text)
