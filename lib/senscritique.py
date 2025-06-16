import requests

SENSCRITIQUE_GRAPHQL_URL = "https://www.senscritique.com/graphql"

SEARCH_QUERY = [{
    "operationName": "Results",
    "variables": {
        "query": "%query%",
        "filters": [],
        "page": {"size": 16, "from": 0}
    },
    "query": "query Results($query: String, $filters: [SKFiltersSet], $page: SKPageInput, $sortBy: String) { results(query: $query, filters: $filters) { hits(page: $page, sortBy: $sortBy) { items { ... on ResultHit { id product { id title originalTitle url rating universe dateRelease year_of_production seasons { seasonNumber } providers { name } } } } } } }"
}]

HEADERS = {
    "User-Agent": "Kodi-LatestRating/1.0",
    "Content-Type": "application/json"
}

def get_senscritique_rating(title):
    body = str(SEARCH_QUERY).replace("%query%", title)
    response = requests.post(SENSCRITIQUE_GRAPHQL_URL, data=body, headers=HEADERS)
    if response.ok:
        try:
            data = response.json()
            items = data[0]["data"]["results"]["hits"]["items"]
            if items:
                product = items[0]["product"]
                return product.get("rating", None)
        except Exception:
            return None
    return None
