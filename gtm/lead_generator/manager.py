from gtm.lead_generator.geocoding import geocode_location
from gtm.lead_generator.textsearch import fetch_leads
from gtm.lead_generator.utils import save_to_csv
from gtm.models.database import get_database_engine, get_session
from gtm.models.leads import Lead


class LeadManager:
    def __init__(self, api_key, db_url="sqlite:///data/leads.db"):
        self.api_key = api_key
        self.engine = get_database_engine(db_url)
        self.session = get_session(self.engine)

    def geocode_location(self, location):
        """Wrapper for geocoding logic."""
        return geocode_location(location, self.api_key)

    def fetch_leads(self, lat, lng, radius, query, place_type):
        """Wrapper for fetching leads."""
        return fetch_leads(lat, lng, radius, query, place_type, self.api_key)

    def save_leads_to_db(self, leads, place_type):
        """
        Inserts or updates leads in the database.
        """
        for lead in leads:
            existing_lead = (
                self.session.query(Lead)
                .filter_by(google_place_id=lead["google_place_id"])
                .first()
            )
            if existing_lead:
                # Update existing lead
                existing_lead.name = lead["name"]
                existing_lead.address = lead["address"]
                existing_lead.rating = lead["rating"]
                existing_lead.user_ratings_total = lead["user_ratings_total"]
                existing_lead.business_status = lead["business_status"]
                existing_lead.place_type = place_type
            else:
                # Insert new lead
                new_lead = Lead(
                    name=lead["name"],
                    address=lead["address"],
                    rating=lead["rating"],
                    user_ratings_total=lead["user_ratings_total"],
                    google_place_id=lead["google_place_id"],
                    business_status=lead["business_status"],
                    place_type=place_type,
                )
                self.session.add(new_lead)
        self.session.commit()

