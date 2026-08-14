from src.infrastructure.database.category_repository import CategoryRepository

class Categorizer:

    def __init__(self, transaction_list):
        self.repo = CategoryRepository()
        self.dict = self.repo.get_category_dict() #category dictionary contains words that are definitely included in certain categories
        self.transaction_list = transaction_list

    def determine_category(self, description):
        """
        :param description: Transaction description (str)
        :return: best category for given description
        """
        max_match_length = 0
        best_category = 'Other' #If no appropriate category can be found, it will be labeled as “Other”
        for category, list_value in self.dict.items():
           for value in list_value:
               if value.lower() in description.lower() and len(value) > max_match_length:
                   best_category = category
                   max_match_length = len(value) #to distinguish situations like Trendyol/Trendyol Yemek
        return best_category

    def categorize(self):
        """
        Using the determine_category method, adds the categories of all transactions
        :return: categorized transaction list
        """
        for transaction in self.transaction_list:
            category = self.determine_category(transaction.description)
            # Regardless of its previous classification, if the amount is positive, it is classified as Income
            if transaction.amount > 0:
                category = 'Income'
            transaction.category = category
        return self.transaction_list

class CategoryService:
    """
    This that connects to the CategoryRepository and acts as a bridge between it and the interface
    """

    def __init__(self):
        self.repo = CategoryRepository()
        self.dict = self.repo.get_category_dict()


    def get_category_list(self):
        return list(self.dict.keys())

    def add_new_category(self, category):
        return self.repo.add_new_category(category)

    def delete_category(self, category):
        return self.repo.delete_category(category)
