from utils.pdf_writer import write_pdf_reportlab



def dispatcher_agent(state: dict, params: dict = None) -> dict:
    articles = state.get("articles", [])

    print("\n=== Today’s Briefing ===\n")
    for a in articles:
        print(f"[{a.get('category','uncategorized').upper()}] {a.get('title')}")
        if a.get("summary"):
            print(f"   {a['summary']}")
        if a.get("link"):
            print(f"   🔗 {a['link']}")
        print("")

    # Later: can also write to PDF/Notion/Slack
    write_pdf_reportlab(articles, output_path="demo/news_summary.pdf")
    return state
