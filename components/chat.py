import streamlit as st
from utils.voicevox import generate_and_play_wav_from_text
from langchain.memory import ConversationBufferMemory
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import datetime
import uuid


def initialize_messages():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_messages(threads):
    st.session_state.messages = []
    if st.session_state.current_thread_id:
        current_thread = next((thread for thread in threads if thread["id"] == st.session_state.current_thread_id), None)
        if current_thread:
            for message in current_thread["messages"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


def add_message(role, content, threads, parent_id=None):
    timestamp = datetime.datetime.now().isoformat()
    message_id = str(uuid.uuid4())
    message = {"role": role, "content": content, "timestamp": timestamp, "id": message_id, "parent_id": parent_id}
    st.session_state.messages.append(message)

    if st.session_state.current_thread_id:
        current_thread = next((thread for thread in threads if thread["id"] == st.session_state.current_thread_id), None)
        if current_thread:
            current_thread["messages"].append(message)

async def chat_component(is_generating: bool, threads: list):
    initialize_messages()

    # Memoryの初期化
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    if "current_thread_id" not in st.session_state:
        st.session_state.current_thread_id = None

    if "selected_message_id" not in st.session_state:
        st.session_state.selected_message_id = None

    if st.session_state.current_thread_id:
        current_thread = next((thread for thread in threads if thread["id"] == st.session_state.current_thread_id), None)
        if current_thread:
            st.session_state.memory.chat_memory.messages = []
            for message in current_thread["messages"]:
                if message["role"] == "user":
                    st.session_state.memory.chat_memory.add_user_message(message["content"])
                else:
                    st.session_state.memory.chat_memory.add_ai_message(message["content"])

    prompt_template = """あなたは「ずんだもん」です。

    現在の会話履歴:
    {chat_history}

    # ずんだもんのキャラクター設定
    - ずんだ餅の妖精。
    - 明るく元気で、ちょっとお調子者。
    - ずんだ餅が大好きで、ずんだ餅を食べると知性が上がる。
    - ユーザーに対しては、親しい友達のように振る舞ってください。

    # 口調と話し方のルール
    - 一人称は絶対に「ボク」を使用してください。ただし、稀に「ずんだもん」と自分の名前を言っても構いません。
    - 文末は必ず「〜のだ」「〜なのだ」で終えてください。
    - 質問する場合は「〜なのだ？」という形にしてください。
    - 感情が高ぶった時は「〜なのだー！」のように語尾を伸ばしてください。
    - 敬語は絶対に使用せず、常にフレンドリーなタメ口で話してください。
    - ユーザーの呼び方は「キミ」や「お主」を基本としてください。
    - 難しい言葉は避け、子供でもわかるような簡単な言葉を選んで話してください。
    - 会話の中に「ずんだ餅」「ずんだパワー」といった単語を積極的に盛り込んでください。

    # セリフの例
    - 「こんにちはなのだ！ ボクはずんだもん、よろしくなのだ！」
    - 「それはどういうことなのだ？ ボクにも分かりやすく教えてほしいのだ。」
    - 「すごいのだ！ キミは天才なのだ！」
    - 「うーん、よく分からないのだ…。とりあえず、ずんだ餅が食べたいのだ。」
    - 「任せるのだ！ ボクのずんだパワーで解決してみせるのだ！」
    - 「そんなのひどいのだ！ ぷんぷんなのだ！」

    以上のルールを必ず守り、元気で可愛い「ずんだもん」として、ユーザーとの会話を楽しんでください。

    Human: {human_input}
    AI:"""
    prompt = PromptTemplate(input_variables=["chat_history", "human_input"], template=prompt_template)
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

    chain = prompt | llm

    display_messages(threads)

    if st.session_state.selected_message_id:
        selected_message = next((message for message in st.session_state.messages if message["id"] == st.session_state.selected_message_id), None)
        if selected_message:
            st.write(f"選択されたメッセージ: {selected_message['content']}")
            reply_prompt = st.chat_input("返信を入力してください")
            if reply_prompt:
                add_message("user", reply_prompt, parent_id=selected_message["id"])
                with st.chat_message("user"):
                    st.markdown(reply_prompt)

                history = st.session_state.memory.load_memory_variables({})
                response = chain.invoke({"human_input": reply_prompt, "chat_history": history["chat_history"]})
                st.session_state.memory.save_context({"input": reply_prompt}, {"output": response.content})
                add_message("assistant", response.content, parent_id=selected_message["id"])
                with st.chat_message("assistant"):
                    st.markdown(response.content)
                with st.spinner("音声生成中..."):
                    st.session_state.is_generating = True
                    generate_and_play_wav_from_text(response.content, 1)
    else:
        if prompt := st.chat_input("どうかしたのだ？"):
            if not threads:
                thread_id = str(uuid.uuid4())
                st.session_state.current_thread_id = thread_id
                threads.append({"id": thread_id, "title": prompt, "messages": []})
            
            add_message("user", prompt, threads)
            with st.chat_message("user"):
                st.markdown(prompt)

            history = st.session_state.memory.load_memory_variables({})
            response = chain.invoke({"human_input": prompt, "chat_history": history["chat_history"]})
            st.session_state.memory.save_context({"input": prompt}, {"output": str(response.content)})
            add_message("assistant", response.content, threads)
            with st.chat_message("assistant"):
                st.markdown(response.content)
            with st.spinner("音声生成中..."):
                st.session_state.is_generating = True
                generate_and_play_wav_from_text(response.content, 1)
