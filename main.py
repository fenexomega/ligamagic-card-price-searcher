#!/usr/bin/python3
#encoding: utf-8

import csv,requests,os,sys
from bs4 import BeautifulSoup

MAX_STORES_PER_CARD = 100

STORES = dict()


def get_card_price(card):
    """
        Gets card price from LIGA MAGIC
    """
    card_name = card['name']
    card_name = card_name.replace(' ','+')
    response = requests.get('https://www.ligamagic.com.br/?view=cards/card&card=' + card_name)
    soup = BeautifulSoup(response.text,'html.parser')
    l = [float(soup.find(id='precos-menor').text[3:].replace(',','.')),\
        float(soup.find(id='precos-medio').text[3:].replace(',','.')),\
        float(soup.find(id='precos-maior').text[3:].replace(',','.'))]
    # get card stores
    divs = soup.findAll("div",{"class":'estoque-linha'})
    for stock_div in divs[:MAX_STORES_PER_CARD]:
        try: 
            link_for_store = stock_div.find("a",{"class":'goto'}).get('href')
            response = requests.get('https://www.ligamagic.com.br/' + link_for_store)
            soup = BeautifulSoup(response.text,'html.parser')
            table = soup.findAll('table')[9]
            rows = table.findAll('tr')[1:]
            for row in rows:
                # print(response.url.split('?')[0])
                cells = [x.text for x in row.find_all('td')]
                if len(cells) < 6 or len(cells) > 7:
                    continue
                language = cells[1].replace('\xa0','')
                #Some sites have a TD with 6 TR, others with 7  
                if len(cells) == 6:
                    quantity = int(cells[3].replace(' unid.',''))
                    try:
                        price    = float(cells[4].replace('R$ ','').replace(',','.'))
                    except ValueError:
                        text = list(filter(None,cells[4].replace('R$ ','').replace(',','.').split('\n')))
                        price = float(min(text))
                else:
                    quantity = int(cells[4].replace(' unid.',''))
                    try:
                        price    = float(cells[5].replace('R$ ','').replace(',','.'))
                    except ValueError:
                        text = list(filter(None,cells[5].replace('R$ ','').replace(',','.').split('\n')))
                        price = float(min(text))
                if quantity >= card['quantity']:
                    store =response.url.split('?')[0]
                    card_obj = {card['name']:{\
                                    'price':price,\
                                    'quantity':quantity,\
                                    'total_price':card['quantity']*price \
                                    }}
                    if not store in STORES:
                        STORES[store] = {'cards':{},'total_cards':0,'total_price':0}
                    if not card['name'] in STORES[store]['cards']:
                        current_store = STORES[store]
                        current_store['cards'].update(card_obj)
                        current_store['total_cards'] += card['quantity']
                        current_store['total_price'] += card_obj[card['name']]['total_price']
                    else:
                        if current_store['cards'][card['name']]['price'] > price:
                            current_store[card['name']] = card_obj
        except KeyboardInterrupt:
            sys.exit(-1)
        except:
            print(f"ERROR FOR: {response.url}")
            continue

        # tr =  soup.find('tr',{'style':'background-color:#F2F2F2'}).find_all('td')
        # tr =  soup.table.find_all('td')
        # info = [x.text for x in tr ]
        # print(info)
    
    return l
    

def read_list(deck_file):
    with open(deck_file) as f:
        content = f.readlines()
        card_list = [x.strip() for x in content]
        card_list = filter(None, card_list) # remove empty lines
    deck = dict()
    deck['quantity'] = 0
    dl = list()
    for l in card_list:
        d = dict()
        qtd_name = l.split(' (')[0] 
        if qtd_name[1] in '0123456789': #if card is like this "20 Mountain"
            d['name'] = qtd_name[3:]
            d['quantity'] = int(l[:2])
        else:
            d['name'] = qtd_name[2:]
            d['quantity'] = int(l[0])
        dl.append(d)
        deck['quantity'] += d['quantity']
    deck['cards'] = dl
    return deck

def get_card_prices(deck):
    deck['max'] = 0
    deck['min'] = 0
    deck['med'] = 0
    for c in deck['cards']:
        print(f"({deck['cards'].index(c)}/{len(deck['cards'])}) - {c['name']}")
        c['price']      = get_card_price(c)
        deck['min'] +=  c['price'][0]*c['quantity']
        deck['med']  +=  c['price'][1]*c['quantity']
        deck['max'] +=  c['price'][2]*c['quantity']
    return deck

def output_list(deck,filename):
    with open(filename,'w',newline='') as csv_file:
        fieldnames = ['name','quantity','price_min','price_med',\
                'price_max','total_min','total_med','total_max']
        writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        for c in deck['cards']:
            csv_file.write("\"{}\",{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n".format(c['name'],c['quantity'],c['price'][0],\
                    c['price'][1],c['price'][2],c['price'][0]*c['quantity'],\
                    c['price'][1]*c['quantity'],c['price'][2]*c['quantity']))
        csv_file.write('\n')
        csv_file.write(f'total min,{deck["min"]:.2f}\n')
        csv_file.write(f'total men,{deck["med"]:.2f}\n')
        csv_file.write(f'total max,{deck["max"]:.2f}\n')

def output_store_list(stores,filename):
    with open(filename,'w',newline='') as csv_file:
        for store in stores:
            csv_file.write(f'{store} - {stores[store]["total_cards"]} \n')
            fieldnames = ['name','quantity','price','total']
            writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
            writer.writeheader()
            for card_name in stores[store]['cards']:
                c = stores[store]['cards'][card_name]
                csv_file.write("\"{}\",{},{:.2f},{:.2f}\n".format(card_name,c['quantity'],c['price'],c['total_price']))
            csv_file.write('\n')
            csv_file.write(f'total,{stores[store]["total_price"]:.2f}\n')
            csv_file.write('\n')
            csv_file.write('\n')



def main():
    if len(sys.argv) < 4 or len(sys.argv) > 4:
        print(f'{sys.argv[0]} decklistfile outputfile.csv stores.csv')
        return
    card_list = read_list(sys.argv[1])
    card_list_prices = get_card_prices(card_list)
    output_list(card_list_prices,sys.argv[2])
    # card_stores = get_stores(card_list_prices)
    output_store_list(STORES,sys.argv[3])
    

if __name__ == "__main__":
    main()

