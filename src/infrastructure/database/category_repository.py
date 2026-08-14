import json

class CategoryRepository:
    """
    This class is a direct controller for the config/category_mappings.json which contains a
    dictionary for the categories and their keywords.
    """

    @staticmethod
    def get_category_dict():
        with open("src/config/category_mappings.json", "r", encoding = "utf-8") as f:
            return json.load(f)

    def add_new_category(self, category):
        category = category.title()
        d = self.get_category_dict()

        if category in d:
            return False
        else:
            d[category] = category
            with open("src/config/category_mappings.json", "w", encoding = "utf-8") as f:
                json.dump(d,f, indent = 4, ensure_ascii = False)
            return True

    def delete_category(self, category):
        d = self.get_category_dict()

        if category in d:
            del d[category]
            with open("src/config/category_mappings.json", "w", encoding = "utf-8") as f:
                json.dump(d,f, indent = 4, ensure_ascii = False)
            return True

        else:
            return False