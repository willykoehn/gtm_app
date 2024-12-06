import requests
import time

TEXTSEARCH_URL = "https://google-map-places.p.rapidapi.com/maps/api/place/textsearch/json"


def fetch_leads(lat: float, lng: float, radius: int, query: str, place_type: str, api_key: str) -> list:
    """
    Fetches leads using the Google Maps Places API.

    Args:
        lat (float): Latitude of the location.
        lng (float): Longitude of the location.
        radius (int): Search radius in meters.
        query (str): Search query string.
        place_type (str): Place type (e.g., "restaurant").
        api_key (str): Your RapidAPI key.

    Returns:
        list: A list of leads, where each lead is a dictionary.

    Raises:
        ValueError: If the API request fails.
    """
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "google-map-places.p.rapidapi.com"
    }

    params = {
        "query": query,
        "radius": radius,
        "location": f"{lat},{lng}",
        "type": place_type,
        "language": "en",
        "region": "en"
    }

    all_leads = []
    while True:
        response = requests.get(TEXTSEARCH_URL, headers=headers, params=params)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch leads: {response.status_code}: {response.text}")

        results = response.json()
        if "results" not in results:
            break

        leads = [
            {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
                "user_ratings_total": place.get("user_ratings_total"),
                "google_place_id": place.get("place_id"),
                "business_status": place.get("business_status"),
            }
            for place in results["results"]
        ]
        all_leads.extend(leads)

        next_page_token = results.get("next_page_token")
        if not next_page_token:
            break

        params["pagetoken"] = next_page_token
        time.sleep(2)

    return all_leads

