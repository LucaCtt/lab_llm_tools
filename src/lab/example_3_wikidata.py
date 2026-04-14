import requests
from rdflib import Graph

from lab.settings import Settings

settings = Settings()

# Retrieves Formula 1 drivers, their nationalities, and the teams they have
# driven for. CONSTRUCT returns RDF triples directly instead of a table of
# bindings — the triple pattern after CONSTRUCT defines the output graph shape.
SPARQL_QUERY = """\
CONSTRUCT {
  ?driver rdfs:label ?driverLabel .
  ?driver <http://lab.unibs.it/ontology/nationality> ?nationalityLabel .
  ?driver <http://lab.unibs.it/ontology/team> ?teamLabel .
}
WHERE {
  ?driver wdt:P31 wd:Q5 .           # instance of: human
  ?driver wdt:P106 wd:Q10841764 .   # occupation: racing driver
  ?driver wdt:P641 wd:Q1968 .       # sport: Formula One
  ?driver wdt:P27 ?nationality .    # country of citizenship
  OPTIONAL { ?driver wdt:P54 ?team . }  # member of sports team
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en" .
  }
}
LIMIT 20
"""

OUTPUT_FILE = "f1_drivers.ttl"


def fetch_rdf(sparql: str) -> Graph:
    """Send a CONSTRUCT query to Wikidata and parse the response as an rdflib Graph."""
    response = requests.get(
        settings.wikidata_endpoint,
        params={"query": sparql},
        headers={
            "Accept": "text/turtle",
            "User-Agent": settings.wikidata_user_agent,
        },
        timeout=10,
    )
    response.raise_for_status()

    g = Graph()
    g.parse(data=response.text, format="turtle")
    return g


def save_graph(g: Graph, path: str) -> None:
    """Serialise the graph to a Turtle file, merging with existing content."""
    existing = Graph()
    try:
        existing.parse(path, format="turtle")
        print(f"Loaded {len(existing)} existing triples from {path}")
    except FileNotFoundError:
        print(f"{path} not found, creating a new file.")

    merged = existing + g
    merged.serialize(path, format="turtle")
    print(f"Saved {len(merged)} triples to {path}")


def main():
    print("Querying Wikidata...")
    g = fetch_rdf(SPARQL_QUERY)
    print(f"Retrieved {len(g)} triples")
    print(g.serialize(format="turtle"))
    save_graph(g, OUTPUT_FILE)


if __name__ == "__main__":
    main()
