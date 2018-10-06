from tabulate import tabulate
from warframe_item import WarframeItem
from collections import OrderedDict

class WarframeItemPrinter:
    items = []

    def __init__(self, items):
        self.items = items

    def tabulate(self, buyer_stats=True, seller_stats=True, ducats=True):
        data = []
        
        for item in self.items:
            values = item.get_data()
            if values['status'] == 200:
                data += [[
                    values['name'],
                    values['seller_stats']['min'],
                    values['seller_stats']['mean'] + u" \u00B1 " + values['seller_stats']['stdev'],
                    values['buyer_stats']['max'],
                    values['buyer_stats']['mean'] + u" \u00B1 " + values['buyer_stats']['stdev'],
                    values['ducats'],
                    values['message']
                ]]
            else:
                data += [[
                    values['name'],
                    0, 0, 0, 0, 0,
                    values['message']
                ]]

        print(tabulate(data, headers=["Name", "Min Sell Price", "Sell Price Average", "Max Buy Price", "Buy Price Average", "Ducats", "Message"]))
        
if __name__ == "__main__()":
    printer = WarframeItemPrinter([WarframeItem('Paris Prime Lower Limb'), WarframeItem('Saryn Prime Chassis Blueprint'), WarframeItem('Tigris Prime Blueprint'), WarframeItem('Forma Blueprint')])
    printer.tabulate()
