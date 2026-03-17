# ☀️ SolarOS 2026: Intelligent Energy Management Dashboard

**Developer:** Yash Narayan Mohanty  
**Project Type:** Technical Portfolio / University Scholarship Submission  
**Live Application:** [PASTE_YOUR_STREAMLIT_LINK_HERE]

---

## ߚ Overview
SolarOS 2026 is a comprehensive Python-based dashboard designed to bridge the gap between complex solar data and residential users. Built with a focus on **AI-driven forecasting** and **financial transparency**, the application provides users in India with localized insights into solar harvest potential, government subsidies, and long-term carbon impact.

## ߧ Key Modules
- **Atmospheric Prediction Engine:** Simulates neural network forecasting to project energy harvest for the upcoming 48 hours.
- **Financial Analytics:** Dynamically calculates savings based on state-specific electricity tariffs (PM-Surya Ghar integration).
- **Live Telemetry Interface:** Provides a real-time visualization of solar array performance and hardware efficiency.
- **Subsidy Navigator:** A logical guide to the national rooftop solar portal, assisting users through the application lifecycle.

## ߛ️ Technical Stack
- **Language:** Python 3.10+
- **Framework:** Streamlit (Web UI & Deployment)
- **Data Handling:** Pandas, NumPy
- **Styling:** Custom CSS Injection with dynamic theme-switching capabilities.
- **Deployment:** GitHub & Streamlit Community Cloud.

## ߓ File Architecture
- `app.py`: The central hub and UI logic.
- `ai_solar_forecast.py`: Neural simulation and forecasting algorithms.
- `gov_subsidy_bot.py`: Regional subsidy calculation engine.
- `real_time_scraper.py`: Automated fetching of market rates.
- `savings_tracker.py`: Historical data processing for ROI analysis.
- `config.py`: Global constants and state electricity pricing.

## ߓ Roadmap & Future Scope
- [ ] **API Integration:** Replacing simulated data with live OpenWeatherMap and NASA Power API feeds.
- [ ] **Hardware Sync:** Connecting physical ESP32/Arduino sensors for real-time voltage monitoring.
- [ ] **ML Training:** Feeding local Odisha solar irradiance data into a Scikit-learn model for higher accuracy.

## ߓ License
This project is open-source and available under the [MIT License](LICENSE).

---
*Created as part of a technical portfolio for University Undergraduate Admissions in AI and Data Science.*
