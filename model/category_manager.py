# model/category_manager.py
class CategoryManager:
    def __init__(self):
        self.categories = {}  # Dictionary to store app-to-category mappings

    def add_category(self, app_name, category):
        """Add or update a category for an app."""
        self.categories[app_name] = category

    def get_category(self, app_name):
        """Get the category for an app."""
        return self.categories.get(app_name, "Uncategorized")

    def update_categories(self, new_categories):
        """Update the entire category dictionary."""
        self.categories.update(new_categories)