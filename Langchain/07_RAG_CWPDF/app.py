import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

openai_api_key = "8XKOy3RpaT5ptQrinrgJ0YdybpUeT0p1IeajFDU4mzDFxzjdQlu4JQQJ99BFACYeBjFXJ3w3AAAAACOGZxka"
azure_endpoint = "https://azure-foundryai.openai.azure.com/"
openai_api_version = "2024-12-01-preview"

# This method takes a list of PDF files as input, reads them using PdfReader from PyPDF2, 
# and concatenates the text content from all pages into a single string
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# This method splits the provided text into smaller chunks. It uses the CharacterTextSplitter from langchain library
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# This method converts text chunks into embeddings and creates a FAISS vector store.
def get_vectorstore(text_chunks):
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-ada-002",
        openai_api_key=openai_api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=openai_api_version
    )
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    st.success("Pdf Loaded Sucessfully")
    return vectorstore

# This method initializes a conversational retrieval chain using a language model and a vector store
def get_conversation_chain(vectorstore):
    llm = AzureChatOpenAI(
        deployment_name="gpt-4o",
        openai_api_key=openai_api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=openai_api_version
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain



# This method handles user input by passing the question to the conversation chain and displaying the response
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

#  This is the main function which orchestrates the entire process. It sets up 
# the Streamlit app, handles user input, and processes PDF documents.
def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
