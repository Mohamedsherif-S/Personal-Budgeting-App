class Category:
    """Class to handle transaction categories and auto-mapping."""
    
    CATEGORIES = ["food", "rent", "salary", "transport", "health", "general"]

    def get_categories_list(self, user_id):
        """Returns the list of categories (user_id is kept for future scaling)."""
        return self.CATEGORIES

    def validate_category(self, category_id):
        """Checks if the category is in our allowed list."""
        return category_id in self.CATEGORIES

    def auto_map_category(self, description, merchant):
        """
        Detects category from description/merchant keywords.
        Returns the category name as a string.
        """
        desc = description.lower()
        
        # Look for food or eating out
        if any(w in desc for w in ["food", "grocery", "restaurant"]):
            return "food"
            
        # Check for income sources
        if any(w in desc for w in ["salary", "wage", "income"]):
            return "salary"
            
        # Check for housing expenses
        if any(w in desc for w in ["rent", "lease"]):
            return "rent"
            
        # Transportation and commute
        if any(w in desc for w in ["uber", "bus", "transport"]):
            return "transport"
            
        # Fallback to general if nothing matches
        return "general"
