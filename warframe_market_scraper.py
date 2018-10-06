import requests
import json
import statistics

def get_item_market_price(item):
    url = "https://api.warframe.market/v1/items/" + item + "/orders"
    print(url)
    resp = requests.get(url)
    #binary = resp.content
    #data = json.loads(str(binary))
    data = resp.json()
    #print(data)

    buyer_price_list = []
    seller_price_list = []


    for order in data['payload']['orders']:
        if order['user']['status'] == 'ingame' or order['user']['status'] == 'online':
            if order['order_type'] == 'buy':
                buyer_price_list += [order['platinum']]

            if order['order_type'] == 'sell':
                seller_price_list += [order['platinum']]

    buyer_mean = buyer_price_list[0]
    buyer_stdev = 0
    seller_mean = seller_price_list[0]
    seller_stdev = 0

    if (len(buyer_price_list) > 1):
        buyer_stdev = statistics.stdev(buyer_price_list)
        buyer_mean = statistics.mean(buyer_price_list)

    if (len(seller_price_list) > 1):
        seller_stdev = statistics.stdev(seller_price_list)
        seller_mean = statistics.mean(seller_price_list)

    return (buyer_mean, buyer_stdev, seller_mean, seller_stdev)

def get_item_ducats(item):
    url = "https://api.warframe.market/v1/items/" + item + "/orders?include=item"
    resp = requests.get(url)
    data = resp.json()
    ducat_price = 0
    
    for set_item in data['include']['item']['items_in_set']:
        if set_item['url_name'] == item:
            ducat_price = set_item['ducats']
            break

    return ducat_price


#print(get_item_market_price('saryn_prime_systems'))
#print(get_item_market_price('volt_prime_neuroptics'))

#print(get_item_ducats('volt_prime_neuroptics'))
