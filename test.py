import streamlit as st
import deeplearningbot_main
from llm_bot import get_answers
from chatterbot_main import get_Response



st.title("RentalCar Assistant")


tab_selection = st.selectbox("Choose Chatbot type",["NN-Bot", "ChatterBot","LLM-bot"])

if tab_selection=="NN-Bot":
        
    
    
# Initialize chat history
    INITIAL_MESSAGE = [
        {"role": "user", "content": "Hi!"},
        {
            "role": "assistant",
            "content": "Hey there, I'm RENTAL BOT, your car rental booking guide! 🚗🔍",
        },
        
        ]

    if "messages" not in st.session_state:
        st.session_state['messages'] = INITIAL_MESSAGE



    with open("ui\sidebar.md", "r") as sidebar_file:
        sidebar_content = sidebar_file.read()

    with open("ui\styles.md", "r") as styles_file:
        styles_content = styles_file.read()
    st.sidebar.markdown(sidebar_content)
    if st.sidebar.button("Reset Chat"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["messages"] = INITIAL_MESSAGE
    st.write(styles_content, unsafe_allow_html=True)

# Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        reply =deeplearningbot_main.chat(prompt)
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

if tab_selection=="ChatterBot":

    
# Initialize chat history
    INITIAL_MESSAGE = [
        {"role": "user", "content": "Hi!"},
        {
            "role": "assistant",
            "content": "Hey there, I'm RENTAL BOT, your car rental booking guide! 🚗🔍",
        },
        
        ]

    if "messages" not in st.session_state:
        st.session_state['messages'] = INITIAL_MESSAGE

    with open("ui\sidebar.md", "r") as sidebar_file:
        sidebar_content = sidebar_file.read()

    with open("ui\styles.md", "r") as styles_file:
        styles_content = styles_file.read()
    st.sidebar.markdown(sidebar_content)
    if st.sidebar.button("Reset Chat"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["messages"] = INITIAL_MESSAGE
    st.write(styles_content, unsafe_allow_html=True)
    

# Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type any rental query here?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        reply =get_Response(prompt)
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})


if tab_selection=="LLM-bot":

    
# Initialize chat history
    INITIAL_MESSAGE = [
        {"role": "user", "content": "Hi!"},
        {
            "role": "assistant",
            "content": "Hey there, I'm RENTAL BOT, your car rental booking guide! 🚗🔍",
        },
        
        ]

    if "messages" not in st.session_state:
        st.session_state['messages'] = INITIAL_MESSAGE

    with open("ui\sidebar.md", "r") as sidebar_file:
        sidebar_content = sidebar_file.read()

    with open("ui\styles.md", "r") as styles_file:
        styles_content = styles_file.read()
    st.sidebar.markdown(sidebar_content)
    if st.sidebar.button("Reset Chat"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state["messages"] = INITIAL_MESSAGE
    st.write(styles_content, unsafe_allow_html=True)
    

# Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type any rental query here?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        reply =get_answers(prompt)
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})





