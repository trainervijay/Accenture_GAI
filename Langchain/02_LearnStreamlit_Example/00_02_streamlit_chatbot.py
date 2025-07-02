import streamlit as st

st.set_page_config(
    page_title="Accenture Chatbot",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state='expanded',
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None

st.markdown("<h1 style='text-align: centered;'>Accenture Chatbot😬</h1>", unsafe_allow_html=True)

user_input = st.text_area("Enter a prompt:", key="user_input", placeholder="Enter a prompt", label_visibility="hidden")

new = st.sidebar.button('➕&nbsp;&nbsp;&nbsp;New chat')

if new:
    if st.session_state.current_conversation is not None:
        first_prompt = st.session_state.current_conversation[0]
        if first_prompt not in st.session_state.chat_history:
            st.session_state.chat_history[first_prompt] = []
            if st.session_state.current_conversation[1:]:
                st.session_state.chat_history[first_prompt].extend(
                    st.session_state.current_conversation[1:]
                )

    st.session_state.current_conversation = [user_input]

if st.button("Send &nbsp;➤"):
    if st.session_state.current_conversation is None:
        st.session_state.current_conversation = []

    st.session_state.current_conversation.append(user_input)

st.sidebar.title("Chat History")

selected_conversation = st.sidebar.selectbox("Select Conversation", list(st.session_state.chat_history.keys()))

if selected_conversation:
    conversation_card = st.sidebar.expander(f"Conversation: {selected_conversation}", expanded=False)
    
    delete_button = conversation_card.button("🗑 Delete")
    
    if delete_button:
        if selected_conversation in st.session_state.chat_history:
            del st.session_state.chat_history[selected_conversation]
    
    with conversation_card:
        for message in st.session_state.chat_history.get(selected_conversation, []):
            st.text(message)
else:
    st.sidebar.text("No conversation selected.")

if st.session_state.current_conversation and not new:
    first_prompt = st.session_state.current_conversation[0]
    conversation_card = st.sidebar.expander(f"New Conversation: {first_prompt}", expanded=False)
    with conversation_card:
        for message in st.session_state.current_conversation[1:]:
            st.text(message)
    if selected_conversation:
        st.markdown(f"### Inputs for Conversation: {selected_conversation}")
        for message in st.session_state.chat_history.get(selected_conversation, []):
            st.text(message)


if st.sidebar.button("Clear Chat History", type="primary"):
    st.session_state.chat_history.clear()
    st.session_state.current_conversation = None