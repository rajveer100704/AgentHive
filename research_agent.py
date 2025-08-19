# app.py
# Multi-Agent AI Researcher (Streamlit + agno)
# Supports OpenRouter or OpenAI via sidebar settings

import os
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools

# ---------- App & state setup ----------
st.set_page_config(page_title="Multi-Agent AI Researcher", page_icon="🤖", layout="wide")
st.title("Multi-Agent AI Researcher 🔍🤖")
st.caption("Research top stories & context, then produce concise summaries/reports.")

# Load .env once (if present)
load_dotenv(override=False)

# ---------- Sidebar: provider & credentials ----------
with st.sidebar:
    st.subheader("⚙️ Model & API Settings")

    provider = st.radio(
        "Provider",
        options=["OpenRouter (recommended)", "OpenAI"],
        index=0,
        help="OpenRouter is OpenAI-compatible and often cheaper. Uses your OpenRouter key.",
    )

    default_base = (
        "https://openrouter.ai/api/v1" if provider.startswith("OpenRouter") else "https://api.openai.com/v1"
    )

    # Read any pre-existing keys from env/session for convenience
    if "OPENAI_API_KEY" not in st.session_state:
        st.session_state.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    api_key = st.text_input(
        "API Key",
        value=st.session_state.OPENAI_API_KEY,
        type="password",
        placeholder="sk-...",
        help="Use an OpenRouter key (sk-or-...) or OpenAI key (sk-...).",
    )

    base_url = st.text_input(
        "Base URL",
        value=os.getenv("OPENAI_API_BASE", default_base),
        help="For OpenRouter use https://openrouter.ai/api/v1. For OpenAI use https://api.openai.com/v1.",
    )

    model_id = st.selectbox(
        "Model",
        options=[
            # Good defaults; you can change/add more
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1-mini",
            "gpt-4.1",
        ],
        index=0,
    )

    st.divider()
    st.subheader("🧪 Options")
    show_debug = st.toggle("Show tool calls & member responses", value=True)
    add_datetime = st.toggle("Add datetime to Web Search instructions", value=True)

    st.divider()
    st.markdown(
        "🔐 **Never commit your real keys.** Keep them in `.env` locally or in repository secrets in CI/CD."
    )

# Persist to session & environment for agno/OpenAI client discovery
def _set_env(key: str, value: Optional[str]):
    if value:
        os.environ[key] = value
        st.session_state[key] = value

_set_env("OPENAI_API_KEY", api_key)
_set_env("OPENAI_API_BASE", base_url)

# Quick helper to build the model (OpenAI-compatible)
def build_model():
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("No API key found. Please enter it in the sidebar.")
    return OpenAIChat(
        id=model_id,                 # agno uses `id` for model name
        base_url=os.getenv("OPENAI_API_BASE") or default_base,
        api_key=os.getenv("OPENAI_API_KEY"),
        # You can set extra params if you like:
        # temperature=0.3,
        # max_tokens=2000,
    )

# ---------- Agents & Team ----------
def build_team():
    model = build_model()

    hn_researcher = Agent(
        name="HackerNews Researcher",
        model=model,
        role="Gets top stories & threads from Hacker News relevant to the user's topic.",
        tools=[HackerNewsTools()],
    )

    web_searcher = Agent(
        name="Web Searcher",
        model=model,
        role="Searches the web for corroborating info and recent context.",
        tools=[DuckDuckGoTools()],
        add_datetime_to_instructions=add_datetime,
    )

    article_reader = Agent(
        name="Article Reader",
        model=model,
        role="Reads and extracts key points from supplied URLs.",
        tools=[Newspaper4kTools()],
    )

    team = Team(
        name="Research Team",
        mode="coordinate",
        model=model,  # coordinator model
        members=[hn_researcher, web_searcher, article_reader],
        instructions=[
            "1) Search Hacker News for items relevant to the user's query.",
            "2) For any promising items, provide the Article Reader with the URLs to extract details.",
            "3) Use Web Searcher to find additional sources & context around each item.",
            "4) Cross-check facts when possible; avoid redundancy.",
            "5) Produce a concise, engaging report with links & bullet points.",
        ],
        show_tool_calls=show_debug,
        show_members_responses=show_debug,
        markdown=True,
        debug_mode=show_debug,
    )
    return team

# ---------- Main UI ----------
st.subheader("📝 Enter your research query")
query = st.text_input("What do you want to research?", placeholder="e.g., Impact of open-source LLMs on education in 2025")

col_run, col_clear = st.columns([1, 1], vertical_alignment="center")
with col_clear:
    if st.button("Clear Output"):
        st.session_state.pop("last_response", None)
        st.session_state.pop("last_error", None)
        st.toast("Cleared.")

with col_run:
    run_clicked = st.button("Run Research", type="primary", disabled=not bool(query))

# Display saved output/errors between reruns
if "last_error" in st.session_state and st.session_state.last_error:
    st.error(st.session_state.last_error)

if "last_response" in st.session_state and st.session_state.last_response:
    st.markdown(st.session_state.last_response)

# ---------- Execution ----------
if run_clicked:
    st.session_state.last_error = None
    st.session_state.last_response = None

    try:
        team = build_team()
        with st.spinner("Coordinating agents…"):
            # `stream=False` keeps things simple/robust across agno versions
            response = team.run(query, stream=False)
        content = getattr(response, "content", None) or str(response)
        st.session_state.last_response = content
        st.markdown(content)
        st.toast("Done!", icon="✅")

    except Exception as e:
        # Helpful error guidance for the two most common issues
        msg = str(e)
        if "Incorrect API key provided" in msg or "No API key" in msg:
            msg = (
                "API key error. If you're using **OpenRouter**, ensure:\n"
                "- Your key starts with `sk-or-`\n"
                "- Base URL is `https://openrouter.ai/api/v1`\n\n"
                "If you're using **OpenAI**, remove the OpenRouter base URL and use an OpenAI key (`sk-...`)."
            )
        st.session_state.last_error = f"❌ Error: {msg}"
        st.error(st.session_state.last_error)

# ---------- Footer ----------
st.divider()
st.caption(
    "Tip: You can prefill keys in a local `.env` file:\n\n"
    "```\nOPENAI_API_KEY=sk-or-...   # or OpenAI sk-...\nOPENAI_API_BASE=https://openrouter.ai/api/v1\n```\n"
    "Keys entered in the sidebar override `.env` for this session."
)
