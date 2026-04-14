"""
Task 1 — SPARQL-based RAG with Wikidata
========================================
Goal: build a minimal pipeline where the LLM generates a SPARQL query,
your code executes it on Wikidata, and the LLM answers using the results.

Pipeline:
question -> generate_sparql() -> query_wikidata() -> verbalize() -> answer()

Instructions
---
1. Choose a narrow topic (e.g. programming languages, Formula 1, etc.).
   All your test questions should belong to that topic.
2. Complete the five TODO functions below.
3. Test with at least three different questions and print all intermediate steps.
"""


def generate_sparql(question: str) -> str: ...  # TODO


def query_wikidata(sparql: str) -> list[dict]: ...  # TODO


def verbalize(results: list[dict]) -> str: ...  # TODO


def answer(question: str, context: str) -> str: ...  # TODO
# You may also use streaming here rather than returning the string result


def ask(question: str) -> None:
    """Run the full RAG pipeline and print each intermediate step.

    Arguments:
       question: A natural language question about your chosen topic.
    """
    print(f"\n{'=' * 60}")
    print(f"QUESTION: {question}")
    print("=" * 60)

    sparql = generate_sparql(question)
    print(f"\n[SPARQL]\n{sparql}")

    results = query_wikidata(sparql)
    print(f"\n[RAW RESULTS] {len(results)} row(s)")

    context = verbalize(results)
    print(f"\n[CONTEXT]\n{context}")

    print("\n[ANSWER]")
    final = answer(question, context)

    if final:
        print(final)


if __name__ == "__main__":
    ask("How many F1 championships has Lewis Hamilton won?")
