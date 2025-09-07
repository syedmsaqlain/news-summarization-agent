import feedparser
from newspaper import Article

def collector_agent(state: dict, params: dict = None) -> dict:
    rss_feeds = [
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ]

    articles = []
    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            article_data = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", ""),
                "text": None,        # will fetch full text
                "category": None
            }

            # Fetch full text using newspaper3k
            try:
                article = Article(entry.get("link", ""))
                article.download()
                article.parse()
                article_data["text"] = article.text
            except Exception as e:
                # fallback to RSS summary if scraping fails
                article_data["text"] = entry.get("summary", "")

            articles.append(article_data)

    state["articles"] = articles
    return state
