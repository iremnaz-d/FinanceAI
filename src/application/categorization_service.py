
class Categorizer:

    def __init__(self, transaction_list):
        self.dict = {'Shopping': ['defacto', 'trendyol', 'victorias secret', 'shopier' ],
                     'Market': ['carrefour','sok', 'market','tekel', 'migros', 'carrefoursa','gida'],
                     'Transportation': ['izmirim','scooter', 'abonman', 'yandex', 'obilet'],
                     'Food Outside': ['trendyol yemek','getir', 'yemek', 'sepet', 'mcdonalds', 'kantin', 'kebap'],
                     'Drink Outside': ['coffee', 'kafe','cafe', 'kafeterya', 'kahveci' ],
                     'Entertainment': ['bubilet',],
                     'Health': ['eczanesi', 'eczane'],
                     'Income': ['gönd']
                     }
        self.transaction_list = transaction_list

    def determine_category(self, description):
        for category, list_value in self.dict.items():
           for value in list_value:
               if value.lower() in description.lower():
                   return category
        return 'Other'

    def categorize(self):
        for transaction in self.transaction_list:
            category = self.determine_category(transaction.description)
            transaction.category = category
        return self.transaction_list