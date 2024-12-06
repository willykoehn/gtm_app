import os
import pandas as pd


def save_to_csv(data: list, query: str, output_dir: str) -> str:
    """
    Saves data to a CSV file.

    Args:
        data (list): The list of data to save.
        query (str): The query string (used for naming the file).
        output_dir (str): The directory where the file will be saved.

    Returns:
        str: The full path to the saved file.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{query.replace(' ', '_')}_leads.csv"
    file_path = os.path.join(output_dir, file_name)

    # Ensure keys match expected column headers
    for row in data:
        row.setdefault("place_type", "Unknown")  # Default value if missing
        row.setdefault("google_place_id", "Unknown")  # Rename key for consistency

    pd.DataFrame(data).to_csv(file_path, index=False)
    return file_path

