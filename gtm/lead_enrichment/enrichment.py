import requests
import json
from gtm.utils.api_utils import make_api_request
from gtm.models.domains import Domain
from gtm.utils.domain_utils import extract_domain, categorize_business_size

PLACE_DETAILS_URL = "https://google-map-places.p.rapidapi.com/maps/api/place/details/json"

def enrich_lead(google_place_id, api_key):
    """
    Fetch and enrich lead details using Google Maps Places API's Place Details endpoint.

    Args:
        google_place_id (str): The unique Google Place ID of the lead.
        api_key (str): The API key for authentication.

    Returns:
        dict: Enriched lead details (phone, email, website, opening hours).
    """
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "google-map-places.p.rapidapi.com"
    }
    params = {"place_id": google_place_id}

    response = requests.get(PLACE_DETAILS_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch details for Place ID {google_place_id}")

    result = response.json().get("result", {})

    return {
        "phone_number": result.get("formatted_phone_number"),
        "email": result.get("email"),  # Assuming the API provides email in some responses
        "website": result.get("website"),
        "opening_hours": json.dumps(result.get("opening_hours", {}).get("weekday_text", [])),  # Convert to JSON
        "user_ratings_total": result.get("user_ratings_total", 0),  # Default to 0
    }

def update_lead_details(session, lead, details):
    """
    Update lead details in the database.

    Args:
        session (Session): SQLAlchemy session.
        lead (Lead): Lead object to update.
        details (dict): Enriched data fields.
    """
    # Update lead fields
    lead.phone_number = details.get("phone_number")
    lead.email = details.get("email")
    lead.website = details.get("website")
    lead.opening_hours = details.get("opening_hours")

    # Extract domain and handle domain table updates
    domain_name = extract_domain(details.get("website"))
    if domain_name:
        domain = session.query(Domain).filter_by(domain_name=domain_name).first()
        if not domain:
            domain = Domain(domain_name=domain_name, number_of_leads=1)
            session.add(domain)
        else:
            domain.number_of_leads += 1
        domain.business_size_category = categorize_business_size(domain.number_of_leads)
        lead.domain = domain

    # Commit changes to the database
    session.commit()
    print(f"Lead '{lead.name}' has been updated successfully.")
