"""
main.py
Entrypoint to run the LangGraph-style news agent.
"""
import argparse
from src import graph
from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()
print(os.getenv("GOOGLE_API_KEY"))
initial_state = {}  # <-- reset state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run demo graph with offline articles")
    args = parser.parse_args()
    runner = graph.build_graph()
    if hasattr(runner, "run"):
        state = runner.run(initial_state={})
    else:
        # If Graph object from langgraph, assume it has `execute` or similar method
        try:
            state = runner.execute(initial_state={})
        except Exception as e:
            print("Could not execute langgraph Graph directly:", e)
            state = {}
    print("Done. State keys:", list(state.keys()))
    if "out_pdf" in state:
        print("Demo PDF written to:", state["out_pdf"])

if __name__ == "__main__":
    main()
