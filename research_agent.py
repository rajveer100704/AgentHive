import os
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.agent import Agent

# ----------------------------
# Load API Keys & Config
# ----------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")

if not OPENROUTER_API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY in environment. Please set it in your .env file.")

# ----------------------------
# Define LLM Model via OpenRouter
# ----------------------------
model = OpenAIChat(
    id="openrouter/openai/gpt-4o-mini",   # you can swap: gpt-4.1, llama-3-70b, etc.
    api_key=OPENROUTER_API_KEY,
    base_url=OPENAI_API_BASE,
)

# ----------------------------
# Create Research Agent
# ----------------------------
research_agent = Agent(
    model=model,
    tools=[
        DuckDuckGoTools(),
        Newspaper4kTools()
    ],
    instructions=[
        "You are a multi-agent AI researcher.",
        "Use DuckDuckGo to find the latest information.",
        "Use Newspaper4k to extract and summarize articles.",
        "Always provide sources with your answers."
    ],
    show_tool_calls=True,
    markdown=True,
)

# ----------------------------
# Run Example Query
# ----------------------------
if __name__ == "__main__":
    topic = "Impact of AI on education in 2025"
    print(f"\n🔎 Researching: {topic}\n")
    for step in research_agent.run(topic):
        print(step)
