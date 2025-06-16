import streamlit as st

def history_component(threads):
    st.sidebar.header("会話履歴")
    if st.sidebar.button("新しいチャットを開始"):
        st.session_state.current_thread_id = None
    for thread in threads:
        if st.sidebar.button(thread["title"], key=thread["id"]):
            st.session_state.current_thread_id = thread["id"]
        st.markdown(
            f"""
            <style>
            div[data-testid="stVerticalBlock"] > section > div{{width: 100% !important;}}
            </style>
            """,
            unsafe_allow_html=True,
        )
