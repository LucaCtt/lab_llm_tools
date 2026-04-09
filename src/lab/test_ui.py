import streamlit as st
import litellm
from lab.settings import Settings

# Initialize settings
settings = Settings()
if not settings.litellm_api_key:
    st.error("Set LITELLM_API_KEY to your LiteLLM master key or user key.")
    st.stop()

litellm.api_base = settings.litellm_base_url
litellm.api_key = settings.litellm_api_key

st.title("Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display chat history (skipping system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Call LiteLLM with streaming
        response = litellm.completion(
            model=settings.model,
            messages=st.session_state.messages,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            top_p=settings.top_p,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": False}
            },
            stream=settings.stream
        )
         # If streaming is disabled, the response will be a ModelResponse object. 
        if isinstance(response, litellm.ModelResponse):
            content = response.choices[0].message.content or ""
            full_response += content
            response_placeholder.markdown(full_response)
        else:
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})