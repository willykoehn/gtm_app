import os
from dotenv import load_dotenv
from tabulate import tabulate
from gtm.lead_generator.manager import LeadManager
from gtm.lead_generator.utils import save_to_csv
from gtm.models.leads import Lead
from gtm.models.domains import Domain

# Load environment variables
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path=env_path)

# Get API key
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    print("Error: RAPIDAPI_KEY not found in .env. Please ensure it is set correctly.")
    exit(1)

if __name__ == "__main__":
    print("Welcome to Will's Lead Generation Tool!")

    # Get user input
    location = input("Enter the location (e.g., 'Sydney, Australia'): ").strip()
    query = input(
        "Enter your search query (e.g., 'restaurants'; leave blank for no query): "
    ).strip()
    radius = int(input("Enter the search radius in meters (max 50,000): ").strip())
    place_type = input(
        "Enter a place type (optional, e.g., 'restaurant', 'meal_delivery', 'meal_takeaway';)\n"
        "For a full list of supported place types, visit: https://developers.google.com/maps/documentation/places/web-service/supported_types\n"
        "Press 'Enter' to skip.\n> "
    ).strip()

    # Initialize LeadManager
    manager = LeadManager(api_key=RAPIDAPI_KEY)

    # Geocode location
    print(f"\nGeocoding location: '{location}'...")
    try:
        lat, lng = manager.geocode_location(location)
        print(f"Geocoding successful: Latitude = {lat}, Longitude = {lng}")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    # Fetch leads
    print(f"\nFetching leads for query '{query}' within {radius} meters around '{location}'...")
    try:
        leads = manager.fetch_leads(lat, lng, radius, query, place_type)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

    # Save leads to CSV
    if leads:
        output_dir = os.path.join(project_root, "data", "output")
        output_path = save_to_csv(leads, query, output_dir)
        print("\nQuery Results:\n")
        print(tabulate(leads, headers="keys", tablefmt="pretty"))
        print(f"\nLeads saved to '{output_path}'")

        # Ask user if they want to update the database
        update_db = input("\nDo you want to update the database with these leads? (y/n): ").strip().lower()
        if update_db == 'y':
            manager.save_leads_to_db(leads, place_type)
            print("\nDatabase updated successfully!")
    else:
        print("\nNo leads found.")

