import requests

GEOCODE_URL = "https://google-map-places.p.rapidapi.com/maps/api/geocode/json"


def geocode_location(location: str, api_key: str) -> tuple:
    """
    Geocodes a location string into latitude and longitude.

    Args:
        location (str): The address or location to geocode.
        api_key (str): Your RapidAPI key.

    Returns:
        tuple: A tuple (latitude, longitude) if successful, None otherwise.

    Raises:
        ValueError: If the location cannot be geocoded.
    """
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "google-map-places.p.rapidapi.com"
    }
    params = {
        "address": location,
        "language": "en",
        "region": "en",
        "result_type": "administrative_area_level_1",
        "location_type": "APPROXIMATE"
    }

    response = requests.get(GEOCODE_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise ValueError(f"Geocoding failed with status code {response.status_code}: {response.text}")

    results = response.json().get("results", [])
    if not results:
        raise ValueError("No results found for the provided location.")

    location_data = results[0]["geometry"]["location"]
    return location_data["lat"], location_data["lng"]

