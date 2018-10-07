import urllib2
from urlparse import urlparse
import requests
from bs4 import BeautifulSoup

def scrape_towns():
    html = urllib2.urlopen("https://suumo.jp/edit/sumi_machi/2018/kanto/")
    soup = BeautifulSoup(html, features="html.parser")
    popular_town_array = []

    town_list = soup.find_all('a', {'class' :'linklist_matrixitem-second'})
    for town in town_list:
        town_text = town.text.replace("\t", "").replace("\r", "").replace("\n", "")
        popular_town_array.append(town_text)

    town_list2 = soup.find_all('div', {'class' :'linklist_subitem-last'})
    for town in town_list:
        town_text = town.text.replace("\t", "").replace("\r", "").replace("\n", "")
        popular_town_array.append(town_text)
    return popular_town_array

def get_real_estate_list(town_name_list):
    all_estate_name_list = {}
    for town_name in town_name_list:
        print("https://www.athome.co.jp/bldg-library/bldname_search/"+town_name.encode('utf-8')+"/")
        print("https://www.sumai-surfin.com/search/result/?prefecture_id=&keyword="+urllib2.quote(town_name.encode('utf-8')))
        response = urllib2.urlopen("https://www.sumai-surfin.com/search/result/?prefecture_id=&keyword="+urllib2.quote(town_name.encode('utf-8')))
        # req.add_header('User-Agent', User_Agent)
        soup = BeautifulSoup(response, features="html.parser")

        estate_name_list = []
        estate_list = soup.find_all('div', {'class' :'p-section__ttl-line'})
        for estate in estate_list:
            estate_name = estate.find('div').find('a').text
            estate_name_list.append(estate_name.encode('utf-8'))
        all_estate_name_list[town_name.encode('utf-8')] = estate_name_list
    return all_estate_name_list

if __name__ == '__main__':
    popular_town_array = scrape_towns()
    print(popular_town_array)
    all_estate_name_list = get_real_estate_list(popular_town_array)
    print(all_estate_name_list["横浜"])
