import os
from dotenv import load_dotenv
from tabulate import tabulate
from gtm.lead_generator.geocoding import geocode_location
from gtm.lead_generator.textsearch import fetch_leads
from gtm.lead_generator.utils import save_to_csv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
env_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=env_path)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    print("Error: RAPIDAPI_KEY not found in .env.")
    exit(1)

if __name__ == "__main__":
    print("Welcome to Will's Lead Generation Tool!")

    location = input("Enter the location (e.g., 'Sydney, Australia'): ").strip()
    query = input("Enter your search query (e.g., 'restaurants'; leave blank for no query): ").strip()
    radius = int(input("Enter the search radius in meters (max 50,000): ").strip())
    place_type = input(
        "Enter a place type (optional, e.g., 'restaurant', 'meal_delivery', 'meal_takeaway';)\n"
        "For a full list of supported place types, visit: https://developers.google.com/maps/documentation/places/web-service/supported_types\n"
        "Press 'Enter' to skip.\n> "
    ).strip()

    print(f"\nGeocoding location: '{location}'...")
    try:
        lat, lng = geocode_location(location, RAPIDAPI_KEY)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    print(f"Geocoding successful: Latitude = {lat}, Longitude = {lng}")

    print(f"\nFetching leads for query '{query}' within {radius} meters around '{location}'...")
    try:
        leads = fetch_leads(lat, lng, radius, query, place_type, RAPIDAPI_KEY)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    if leads:
        output_dir = os.path.join(project_root, "data", "output")
        output_path = save_to_csv(leads, query, output_dir)
        print("\nQuery Results:\n")
        print(tabulate(leads, headers="keys", tablefmt="pretty"))
        print(f"\nLeads saved to '{output_path}'")
    else:
        print("\nNo leads found.")

