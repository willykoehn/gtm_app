import re
from urllib.parse import urlparse

def extract_domain(url):
    """
    Extract the pure domain name from a URL or other formats.

    Args:
        url (str): The input URL or domain string.

    Returns:
        str: The formatted domain name (e.g., 'example.com') or None if invalid.
    """
    if not url:
        return None

    # Parse the URL to extract the netloc
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc or parsed_url.path  # Use netloc; fallback to path if no scheme
    except Exception:
        return None

    # Remove common prefixes like 'www.'
    domain = domain.lower()
    if domain.startswith('www.'):
        domain = domain[4:]

    # Validate the domain using a regex
    domain_regex = re.compile(
        r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"  # Matches valid domain names like 'example.com'
    )
    if not domain_regex.match(domain):
        return None

    return domain

def categorize_business_size(number_of_leads):
    """
    Categorize a business size based on the number of leads.

    Args:
        number_of_leads (int): Number of leads associated with the domain.

    Returns:
        str: Business size category ('SME', 'Mid-Market', 'Enterprise').
    """
    if number_of_leads < 10:
        return "SME"
    elif 10 <= number_of_leads < 50:
        return "Mid-Market"
    else:
        return "Enterprise"

