"""
Task 3: Hybrid Retrieval over RDF store
================================
Goal: implement three different retrieval strategies over the local rdflib
graph built in Task 2, then compare their outputs for the same question.

Retrieval strategies
---
A) SPARQL retrieval: precise, structured, requires well-formed query
B) Text retrieval: keyword/regex match over literal values (FILTER + REGEX)
C) Embedding retrieval: semantic similarity between question and stored labels

Instructions
---
1. Load the RDF graph you built in Task 2.
2. Complete retrieve_sparql(), retrieve_text(), retrieve_embedding().
3. Run compare() for at least two questions and note differences.

Note: Make sure to include clear docstrings describing their purpose and expected input/output,
as you will use these functions as tools in the next task.

"""

from rdflib import Graph
from lab.task_1_sparql import answer  # reusing answer() from Task 1


def retrieve_sparql(graph: Graph, query: str) -> str: ...  # TODO


def retrieve_text(graph: Graph, keyword: str) -> str: ...  # TODO


def retrieve_embedding(graph: Graph, question: str) -> str: ...  # TODO


def compare(graph: Graph, question: str) -> None:
    """Run all three retrieval strategies on the same question and print results."""
    print(f"\n{'=' * 60}")
    print(f"QUESTION: {question}")
    print("=" * 60)

    for label, fn in [
        ("A) SPARQL retrieval", retrieve_sparql),
        ("B) Text retrieval", retrieve_text),
        ("C) Embedding retrieval", retrieve_embedding),
    ]:
        print(f"\n--- {label} ---")
        try:
            context = fn(graph, question)
        except NotImplementedError:
            print("  [not implemented yet]")
            continue
        print(context or "  (no results)")

        print("\n[ANSWER]")
        print(answer(question, context))


if __name__ == "__main__":
    g = Graph()
    g.parse("local_graph.ttl", format="turtle")
