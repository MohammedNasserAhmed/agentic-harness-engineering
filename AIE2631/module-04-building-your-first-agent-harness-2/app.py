"""A simple local UI for the refund-flow tutorial agent."""

import os
import sys
import logging
from pathlib import Path
from uuid import uuid4

import streamlit as st
from langchain.messages import HumanMessage

from ui_helpers import friendly_tool_steps


PROJECT_ROOT = Path(__file__).resolve().parent
AGENT_DIRECTORY = PROJECT_ROOT / "agent"
ROBOT_IMAGE = PROJECT_ROOT / "assets" / "refund-robot.png"
if str(AGENT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(AGENT_DIRECTORY))

from agent import agent  # noqa: E402
from data import users_data  # noqa: E402


st.set_page_config(page_title="Refund System", page_icon="💬", layout="wide")

st.markdown(
    """
    <style>
      :root { color-scheme: light; }
      .stApp { background: #f7f6f2; color: #292724; }
      .block-container { max-width: 860px; padding: 3.25rem 2.25rem 8rem; }
      .stApp, .stApp p, .stApp span, .stApp div, .stApp label { color: #292724; }
      [data-testid="stSidebar"] { background: #eeece5; border-left: 1px solid #dcd8cd; }
      [data-testid="stSidebar"] * { color: #292724 !important; }
      [data-testid="stSidebar"] .stCaption { color: #625e56 !important; line-height: 1.55; }
      [data-testid="stSidebar"] code { background: #ddd9cf !important; border-radius: 5px; color: #292724 !important; padding: .12rem .3rem; }
      [data-testid="stSidebar"] details { background: #f7f6f2 !important; border: 1px solid #d3cec3 !important; border-radius: 10px; }
      [data-testid="stSidebar"] summary { background: #f7f6f2 !important; color: #292724 !important; }
      [data-testid="stSidebar"] [data-testid="stExpanderDetails"] { background: #f7f6f2 !important; }
      [data-testid="stSidebar"] [data-testid="stExpanderDetails"] p { color: #292724 !important; }
      .activity-step { align-items: center; background: #0b3d2e; border-radius: 11px; color: #fffdf7 !important; display: flex; font-size: 1rem; gap: .65rem; line-height: 1.45; margin: .4rem 0; padding: .85rem .95rem; }
      .activity-step span { color: #fffdf7 !important; }
      .activity-check { color: #9df0bf !important; font-size: 1.15rem; font-weight: 700; }
      [data-testid="stSidebar"] .stButton > button { background: #292724 !important; border: 1px solid #292724 !important; color: #fffdf7 !important; }
      [data-testid="stSidebar"] .stButton > button * { color: #fffdf7 !important; }
      [data-testid="stSidebar"] .stButton > button:hover { background: #d96d45 !important; border-color: #d96d45 !important; }
      [data-testid="stChatMessage"] { background: transparent; border: 0; border-radius: 0; padding: .75rem 0; gap: .85rem; }
      [data-testid="stChatMessage"] p { color: #292724 !important; font-size: 1rem; line-height: 1.65; }
      [data-testid="stChatMessageAvatarUser"] { background: #292724 !important; }
      [data-testid="stChatMessageAvatarAssistant"] { background: #d96d45 !important; }
      [data-testid="stChatInput"] { background: #292724 !important; border: 1px solid #292724 !important; border-radius: 18px !important; box-shadow: 0 7px 24px rgba(47, 43, 37, .14); padding: .3rem .45rem .3rem .8rem; }
      [data-testid="stChatInput"]:focus-within { border-color: #d96d45 !important; box-shadow: 0 0 0 3px rgba(217, 109, 69, .20); }
      [data-testid="stChatInput"] textarea, [data-testid="stChatInput"] [contenteditable="true"] { background: transparent !important; color: #fffdf7 !important; caret-color: #fffdf7 !important; font-size: 1rem; line-height: 1.5; padding: .65rem .3rem; }
      [data-testid="stChatInput"] textarea::placeholder { color: #cfc9bd !important; opacity: 1; }
      [data-testid="stChatInput"] button { background: #d96d45 !important; border-radius: 11px !important; color: #ffffff !important; height: 2.35rem; width: 2.35rem; }
      [data-testid="stChatInput"] button:hover { background: #ee8058 !important; }
      [data-testid="stChatInput"] button svg { fill: #ffffff !important; }
      .brand { color: #d96d45 !important; font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
      .hero { border-bottom: 1px solid #dcd8cd; margin-bottom: 1.6rem; padding-bottom: 1.25rem; }
      .system-name { color: #292724 !important; font-family: Georgia, 'Times New Roman', serif; font-size: clamp(2.35rem, 5vw, 3.7rem); font-weight: 400; letter-spacing: -.045em; line-height: 1.04; margin: .35rem 0 .8rem; }
      .robot-wrap img { max-height: 150px; object-fit: contain; }
      .helper { color: #625e56 !important; font-size: 1rem; line-height: 1.55; max-width: 42rem; }
      .final-status { border: 1px solid #d8b19e; border-radius: 12px; background: #fbefe9; padding: .9rem 1rem; color: #5b321f !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def reset_conversation() -> None:
    st.session_state.thread_id = str(uuid4())
    st.session_state.messages = []
    st.session_state.activity = []
    st.session_state.complete = False


if "thread_id" not in st.session_state:
    reset_conversation()


st.markdown('<div class="hero">', unsafe_allow_html=True)
hero_copy, hero_art = st.columns([3, 1], vertical_alignment="center")
with hero_copy:
    st.markdown(
        '<div class="brand">Customer support agent</div>', unsafe_allow_html=True
    )
    st.markdown('<div class="system-name">REFUND SYSTEM</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="helper">Describe what you would like refunded.</div>',
        unsafe_allow_html=True,
    )
with hero_art:
    st.markdown('<div class="robot-wrap">', unsafe_allow_html=True)
    st.image(ROBOT_IMAGE, width=170)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("What the agent checked")
    if st.session_state.activity:
        for step in st.session_state.activity:
            st.markdown(
                f'<div class="activity-step"><span class="activity-check">✓</span><span>{step}</span></div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("Steps will appear here while your request is reviewed.")

    st.divider()
    st.subheader("Try the tutorial data")
    st.caption(
        "Use a real username and item, for example: `customer201` and `laptop_stand`."
    )
    with st.expander("Available customers"):
        for username, purchases in users_data.items():
            st.markdown(f"**{username}** — {', '.join(purchases)}")

    if st.button("New refund request", use_container_width=True):
        reset_conversation()
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.complete:
    st.markdown(
        '<div class="final-status">This refund request is complete. Start a new request to continue.</div>',
        unsafe_allow_html=True,
    )
    st.chat_input("This refund request is complete", disabled=True)
elif prompt := st.chat_input("Describe the item you would like refunded"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Reviewing your refund request..."):
            try:
                response = agent.invoke(
                    {"messages": HumanMessage(content=prompt)},
                    config={"configurable": {"thread_id": st.session_state.thread_id}},
                )
                structured_response = response["structured_response"]
                answer = structured_response.answer
                for step in friendly_tool_steps(response["messages"]):
                    if step not in st.session_state.activity:
                        st.session_state.activity.append(step)
                st.session_state.complete = not structured_response.conversation
            except Exception:
                logging.exception("Refund agent invocation failed")
                if not os.getenv("OPENAI_API_KEY"):
                    answer = "I could not start the refund agent. Add OPENAI_API_KEY to your local .env file and restart the app."
                else:
                    answer = "I could not review that request right now. Please check the local agent configuration and try again."

        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
