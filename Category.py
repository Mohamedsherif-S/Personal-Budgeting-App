class Category:
    """
    Represents categories.
    """

    def get_categories_list(self, user_id):
        return ["food", "rent", "salary"]

    def validate_category(self, category_id):
        return True

    def auto_map_category(self, description, merchant):
        return "general"

    def match_by_keywords(self, description, merchant):
        return "matched"

    def get_category_name(self, category_id):
        return "category_name"