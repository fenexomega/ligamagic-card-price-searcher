#!/usr/bin/python3
#encoding: utf-8

import csv,requests,os,sys
from bs4 import BeautifulSoup

def get_card_price(card_name):
    """
        Gets card price from LIGA MAGIC
    """
    print(card_name)
    card_name = card_name.replace(' ','+')
    response = requests.get('https://www.ligamagic.com.br/?view=cards/card&card=' + card_name)
    soup = BeautifulSoup(response.text,'html.parser')
    l = [float(soup.find(id='precos-menor').text[3:].replace(',','.')),\
        float(soup.find(id='precos-medio').text[3:].replace(',','.')),\
        float(soup.find(id='precos-maior').text[3:].replace(',','.'))]
    return l
    

def read_list(deck_file):
    with open(deck_file) as f:
        content = f.readlines()
        card_list = [x.strip() for x in content]
        card_list = filter(None, card_list) # remove empty lines
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
    return dl

def get_card_prices(deck_list):
    deck = dict()
    deck['max'] = 0
    deck['min'] = 0
    deck['med'] = 0
    for c in deck_list:
        c['price']      = get_card_price(c['name'])
        deck['min'] +=  c['price'][0]*c['quantity']
        deck['med']  +=  c['price'][1]*c['quantity']
        deck['max'] +=  c['price'][2]*c['quantity']
    deck['cards'] = deck_list
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
        csv_file.write(f'total min,{deck["med"]:.2f}\n')
        csv_file.write(f'total min,{deck["max"]:.2f}\n')


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print(f'{sys.argv[0]} decklistfile outputfile.csv [pt]')
        return
    card_list = read_list(sys.argv[1])
    card_list_prices = get_card_prices(card_list)
    output_list(card_list_prices,sys.argv[2])
    

if __name__ == "__main__":
    main()
