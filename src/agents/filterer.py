import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text

def filter_agent(state: dict, params: dict = None) -> dict:
    articles = state.get("articles", [])
    seen = set()
    filtered = []

    for a in articles:
        title = clean_text(a.get("title", ""))
        link = a.get("link")
        summary = clean_text(a.get("summary", ""))

        # Deduplication
        key = link or title.lower()
        if key in seen:
            continue
        seen.add(key)

        # Skip too-short titles
        if len(title.split()) < 3:
            continue

        filtered.append({
            "title": title,
            "link": link,
            "summary": summary if summary else None,
            "text": a.get("text"),
            "category": a.get("category")
        })

    state["articles"] = filtered
    return state
