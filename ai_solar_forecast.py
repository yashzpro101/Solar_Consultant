import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from config import Config


class SolarForecaster:
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.lat = Config.CITY_LAT
        self.lon = Config.CITY_LON
        self.model = self._train_dummy_model()  # In production, load a pre-trained .pkl file

    def _train_dummy_model(self) -> RandomForestRegressor:
        """Trains a basic Random Forest model on dummy data for demonstration."""
        # Features: [Cloud Cover %, Temperature (C), Daylight Hours]
        X = np.array([[10, 30, 12], [80, 22, 10], [50, 25, 11], [0, 35, 13]])
        y = np.array([50.0, 15.0, 30.0, 60.0])  # Target: Harvest in kWh

        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        return model

    def fetch_weather_forecast(self) -> list:
        """Fetches 48-hour weather forecast from OpenWeatherMap."""
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("list", [])[:16]  # 16 * 3-hour chunks = 48 hours
        except requests.exceptions.RequestException as e:
            print(f"Weather API Error: {e}")
            return []

    def predict_48h_harvest(self) -> float:
        """Predicts the harvest potential for the next 48 hours."""
        forecast_data = self.fetch_weather_forecast()
        if not forecast_data:
            return 0.0

        total_predicted_kwh = 0.0
        for chunk in forecast_data:
            clouds = chunk["clouds"]["all"]
            temp = chunk["main"]["temp"]
            daylight = 3 if chunk["sys"]["pod"] == "d" else 0  # 3 hours of daylight if 'day'

            features = np.array([[clouds, temp, daylight]])
            prediction = self.model.predict(features)[0]
            total_predicted_kwh += prediction

        return round(total_predicted_kwh, 2)