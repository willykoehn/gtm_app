from tabulate import tabulate

def format_enriched_data(details):
    """
    Format enriched data for pretty-printing.

    Args:
        details (dict): The enriched data fields.

    Returns:
        str: Formatted string representation of the data.
    """
    # Format opening hours
    opening_hours = "[array]" if "opening_hours" in details and details["opening_hours"] else ""

    # Prepare the table
    formatted_data = [
        ["Phone Number", details.get("phone_number", "")],
        ["Email", details.get("email", "")],
        ["Website", details.get("website", "")],
        ["Opening Hours", opening_hours]
    ]

    # Pretty-print the table
    return tabulate(formatted_data, headers=["Field", "Value"], tablefmt="pretty")

