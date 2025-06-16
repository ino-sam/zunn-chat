import streamlit as st
from components.chat import chat_component
from components.history import history_component

async def main():
    st.title("ずんだもんbot")
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False

    if "threads" not in st.session_state:
        st.session_state.threads = []

    history_component(st.session_state.threads)

    await chat_component(is_generating=st.session_state.is_generating, threads=st.session_state.threads)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
