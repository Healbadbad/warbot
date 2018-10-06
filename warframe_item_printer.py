from tabulate import tabulate
from warframe_item import WarframeItem

class WarframeItemPrinter:
    items = []

    def __init__(self, items):
        self.items = items

    def tabulate(self, buyer_stats=True, seller_stats=True, ducats=True):
        data = []
        for item in self.items:
            # print (item.get_data())
            values = item.get_data()
            data += [[values['name'], values['seller_stats']['mean'], values['seller_stats']['stdev'], values['buyer_stats']['mean'], values['buyer_stats']['stdev'], values['ducats']]]

        # print (data)
        print(tabulate(data, headers=["Name", "Mean Sale Price", "Seller Stdev", "Mean Buy Price", "Buyer Stdev", "Ducats"]))
        
printer = WarframeItemPrinter([WarframeItem('Neo B1 Intact'), WarframeItem('Saryn Prime Chassis Blueprint'), WarframeItem('Tigris Prime Blueprint')])
# item1 = WarframeItem('Saryn Prime Chassis Blueprint')
# item2 = WarframeItem('Volt Prime Blueprint')
# printer = WarframeItemPrinter([item1, item2])
# printer.tabulate()
printer.tabulate()