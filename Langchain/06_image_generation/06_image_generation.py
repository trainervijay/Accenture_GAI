import os
import requests
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

# To run this code, ensure you have the required packages installed:
# pip install streamlit openai python-dotenv requests
# after installing, run the app with: 
# streamlit run 06_image_generation.py

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key="1thBoA2daB7fncFl4TDzAi7mr9IMcLwdoEMvZDC8ZiaWVO8aBs59JQQJ99BFACfhMk5XJ3w3AAAAACOGkZfw",
    api_version="2024-02-01",
    azure_endpoint="https://vijay-mcijm3q9-swedencentral.openai.azure.com/",
)

# CAD-focused system message for prompt enrichment
system_description = (
    "You are an AI-powered image assistant that generates images"
)

# Function to generate image
def generate_image(prompt):
    full_prompt = f"{system_description}\nPrompt: {prompt}"
    response = client.images.generate(
        model="dall-e-3",
        prompt=full_prompt,
        n=1
    )
    return response.data[0].url

# Streamlit UI
st.set_page_config(page_title="Image Assistant", layout="centered")
st.title("🛠️ AI-Powered Image Generator")

st.markdown("Enter a prompt like:")
st.markdown(
    "- **'Design a futuristic cityscape with flying cars'**\n"
    "- **'Create a blueprint for a modern eco-friendly house'**\n"
)

prompt_input = st.text_input("Image Prompt", placeholder="Describe your image...")

col1, col2 = st.columns([1, 1])
generate_clicked = col1.button("Generate")
clear_clicked = col2.button("Clear")

if generate_clicked and prompt_input.strip():
    with st.spinner("Generating image..."):
        try:
            image_url = generate_image(prompt_input)
            st.image(image_url, caption="Generated Image")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

if clear_clicked:
    st.experimental_rerun()