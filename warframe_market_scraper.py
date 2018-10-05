import requests
import json
import statistics

def get_item_market_price(item):
    url = "https://api.warframe.market/v1/items/" + item + "/orders"
    print (url)
    resp = requests.get(url)
    binary = resp.content
    data = json.loads(binary)

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





print(get_item_market_price('saryn_prime_systems'))
print(get_item_market_price('volt_prime_neuroptics'))