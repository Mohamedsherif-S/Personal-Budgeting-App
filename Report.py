class Report:
    """Handles financial report generation and data calculations."""

    def request_report(self, user_id, start, end, r_type):
        """
        Validates the date range and prints a report summary header.
        Takes start/end dates and the report type (summary/detailed).
        """
        if self._validate_date_range(start, end):
            print(f"  [Report] {r_type} | {start} → {end}")

    def _validate_date_range(self, start, end):
        """Internal helper to ensure the start date isn't after the end date."""
        return start <= end

    def calculate_total_income(self, transactions):
        """
        Filters transactions for income and returns the total sum.
        Expects a list of transaction dictionaries.
        """
        return sum(float(t["amount"]) for t in transactions if t.get("type") == "income")

    def calculate_total_expense(self, transactions):
        """
        Filters transactions for expenses and returns the total sum.
        Expects a list of transaction dictionaries.
        """
        return sum(float(t["amount"]) for t in transactions if t.get("type") == "expense")
