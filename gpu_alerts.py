import requests
from bs4 import BeautifulSoup
import time

def get_all_items(soup):
    global in_stock
    global out_of_stock
    items = soup.find_all('li', class_='sku-item')

    for item in items:
        try:
            sku_header = item.find_next(class_='sku-header')
            sku_link = 'https://www.bestbuy.com' + sku_header.find_next('a').attrs['href']
            sku_title = sku_header.find_next('a').contents[0]
            sku_button = sku_header.find_next(class_='fulfillment-add-to-cart-button')
            this_button = sku_button.find_next('button')
            if this_button.contents[0] == 'Sold Out':
                out_of_stock[sku_title] = sku_link
            elif this_button.contents[1] == 'Add to Cart':
                in_stock[sku_title] = sku_link
                sent_alert[sku_title] # Add sku to list of alerts that have been sent
                print('***** {} is IN STOCK\nLink: {} *****\n'.format(sku_title, sku_link))
            else:
                continue
        except:
            continue

def send_alert(data):
    webhook = 'https://discord.com/api/webhooks/842075711338184734/3SXJ8usLG6QemYhKPxfltNdM-LCJpQoJWcFEYW_a3qbNqQT158hjlqxvFtncRlJEVgbG'
    this_data = {
        "content": "{} is IN STOCK!!!".format(data[0])
    }

    this_data["embeds"] = [
        {
            "title": "{} is IN STOCK!!!".format(data[0]),
            "url": "{}".format(data[1])
        }
    ]

    returned = requests.post(webhook, json=this_data)
    print(returned.status_code)

if __name__ == "__main__":
    global in_stock
    global out_of_stock
    global sent_alert
    in_stock = {}
    out_of_stock = {}
    sent_alert = []
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    urls = {
        'RTX 3080': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080', 
        'RTX 3070': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070', 
        'RTX 3060Ti': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti', 
        'RTX 3090': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090', 
        'RTX 3060': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060', 
        'RX 6800 XT': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800%20XT', 
        'RX 6800': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206800', 
        'RX 6900 XT': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206900%20XT',
        'RX 6700 XT': 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~AMD%20Radeon%20RX%206700%20XT'
    }

    while True:
        for url in urls.items():
            print('Checking {} inventory...'.format(url[0]))
            response = requests.get(url[1], headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            get_all_items(soup)

        if len(in_stock.items()) == 0:
            print('Nothing is in stock')
            sent_alert = {} # clear out alerts 
        else: # we have in stock items
            for item in in_stock.items():
                if item[0] in sent_alert: # dont send repetative alerts
                    continue
                else:
                    print('{} is IN STOCK\tLink: {}'.format(item[0], item[1]))
                    send_alert(item)
                    sent_alert.append(item[0])
        time.sleep(65)