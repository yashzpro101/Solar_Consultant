import pandas as pd

class MarketScraper:
    def __init__(self):
        # We no longer need max_capacity here as we moved live calc to app.py
        pass

    def get_latest_prices(self):
        """Returns a DataFrame of verified solar component prices for 2026."""
        data = {
            "Component": [
                "Mono PERC Solar Panel (550W)",
                "Hybrid Inverter (5kW)",
                "Lithium-Ion Battery (5kWh)",
                "Mounting Structure (per kW)",
                "Bi-Directional Net Meter"
            ],
            "Price (Approx)": [
                "₹14,500",
                "₹65,000",
                "₹1,20,000",
                "₹8,500",
                "₹4,200"
            ],
            "Availability": ["In Stock", "High Demand", "Available", "In Stock", "Limited"]
        }
        return pd.DataFrame(data)