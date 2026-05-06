# Merge Request Summary

The sections below summarize the file-by-file changes that remain in scope for review.

## `.gitignore`

- Keeps `.env` ignored and adds `/.deps`.

## `src/lab/example_1_litellm.py`

- Switches the example from `settings.model` to `settings.litellm_model`.

## `src/lab/example_2_function_calls.py`

- Replaces the automatic `function_to_dict` conversion with an explicit tool schema for `get_championships`.
- Updates the completion call to use `settings.litellm_model` instead of the raw `settings.model`.
- The explicit schema makes the function-calling example more deterministic and easier to reason about because the argument contract is now written directly in the source.

## `src/lab/example_3_wikidata.py`

- Reworks the Wikidata extraction flow from a direct `CONSTRUCT` query into a `SELECT`-based pipeline that post-processes rows into RDF triples locally.
- Narrows the domain to a fixed set of Formula 1 drivers identified by QIDs, with explicit slug and label mappings.
- Adds fallback query endpoints so the export can retry against a secondary Wikidata-compatible endpoint if the primary one fails.
- Introduces nationality normalization logic, including conversion from country labels such as `United Kingdom` to nationalities such as `British`.
- Adds selection logic for team history so the exported graph stores one representative team per driver, preferring current or latest data when multiple rows exist.
- Simplifies serialization by writing the generated graph directly instead of merging with any pre-existing Turtle file.
- The file now acts as a controlled graph builder for the rest of the lab.

## `src/lab/settings.py`

- Changes the default LiteLLM base URL from an internal HTTP endpoint to `https://gpustack.ing.unibs.it/v1`.
- Changes the default model from `openai/qwen-3.5-instruct` to `qwen35-4b`.
- Adds a `litellm_model` property that returns the configured model unchanged if it already contains a provider prefix, otherwise prefixes it as `openai/<model>`.

## `src/lab/task_1_sparql.py`

- Replaces the placeholder assignment skeleton with a complete Formula 1 question-answering pipeline.
- Configures LiteLLM using the shared settings object and fails fast if `LITELLM_API_KEY` is missing.
- Adds a focused SPARQL-generation prompt and a separate answer-generation prompt tuned for concise, grounded answers.
- Introduces domain constants for known drivers, QIDs, supported nationalities, fallback Wikidata endpoints, and the local Turtle graph path.
- Adds response-cleaning helpers so LLM-generated SPARQL can be stripped of markdown fences or leading prose before execution.
- Adds question analysis helpers that detect named drivers and match known terms, allowing simple questions to be routed to handcrafted queries instead of relying entirely on model generation.
- Adds heuristics to validate whether a generated SPARQL query looks plausible for the intended Formula 1 domain.
- Adds support for loading a locally exported RDF graph through `example_3_wikidata.py`, which gives the task an offline grounding path in addition to live Wikidata access.

## `src/lab/task_2_hybrid_retrieval.py`

- Replaces the TODO skeleton with three implemented retrieval strategies over the local RDF graph: SPARQL retrieval, keyword/text retrieval, and embedding retrieval.
- Adds graph-loading support that exports and reads `f1_drivers.ttl` automatically when the local graph is missing.
- Adds shared normalization, token extraction, and label-matching helpers so retrieval can key off driver names, nationality words, and team-related terms.
- Builds structured driver records from RDF triples and converts them into readable sentences used by both text and embedding retrieval.
- Implements local SPARQL generation against the exported graph using `rdfs:label` and the custom `lab:` namespace, with dynamic filters derived from question terms.
- Implements text retrieval as a simple scored keyword match over normalized driver summaries.
- Implements embedding retrieval with `sentence-transformers`, caches the model with `lru_cache`, and degrades gracefully back to text retrieval when embeddings are unavailable.
- Re-enables the embedding comparison path in `compare()` so all three retrieval strategies can be tested side by side.

## `src/lab/task_3_rag_agent.py`

- Reframes the task as a tool-calling agent built on top of the retrieval strategies from Task 2.
- Configures LiteLLM through shared settings and enforces the presence of `LITELLM_API_KEY`.
- Imports all three retrieval modes and wraps them as callable tools bound to the current RDF graph instance.
- Defines explicit JSON schemas for each retrieval tool instead of leaving tool structure implicit.
- Adds a system prompt that forces retrieval-before-answering behavior and biases direct fact questions toward SPARQL retrieval first.
- Implements an iterative tool-calling loop that sends the conversation to LiteLLM, executes requested tools, appends tool results back into the message history, and continues until the model stops requesting tools.
- Adds a fallback path that manually invokes a retrieval tool if the model tries to answer without calling one first.
- Combines all retrieved context and routes the final response through `task_1_sparql.answer()` so the answer stays grounded in retrieved evidence.
