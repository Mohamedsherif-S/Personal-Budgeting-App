class Category:
    CATEGORIES = ["food", "rent", "salary", "transport", "health", "general"]

    def get_categories_list(self, user_id):
        return self.CATEGORIES

    def validate_category(self, category_id):
        return category_id in self.CATEGORIES

    def auto_map_category(self, description, merchant):
        desc = description.lower()
        if any(w in desc for w in ["food", "grocery", "restaurant"]):
            return "food"
        if any(w in desc for w in ["salary", "wage", "income"]):
            return "salary"
        if any(w in desc for w in ["rent", "lease"]):
            return "rent"
        if any(w in desc for w in ["uber", "bus", "transport"]):
            return "transport"
        return "general"
