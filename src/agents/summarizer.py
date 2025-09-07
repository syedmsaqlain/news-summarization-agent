import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

def summarizer_agent(state: dict, params: dict = None) -> dict:
    """
    Summarizes each article in the state using Gemini LLM.
    Updates each article with 'summary' key.
    Prints a clean briefing with category, title, summary/description, and link.
    """
    demo = False  # <- Enable demo mode to avoid calling Gemini

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or demo:
        print("⚠️ GOOGLE_API_KEY not found in environment, skipping summarization")
        for a in state.get("articles", []):
            a.clear()
            a["summary"] = None
            a["description"]= None
            a["link"]= None
            a["category"]=""
            a["Title"]=""
            a["text"] = a.get("text") or ""
            state["articles"] = []

        return state

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",  # or gemini-1.5-pro
        google_api_key=api_key,
        temperature=0
    )

    #print("=== Today’s Briefing ===\n")

    for a in state.get("articles", []):
        title = a.get("title", "No Title")
        category = a.get("category", "UNCAT")
        text = a.get("text") or ""
        
        # Summarize using LLM if text exists
        if text.strip():
            prompt = f"Summarize this article in 3–4 bullet points:\n\n{text}"
            try:
                result = llm.invoke(prompt)
                a["summary"] = result.content.strip()
            except Exception as e:
                a["summary"] = f"[Summarization failed: {e}]"
        else:
            a["summary"] = "[No text to summarize]"

        # Print the article briefing
        #print(f"[{category}] {title}")
        #if a.get("summary"):
        #    print(f"   📝 Summary:\n{a['summary']}")
        #elif a.get("description"):
        #    print(f"   {a['description']}")
        #if a.get("link"):
        #    print(f"   🔗 {a['link']}\n")

    #print("Done. State keys:", list(state.keys()))
    return state
