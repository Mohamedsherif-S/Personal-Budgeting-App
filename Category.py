class Category:
    def get_categories_list(self, user_id):
        return ["food", "rent", "salary", "transport", "health", "general"]

    def validate_category(self, category_id):
        return category_id in self.get_categories_list(None)

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

    def match_by_keywords(self, description, merchant):
        return self.auto_map_category(description, merchant)

    def get_category_name(self, category_id):
        return category_id