import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    # API Keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_fallback_key")
    CITY_LAT = os.getenv("CITY_LAT", "28.6139")  # Default: New Delhi
    CITY_LON = os.getenv("CITY_LON", "77.2090")

    # 2026 Residential Electricity Rates (₹ per kWh/Unit)
    # These are used to calculate the 'Savings' dynamically
    STATE_RATES = {
        "Odisha": 5.80,
        "Rajasthan": 7.10,
        "Telangana": 8.50,
        "Karnataka": 8.15,
        "West Bengal": 7.40,
        "Delhi": 6.50,
        "Gujarat": 7.20,
        "Maharashtra": 9.80,
        "Uttar Pradesh": 7.50,
        "Other": 7.00
    }

    CO2_EMISSION_FACTOR = 0.85  # kg of CO2 saved per kWh generated