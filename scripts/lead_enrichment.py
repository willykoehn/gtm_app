import os
from dotenv import load_dotenv
from gtm.models.database import get_session, get_database_engine
from gtm.models.leads import Lead
from gtm.models.domains import Domain
from gtm.utils.display_utils import format_enriched_data
from gtm.lead_enrichment.enrichment import enrich_lead, update_lead_details
from gtm.utils.domain_utils import extract_domain, categorize_business_size

# Load environment variables
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path=env_path)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

if not RAPIDAPI_KEY:
    print("Error: RAPIDAPI_KEY not found in .env.")
    exit(1)

# Initialize database
engine = get_database_engine()
session = get_session(engine)

def ensure_domain(session, website):
    """
    Ensure the domain exists in the Domain table, and return the domain instance.

    Args:
        session: The database session.
        website: The website URL to extract the domain from.

    Returns:
        Domain: The domain instance, either existing or newly created.
    """
    domain_name = extract_domain(website)
    if domain_name:
        domain = session.query(Domain).filter_by(domain_name=domain_name).first()
        if not domain:
            domain = Domain(domain_name=domain_name, number_of_leads=1)
            session.add(domain)
        else:
            domain.number_of_leads = session.query(Lead).filter(Lead.domain_id == domain.id).count()
            domain.business_size_category = categorize_business_size(domain.number_of_leads)
        return domain
    return None

if __name__ == "__main__":
    print("Welcome to Lead Enrichment Tool!")

    # Option 1: Get data for unenriched leads
    user_choice = input("Do you want to retrieve data for unenriched leads? (y/n): ").strip().lower()

    if user_choice == "y":
        leads = session.query(Lead).filter(
            (Lead.phone_number == None) &
            (Lead.email == None) &
            (Lead.website == None) &
            (Lead.opening_hours == None)
        ).all()

        if not leads:
            print("No unenriched leads found.")
        else:
            for lead in leads:
                print(f"\nProcessing lead: {lead.name} (ID: {lead.id})")

                retrieve_data = input("Do you want to retrieve enriched details for this lead? (y/n): ").strip().lower()
                if retrieve_data == "y":
                    try:
                        details = enrich_lead(lead.google_place_id, RAPIDAPI_KEY)

                        # Debug: Ensure enriched data is retrieved
                        print("Enriched Details (Raw):", details)

                        if details:
                            format_enriched_data(details)
                        else:
                            print(f"No enriched data found for lead: {lead.name}")

                        update_db = input("Do you want to update the database with this data? (y/n): ").strip().lower()
                        if update_db == "y":
                            domain = ensure_domain(session, details.get("website"))
                            update_lead_details(session, lead, details, domain)

                    except Exception as e:
                        print(f"Error enriching lead '{lead.name}': {e}")

    # Option 2: Update data for a specific lead
    elif user_choice == "n":
        update_choice = input("Do you want to update data for a specific lead? (y/n): ").strip().lower()

        if update_choice == "y":
            try:
                lead_id = int(input("Enter the Lead ID to update: ").strip())
                lead = session.get(Lead, lead_id)

                if not lead:
                    print(f"No lead found with ID {lead_id}.")
                else:
                    print(f"Processing lead: {lead.name} (ID: {lead.id})")

                    details = enrich_lead(lead.google_place_id, RAPIDAPI_KEY)
                    
                    # Debug: Ensure enriched data is retrieved
                    print("Enriched Details (Raw):", details)

                    if details:
                        format_enriched_data(details)
                    else:
                        print(f"No enriched data found for lead: {lead.name}")

                    update_db = input("Do you want to update the database with this data? (y/n): ").strip().lower()
                    if update_db == "y":
                        domain = ensure_domain(session, details.get("website"))
                        update_lead_details(session, lead, details, domain)

            except Exception as e:
                print(f"Error processing lead: {e}")

    print("Lead enrichment process completed.")

