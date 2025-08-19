# 📰 Multi-Agent AI Researcher

    A **Streamlit-powered AI application** that leverages a team of specialized agents to research **top HackerNews stories** and generate insightful summaries, reports, and     blog-style content.  
    This project demonstrates **multi-agent collaboration**, **LLM orchestration**, and **real-world data integration** — making it production-ready and portfolio-worthy.

---

## 🚀 Overview

    The Multi-Agent AI Researcher is built to simulate a research assistant team.  
    Instead of relying on a single LLM, it coordinates multiple AI agents — each with a specialized role:

     - 🔍 **HackerNews Researcher** → Fetches top stories and user details using HackerNews API.  
     - 🌐 **Web Searcher** → Enriches context with external web search (DuckDuckGo).  
     - 📖 **Article Reader** → Extracts clean article content using  'newspaper4k`.  

These agents collaborate under a **HackerNews Team Orchestrator** to deliver structured research output, including titles, summaries, and reference links.

---

## ✨ Features

    - Research trending **HackerNews stories** and top users.  
    - AI-driven **article summarization** with contextual enrichment.  
    - Generates **blog posts, research reports, and social media drafts**.  
    - Built with **OpenRouter / OpenAI GPT-4o** for advanced reasoning.  
    - Lightweight, interactive **Streamlit UI** for seamless use.  

---

## 🛠️ Tech Stack

    - **Frontend/UI** → [Streamlit](https://streamlit.io/)  
    - **Agents & LLM Orchestration** → OpenRouter / OpenAI GPT-4o  
    - **APIs** → HackerNews API, DuckDuckGo Search  
    - **Content Extraction** → newspaper4k  
    - **Python Libraries** → 'requests`, `beautifulsoup4`, `langchain`, etc.  

---

## ⚙️ Setup

    1. **Clone this repository**:
        git clone https://github.com/rajveer100704/AgentHive.git
        cd AgentHive
    
    2. **Install the dependencies**:
        pip install -r requirements.txt

        
    3.**Get your OpenAI API Key**:
        Sign up for an OpenAI account (or the LLM provider of your choice) and obtain your API key.

    4.** Run the Streamlit App**
        streamlit run research_agent.py

##⚙️ How It Works
        
    Upon running the app, you will be prompted to enter your OpenAI API key. This key is used to authenticate and access the OpenAI language models.

    Once you provide a valid API key, three specialized AI agents are created:

       HackerNews Researcher: Specializes in getting top stories from HackerNews using the HackerNews API.
       Web Searcher: Searches the web for additional information on topics using DuckDuckGo search.
       Article Reader: Reads and extracts content from article URLs using newspaper4k tools.
       These agents work together as a coordinated team under the HackerNews Team which orchestrates the research process.

    Enter your research query in the provided text input field. This could be a topic, keyword, or specific question related to HackerNews stories or users.

    The HackerNews Team follows a structured workflow:

      1.First searches HackerNews for relevant stories based on your query
      2.Uses the Article Reader to extract detailed content from the story URLs
      3.Leverages the Web Searcher to gather additional context and information
      4.Finally provides a thoughtful and engaging summary with title, summary, and reference links
      5.The generated content is structured as an Article with a title, summary, and reference links for easy review and use.

       

