class Report:
    def request_report(self, user_id, start, end, r_type):
        if self.validate_date_range(start, end):
            print(f"  [Report] {r_type} | {start} → {end}")

    def validate_date_range(self, start, end):
        return start <= end

    def calculate_total_income(self, transactions):
        return sum(t["amount"] for t in transactions if t.get("type") == "income")

    def calculate_total_expense(self, transactions):
        return sum(t["amount"] for t in transactions if t.get("type") == "expense")

    def categorize_expenses(self, transactions, categories):
        return {}

    def calculate_budget_variance(self, budgets, transactions):
        return {}

    def identify_top_spending_categories(self, transactions, limit):
        return []

    def generate_charts(self, *args):
        pass

    def create_pie_chart(self, data):
        pass

    def create_bar_chart(self, data):
        pass

    def create_line_chart(self, data):
        pass

    def compile_report(self, summary, charts, tables, insights):
        return {}