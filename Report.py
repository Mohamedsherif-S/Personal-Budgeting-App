class Report:
    def request_report(self, user_id, start, end, r_type):
        if self._validate_date_range(start, end):
            print(f"  [Report] {r_type} | {start} → {end}")

    def _validate_date_range(self, start, end):
        return start <= end

    def calculate_total_income(self, transactions):
        return sum(float(t["amount"]) for t in transactions if t.get("type") == "income")

    def calculate_total_expense(self, transactions):
        return sum(float(t["amount"]) for t in transactions if t.get("type") == "expense")
