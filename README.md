# 🧭 News Summarization Agent — LangGraph Version

This repository is an **agentic** rework of the News Summarization project using a graph-based orchestration approach (LangGraph-style).
It converts the previous pipeline/bot into a set of independent agents (CollectorAgent, FilterAgent, SummarizerAgent, CategorizerAgent, DispatcherAgent)
connected by an explicit graph. Each agent is responsible for one role and the graph controls the flow.

> NOTE: This scaffold includes a lightweight **fallback graph runner** so you can try the agent locally even if `langgraph` isn't installed.

## What you'll find here

- `src/agents/` — agent implementations (collector, filterer, summarizer, categorizer, dispatcher)
- `src/graph.py` — graph definition and runner (uses LangGraph if available; otherwise uses fallback)
- `src/main.py` — entrypoint to invoke the agent (supports `--demo`)
- `demo/sample_output.pdf` — example briefing
- `docs/architecture_diagram.png` — architecture image

## Quick start

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the demo agent (offline sample):
```bash
python src/main.py --demo
```

This will run the agent graph and produce `demo/sample_output.pdf` and print the briefing to console.

## Extending

- Replace demo RSS/articles in `agents/collector.py` with real RSS feeds / NewsAPI calls.
- Swap the simple classifier with a trained model or a cloud-hosted classifier.
- Add branching and retries in `src/graph.py` by modifying edges or adding conditional nodes.
- Integrate Slack/Email by configuring environment variables and implementing the delivery in `agents/dispatcher.py`.

## License
MIT
