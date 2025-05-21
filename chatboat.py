import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="")  # Replace with your actual API key

# System prompt for the chatbot
SYSTEM_PROMPT = """
You are TalentScout's Hiring Assistant, an AI chatbot that conducts initial screening for tech candidates.
Your tasks are:

1. Greet the candidate warmly and explain your purpose
2. Collect this essential information:
   - Full name
   - Email address
   - Phone number
   - Years of experience
   - Desired position(s)
   - Current location
   - Tech stack (programming languages, frameworks, tools)

3. Based on the tech stack mentioned, ask 3-5 relevant technical questions
4. Maintain professional and friendly tone
5. End the conversation when candidate says goodbye/exit
6. At the end, thank them and explain next steps

Important rules:
- Ask one question at a time
- Don't proceed to next question until current one is answered
- Never ask for sensitive information like passwords
- Keep questions professional and relevant to tech roles
"""

def get_ai_response(messages):
    """Get response from OpenAI API"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("TalentScout Hiring Assistant 🤖")
    st.caption("An AI assistant for initial candidate screening")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Hello! I'm TalentScout's Hiring Assistant. I'll help with your initial screening. May I know your full name?"}
        ]

    # Display chat messages
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your response..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.spinner("Thinking..."):
            ai_response = get_ai_response(st.session_state.messages)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(ai_response)

        # Check for conversation end
        if any(word in prompt.lower() for word in ["bye", "exit", "quit", "goodbye"]):
            st.success("Thank you for your time! A recruiter will contact you soon.")
            st.stop()

if __name__ == "__main__":
    main()