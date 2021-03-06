from requests import get
import json
import re
from statistics import stdev, mean
from math import inf

class WarframeItem:
    def __init__(self, item_name):
        self.warframe_api_url = "https://api.warframe.market/v1/items/{}/orders?include=item"
        self.item_name = ""
        self.buyers = []
        self.sellers = []
        self.ducat_value = 0
        self.clean_item_name(item_name)
        #print(self.item_name)
        self.warframe_api_url = self.warframe_api_url.format(self.item_name)
        self.json_data, self.status = self.request_data()
        if self.status == 200:
            self.get_market_data()

    def clean_item_name(self, item_name):
        words = item_name.lower().split(' ')
        for word in ["chassis", "neuroptics", "systems"]:
            if word in words and "blueprint" in words:
                words = words[:-1]
                break

            if 'relic' in words:
                words = words[:-1] + ['intact']

        for word in words:
            self.item_name += re.sub('\W+','', word) + "_"
        self.item_name = self.item_name[:-1]

        return self.item_name
    
    def request_data(self):
        resp = get(self.warframe_api_url)
        json_data = resp.json()

        return json_data, resp.status_code

    def get_market_data(self):
        for order in self.json_data['payload']['orders']:
                if order['user']['status'] == 'ingame' or order['user']['status'] == 'online':
                    if order['order_type'] == 'buy':
                        self.buyers += [order]
                    if order['order_type'] == 'sell':
                        self.sellers += [order]

        return (self.buyers, self.sellers)

    def get_stdev(self, data):
        quantity_scaled_list = []

        if len(data) < 1:
            return 0

        for order in data:
            if order['platinum'] and order['quantity']:
                quantity_scaled_list += [order['platinum']] * order['quantity']
        
        return stdev(quantity_scaled_list)

    def get_mean(self, data):
        quantity_scaled_list = []

        if len(data) == 0:
            return 0

        for order in data:
            if order['platinum'] and order['quantity']:
                quantity_scaled_list += [order['platinum']] * order['quantity']

        return mean(quantity_scaled_list)

    def get_min(self, data):
        lowest = inf

        for order in data:
            lowest = min(order['platinum'], lowest)

        return lowest

    def get_max(self, data):
        highest = 0

        for order in data:
            highest = max(order['platinum'], highest)

        return highest

    def get_ducat_value(self):
        for set_item in self.json_data['include']['item']['items_in_set']:
            if set_item['url_name'] == self.item_name:
                if 'ducats' in set_item:
                    self.ducat_value = set_item['ducats']
                break

        return self.ducat_value

    def get_data(self, buyer_stats=True, seller_stats=True, ducats=True):
        data = {
            'name': self.item_name,
            'uri': self.warframe_api_url,
            'status': self.status
        }

        if self.status == 200:
            data['message'] = ""
            if seller_stats:
                data['seller_stats'] = {
                    'min': "{0:.2f}".format(self.get_min(self.sellers)),
                    'max': "{0:.2f}".format(self.get_max(self.sellers)),
                    'stdev': "{0:.2f}".format(self.get_stdev(self.sellers)),
                    'mean': "{0:.2f}".format(self.get_mean(self.sellers))
                }
            if buyer_stats:
                data['buyer_stats'] = {
                    'min': "{0:.2f}".format(self.get_min(self.buyers)),
                    'max': "{0:.2f}".format(self.get_max(self.buyers)),
                    'stdev': "{0:.2f}".format(self.get_stdev(self.buyers)),
                    'mean': "{0:.2f}".format(self.get_mean(self.buyers))
                }

            if ducats:
                data['ducats'] = self.get_ducat_value()
        else:
            data['message'] = f"No API entry for {self.item_name}"
        
        return data

# item = WarframeItem('Volt Prime Systems')
# print(item.get_data())
