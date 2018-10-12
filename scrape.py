# -*- coding: utf-8 -*-
import urllib.request
import time
import codecs
import sys
import json
import xmltodict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from pygeocoder import Geocoder

def scrape_towns():
    html = urllib.request.urlopen("https://suumo.jp/edit/sumi_machi/2018/kanto/")
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
        print("https://www.sumai-surfin.com/search/result/?prefecture_id=&keyword="+urllib.request.quote(town_name.encode('utf-8')))
        response = urllib.request.urlopen("https://www.sumai-surfin.com/search/result/?prefecture_id=&keyword="+urllib.request.quote(town_name.encode('utf-8')))
        # req.add_header('User-Agent', User_Agent)
        soup = BeautifulSoup(response, features="html.parser")

        estate_name_list = []
        estate_list = soup.find_all('div', {'class' :'p-section__ttl-line'})
        for estate in estate_list:
            estate_name = estate.find('div').find('a').text
            estate_name_list.append(estate_name)
        all_estate_name_list[town_name] = estate_name_list
    return all_estate_name_list

def get_geocode_from_estate_name(estate_name_list, api_key):
    estate_detail_list = []
    for estate_name in estate_name_list:
        time.sleep(6)
        estate_detail = {}
        estate_detail["name"] = estate_name

        request = urllib.request.Request("https://www.geocoding.jp/api/?q="+urllib.request.quote(estate_name.encode('utf-8')))
        with urllib.request.urlopen(request) as response:
            result_xml = response.read()
            parse_result = xmltodict.parse(result_xml)
            result = parse_result["result"]
            print(parse_result["result"])
            if "coordinate" in result:
                estate_detail["lat"] = result["coordinate"]["lat"];
                estate_detail["lng"] = result["coordinate"]["lng"];
        #results = Geocoder(api_key).geocode(estate_name)
        #estate_detail["lat"] = results[0].geometry.location.lat();
        #estate_detail["lng"] = results[0].geometry.location.lng();

        print(estate_detail)
        estate_detail_list.append(estate_detail)
    return estate_detail_list;

if __name__ == '__main__':
    api_key = sys.argv[1]

    popular_town_array = scrape_towns()
    print(popular_town_array)
    all_estate_name_list = get_real_estate_list(popular_town_array)
    print(all_estate_name_list)

    estate_detail_list = get_geocode_from_estate_name(all_estate_name_list["恵比寿"], api_key)
    f = codecs.open("output.json", "w", "utf-8")
    json.dump(estate_detail_list, f, ensure_ascii=False)
