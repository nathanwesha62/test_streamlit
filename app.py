import streamlit as st
import requests

# Constants (replace with your actual API key and channel token)
API_KEY_question_generator = "5rblfHfn.IkKVUJZy4shYcAYNVMLEHlMR5woR3kal"
API_KEY_answer_eval = "0ldh7pzP.ThAVGtU3QHgVwdStzZCGkD54SnPSUisK"
QUESTION_ENDPOINT_generator = "https://payload.vextapp.com/hook/3U7LL8D63P/catch/$(channel_token)"
QUESTION_ENDPOINT_eval = "https://payload.vextapp.com/hook/1FK8L012RF/catch/$(channel_token)"

# Streamlit App
st.set_page_config(page_title="UPSC Question Generator", layout="centered")
st.title("Insert your favourite UPSC topic, and I will give you a question.")

# Step 1: Get topic input from user
if "question" not in st.session_state:
    topic = st.text_input("Enter your UPSC topic")
    if st.button("Send") and topic:
        # Call first API to get question
        payload = {
            "payload": f"UPSC mains questions on {topic}",
            "env": "dev"
        }
        headers = {
            "Content-Type": "application/json",
            "Apikey": f"Api-Key {API_KEY_question_generator}"
        }

        response = requests.post(QUESTION_ENDPOINT_generator, json=payload, headers=headers)

        if response.status_code == 200:
            question_text = response.text.strip()
            st.session_state.question = question_text
            st.experimental_rerun()
        else:
            st.error("Failed to fetch question. Please try again.")

# Step 2: Show question and collect user's answer
else:
    st.subheader("Your Question")
    st.write(st.session_state.question)

    user_answer = st.text_area("Write your answer below:", height=200)

    if st.button("Submit Answer") and user_answer:
        payload = {
            "payload": user_answer,
            "env": "dev",
            "custom_variables": {"question": st.session_state.question}
        }
        headers = {
            "Content-Type": "application/json",
            "Apikey": f"Api-Key {API_KEY_answer_eval}"
        }

        response = requests.post(QUESTION_ENDPOINT_eval, json=payload, headers=headers)

        if response.status_code == 200:
            st.subheader("Feedback:")
            st.write(response.text.strip())
        else:
            st.error("Failed to evaluate your answer. Please try again.")
