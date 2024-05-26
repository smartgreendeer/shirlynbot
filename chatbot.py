import streamlit as st
import os
from dotenv import load_dotenv
import replicate

# Load environment variables from .env file
load_dotenv()

# Retrieve Replicate API token from environment variables
replicate_api = os.getenv('REPLICATE_API_TOKEN')

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')
    st.write('This chatbot is created using the open-source Llama 2 LLM model from Meta.')
    
    if not replicate_api or not replicate_api.startswith('r8_') or len(replicate_api) != 40:
        st.warning('Please set a valid Replicate API token in your .env file!', icon='⚠️')
    else:
        st.success('API key validated!', icon='✅')
        
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    
    temperature = st.sidebar.slider('Temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('Max Length', min_value=32, max_value=128, value=120, step=8)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat history
st.subheader('Chat History')
for message in st.session_state.messages:
    with st.expander(f"{message['role']}: {message['content']}"):
        pass

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Define pre-prompt for Llama model
PRE_PROMPT = "You are a helpful personal assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as a Personal Assistant."

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = ""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    full_prompt = f"{PRE_PROMPT} {string_dialogue} {prompt_input} Assistant: "
    output = replicate.run(llm, 
                           input={"prompt": full_prompt,
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
prompt = st.text_input('Type your message:', key='prompt')
if st.button('Send') and prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        response = generate_llama2_response(prompt)
        full_response = ''
        for item in response:
            full_response += item

        # Display LLaMA2 response
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Define the URL of the Blogging social app
blog_app_url = "https://socialblogapp.netlify.app"

# Add a button to navigate to the Blogging social app
if st.button("Go to Blog App"):
   st.markdown(f"[Go to Blog App]({blog_app_url})")

# Add an Acknowledgment button to navigate back to the Blogging social app
if st.button("Acknowledge", key='ack_button'):
    st.markdown(f"[Go to Blog App]({blog_app_url})")