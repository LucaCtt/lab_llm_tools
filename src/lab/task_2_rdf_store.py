"""
Task 2: Local RDF Store with rdflib
======================================
Goal: instead of discarding Wikidata results after each query, persist them
into a local RDF graph, then query the local graph with SPARQL.
This simulates a lightweight knowledge base that grows as you ask questions.

You can (in fact, should) use functions from previous tasks and examples.

Instructions
---
1. Complete the two TODO functions: sparql_local(), ask().
2. Run ask() for at least two questions and verify the graph grows.
3. After loading a few questions, run sparql_local() with a hand-written query
   to confirm the data is really stored locally.
"""

from rdflib import Graph


def sparql_local(graph: Graph, query: str) -> list[dict]: ...  # TODO


def ask(question: str, graph: Graph) -> str: ...  # TODO


if __name__ == "__main__":
    g = Graph()
    q1 = "What is the capital of France?"
    q2 = "Who is the president of the United States?"
    print(ask(q1, g))
    print(ask(q2, g))

    g.serialize("local_graph.ttl", format="turtle")
