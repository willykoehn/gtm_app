
# gtm_app

**gtm_app** is a Python-based tool designed to assist businesses and developers with lead generation, market research, lead enrichment, and lead scoring. The project leverages the Google Maps Places API to fetch business leads based on user-defined parameters such as location, query, and place type.

---

## Features
- **Lead Generation**:
  - Geocode locations into latitude and longitude.
  - Fetch leads based on query and place type using the Google Maps Places API.
  - Support for paginated results (up to 60 results).
  - Pretty-printed results in the terminal using `tabulate`.
  - Save results to a CSV file for further analysis.
  
- **Market Research (Planned)**:
  - Gather and analyze trends in specific industries or locations.

- **Lead Enrichment (Planned)**:
  - Enrich lead data with additional details like social media profiles or company size.

- **Lead Scoring (Planned)**:
  - Score leads based on custom criteria like ratings, reviews, or relevance.

---

## Setup

### Prerequisites
- Python 3.8 or higher.
- A [RapidAPI](https://rapidapi.com/) account with access to the [Google Maps Places API](https://rapidapi.com/gmapplatform/api/google-map-places).

### Installation

#### Clone the Repository
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gtm_app.git
   cd gtm_app
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scriptsctivate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Configure the `.env` File
4. Create a `.env` file in the project root:
   ```env
   RAPIDAPI_KEY=your_rapidapi_key_here
   ```

#### Install the Project in Editable Mode
5. Install the project as an editable package:
   ```bash
   pip install -e .
   ```

   This makes the `gtm` module available globally in your virtual environment.

---

## Usage
1. Navigate to the project directory:
   ```bash
   cd gtm_app
   ```

2. Run the lead generation script:
   ```bash
   python scripts/lead_generator.py
   ```

3. Follow the prompts:
   - Enter a location (e.g., `Sydney, Australia`).
   - Enter a search query (e.g., `restaurants`).
   - Enter a search radius in meters (e.g., `5000`).
   - Optionally, specify a place type (e.g., `restaurant`). For a full list of supported place types, visit the [Google Maps Place Types Documentation](https://developers.google.com/maps/documentation/places/web-service/supported_types).

---

## Example Output
### Terminal Output
```
Welcome to Will's Lead Generation Tool!

Enter the location (e.g., 'Sydney, Australia'): Sydney, Australia
Enter your search query (e.g., 'restaurants'; leave blank and press Enter for a blank query): restaurants
Enter the search radius in meters (max 50,000): 5000
Enter a place type (optional, e.g., 'restaurant'; press Enter to skip): restaurant

Geocoding location: 'Sydney, Australia'...
Geocoding successful: Latitude = -33.8688, Longitude = 151.2093

Fetching leads for query 'restaurants' within 5000 meters around 'Sydney, Australia'...

Query Results:

+------------------------+--------------------------+--------+-------------------+---------------------+-----------------+
|          name          |         address         | rating | user_ratings_total |      place_id       | business_status |
+------------------------+--------------------------+--------+-------------------+---------------------+-----------------+
| The Sydney Restaurant | 123 Main St, Sydney      | 4.5    | 200               | abc123              | OPERATIONAL     |
| Another Restaurant     | 456 Market St, Sydney   | 4.0    | 150               | def456              | OPERATIONAL     |
+------------------------+--------------------------+--------+-------------------+---------------------+-----------------+

Leads saved to '/path/to/gtm_app/data/output/restaurants_leads.csv'
```

### CSV Output
Results are saved as a CSV file in the `data/output/` directory:
```
data/output/restaurants_leads.csv
```

---

## Roadmap
- [x] Lead Generation
- [ ] Market Research
- [ ] Lead Enrichment
- [ ] Lead Scoring

---

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your improvements.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
