class GovGuide:
    def __init__(self):
        # Logic rules for 2026 PM Surya Ghar Muft Bijli Yojana
        self.subsidy_tiers = {
            "tier_1_rate": 30000,  # ₹30,000 per kW for first 2 kW
            "tier_2_rate": 18000,  # ₹18,000 for the 3rd kW
            "max_subsidy": 78000  # Total Central Cap
        }

    def calculate_subsidy(self, system_size_kw: float) -> dict:
        """Calculates expected subsidy and provides step-by-step claims guide."""

        if system_size_kw <= 2:
            subsidy_amount = system_size_kw * self.subsidy_tiers["tier_1_rate"]
        elif system_size_kw < 3:
            base = 2 * self.subsidy_tiers["tier_1_rate"]
            extra = (system_size_kw - 2) * self.subsidy_tiers["tier_2_rate"]
            subsidy_amount = base + extra
        else:
            # 3kW and above gets the full cap
            subsidy_amount = self.subsidy_tiers["max_subsidy"]

        steps = [
            "1. Visit the 'PM Surya Ghar' official portal or mobile app.",
            "2. Register using your Consumer Account Number (from your Electricity Bill).",
            "3. Apply for Technical Feasibility approval from your local DISCOM.",
            "4. Get installation done by a registered vendor after approval.",
            f"5. Post net-metering, your ₹{subsidy_amount:,.2f} subsidy will be credited to your linked bank account."
        ]

        return {"estimated_subsidy": subsidy_amount, "steps": steps}