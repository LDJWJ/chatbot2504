import streamlit as st
from openai import OpenAI

# Show an image at the top
st.image("https://raw.githubusercontent.com/LDJWJ/chatbot2504/refs/heads/main/image01.jpg", use_column_width=True)


# Show title and description.
st.title("✍️ 창작 지원 챗봇")
st.write(
    "이 챗봇은 작가, 아티스트, 음악가를 위해 설계되었습니다. 아이디어 제안, 글쓰기 프롬프트, 스토리 전개 조언 등을 제공합니다. "
    "예: '판타지 소설 시작을 어떻게 할까?' 같은 질문을 해보세요. "
    "사용하려면 OpenAI API 키가 필요합니다. [여기](https://platform.openai.com/account/api-keys)에서 얻을 수 있습니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력해 주세요.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "당신은 창작을 돕는 AI입니다. 작가, 아티스트, 음악가를 위해 아이디어를 제안하고, 글쓰기 프롬프트나 스토리 전개 조언을 제공하세요. 창의적이고 구체적인 답변을 주되, 사용자의 입력에 맞춰 영감을 불어넣는 역할을 합니다."}
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        if message["role"] != "system":  # 시스템 메시지는 표시하지 않음
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Create a chat input field with a custom placeholder.
    if prompt := st.chat_input("창작에 대해 물어보세요 (예: '판타지 소설의 시작을 어떻게 할까?')"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat and store it in session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
