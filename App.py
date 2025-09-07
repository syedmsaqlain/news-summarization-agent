import streamlit as st
from src import graph

st.title("📰 News Summarization Agent (Full Pipeline)")

runner = graph.build_graph()
state = runner.run(initial_state={})

# Show results from state
if "articles" in state:
    for idx, a in enumerate(state["articles"], start=1):
        cat=a.get('category','No Uncategorized')
        #st.subheader(f"{a.get('category','No Uncategorized')}")
        st.subheader(f"{idx}. [{cat}]{a.get('title','No Title')}")
        st.write(f"🔗 [Read more]({a.get('link','')})")
        st.write("**Summary:**")
        st.write(a.get("summary","[No summary]"))
