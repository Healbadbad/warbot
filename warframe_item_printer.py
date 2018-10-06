from tabulate import tabulate
from warframe_item import WarframeItem

class WarframeItemPrinter:
    items = []

    def __init__(self, items):
        self.items = items

    def tabulate(self, buyer_stats=True, seller_stats=True, ducats=True):
        data = []
        for item in self.items:
            values = item.get_data()
            data += [[values['name'], values['seller_stats']['min'], values['seller_stats']['mean'] + u" \u00B1 " + values['seller_stats']['stdev'], values['buyer_stats']['max'], values['buyer_stats']['mean'] + u" \u00B1 " + values['buyer_stats']['stdev'], values['ducats']]]

        print(tabulate(data, headers=["Name", "Min Sell Price", "Sell Price Average", "Buy Price Max", "Buy Price Average", "Ducats"]))
        
printer = WarframeItemPrinter([WarframeItem('Neo B1 Intact'), WarframeItem('Saryn Prime Chassis Blueprint'), WarframeItem('Tigris Prime Blueprint')])

printer.tabulate()