from src.infrastructure.database.category_repository import CategoryRepository

class Categorizer:

    def __init__(self, transaction_list):
        self.repo = CategoryRepository()
        self.dict = self.repo.get_category_dict()
        self.transaction_list = transaction_list

    def determine_category(self, description):
        max_match_length = 0
        best_category = 'Other'
        for category, list_value in self.dict.items():
           for value in list_value:
               if value.lower() in description.lower() and len(value) > max_match_length:
                   best_category = category
                   max_match_length = len(value)
        return best_category

    def categorize(self):
        for transaction in self.transaction_list:
            category = self.determine_category(transaction.description)
            if transaction.amount > 0:
                category = 'Income'
            transaction.category = category
        return self.transaction_list

class CategoryService:

    def __init__(self):
        self.repo = CategoryRepository()
        self.dict = self.repo.get_category_dict()


    def get_category_list(self):
        return list(self.dict.keys())

    def add_new_category(self, category):
        return self.repo.add_new_category(category)

    def delete_category(self, category):
        return self.repo.delete_category(category)
