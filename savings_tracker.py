import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from config import Config


class SavingsTracker:
    def __init__(self):
        # FIX: Default to a general rate since app.py now passes calculated values
        # We use .get() to avoid the AttributeError if the key is missing
        self.rate = Config.STATE_RATES.get("Other", 7.0)
        self.co2_factor = Config.CO2_EMISSION_FACTOR
        self.model = LinearRegression()

    def _train_projection_model(self, historical_data: list):
        """Trains a simple linear regression to project future savings."""
        # X = months (1, 2, 3...), y = data values
        months = np.array(range(1, len(historical_data) + 1)).reshape(-1, 1)
        values = np.array(historical_data)
        self.model.fit(months, values)

    def generate_dashboard_data(self, history_values: list) -> dict:
        """Calculates total savings, CO2 reduction, and next month's projection."""
        if not history_values:
            return {}

        # Train model on the values provided (already calculated in app.py)
        self._train_projection_model(history_values)

        total_val = sum(history_values)

        # Since history_values passed from app.py are already in Rupees:
        total_savings = total_val
        # Reverse calculate kWh for CO2 estimation (Savings / Rate)
        total_kwh = total_savings / self.rate
        total_co2_saved = total_kwh * self.co2_factor

        next_month_idx = np.array([[len(history_values) + 1]])
        projected_savings = self.model.predict(next_month_idx)[0]

        # Formatting months for the graph
        month_names = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
        # Ensure list length matches historical data
        display_months = month_names[-len(history_values):] if len(history_values) <= 6 else range(1,
                                                                                                   len(history_values) + 1)

        return {
            "total_savings": total_savings,
            "co2_saved_kg": total_co2_saved,
            "projected_next_month": max(0, projected_savings),  # Ensure no negative projections
            "history_df": pd.DataFrame({
                "Month": display_months,
                "Savings": history_values
            })
        }