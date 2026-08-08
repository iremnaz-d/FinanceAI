
class Categorizer:

    def __init__(self, transaction_list):
        self.dict = {'Shopping': ['defacto', 'trendyol', 'victorias secret', 'shopier' ],
                     'Market': ['carrefour','sok', 'market','tekel', 'migros', 'carrefoursa','gida'],
                     'Transportation': ['izmirim','scooter', 'abonman', 'yandex', 'obilet'],
                     'Food Outside': ['trendyol yemek','getir', 'yemek', 'sepet', 'mcdonalds', 'kantin', 'kebap'],
                     'Drink Outside': ['coffee', 'kafe','cafe', 'kafeterya', 'kahveci' ],
                     'Entertainment': ['bubilet',],
                     'Health': ['eczanesi', 'eczane'],
                     'Personal Payment': ['fast', 'havale'],
                     'Income': ['gönd']
                     }
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

    def get_category_list(self):
        return list(self.dict.keys())