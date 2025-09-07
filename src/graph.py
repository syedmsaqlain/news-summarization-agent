"""
graph.py
Defines the agent graph. Uses langgraph if available; otherwise uses a local fallback runner.
Graph flow:
 Collector -> Filter -> Summarizer -> Categorizer -> Dispatcher -> END
"""
try:
    # Attempt to import LangGraph (if installed)
    from langgraph import Graph, Node
    HAS_LANGGRAPH = True
except Exception:
    HAS_LANGGRAPH = False

# Import agents (they are simple functions)
from src.agents import collector as collector_mod
from src.agents import filterer as filterer_mod
from src.agents import summarizer as summarizer_mod
from src.agents import categorizer as categorizer_mod
from src.agents import dispatcher as dispatcher_mod

# Fallback simple runner
class SimpleGraphRunner:
    def __init__(self):
        self.nodes = []
    def add_node(self, fn, name=None, params=None):
        self.nodes.append((name or fn.__name__, fn, params or {}))
    def run(self, initial_state=None):
        state = initial_state or {}
        for name, fn, params in self.nodes:
            print(f"-> Running node: {name}")
            state = fn(state, params)
        return state

def build_graph():
    if HAS_LANGGRAPH:
        # This block is illustrative — API may differ for the real LangGraph package.
        g = Graph()
        g.add_node(Node("collector", collector_mod.collector_agent))
        g.add_node(Node("filter", filterer_mod.filter_agent))
        g.add_node(Node("summarizer", summarizer_mod.summarizer_agent))
        g.add_node(Node("categorizer", categorizer_mod.categorizer_agent))
        g.add_node(Node("dispatcher", dispatcher_mod.dispatcher_agent))
        g.add_edge("collector", "filter")
        g.add_edge("filter", "summarizer")
        g.add_edge("summarizer", "categorizer")
        g.add_edge("categorizer", "dispatcher")
        return g
    else:
        runner = SimpleGraphRunner()
        runner.add_node(collector_mod.collector_agent, name="collector", params={"demo": True})
        runner.add_node(filterer_mod.filter_agent, name="filter", params={"days":7})
        runner.add_node(summarizer_mod.summarizer_agent, name="summarizer", params={})
        runner.add_node(categorizer_mod.categorizer_agent, name="categorizer", params={})
        runner.add_node(dispatcher_mod.dispatcher_agent, name="dispatcher", params={"out_dir":"demo"})
        return runner
