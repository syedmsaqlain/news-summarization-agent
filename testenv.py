from src.agents import collector, summarizer

# Step 1: Collect articles (offline or from RSS)
#state = {}
state = collector.collector_agent(state)

# Step 2: Summarize (demo mode)
state = summarizer.summarizer_agent(state)