# -*- coding: utf-8 -*-
import urllib.request
import time
import codecs
import sys
import json
import xmltodict
import xml.etree.ElementTree as ET
import mysql.connector
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
    """
    town_list2 = soup.find_all('div', {'class' :'linklist_subitem-last'})
    for town in town_list:
        town_text = town.text.replace("\t", "").replace("\r", "").replace("\n", "")
        popular_town_array.append(town_text)
    """
    return popular_town_array

def get_real_estate_list(town_name_list):
    all_estate_name_list = {}
    init_page = 1
    for town_name in town_name_list:
        response = urllib.request.urlopen("https://www.sumai-surfin.com/search/result/?p="+str(init_page)+"&keyword="+urllib.request.quote(town_name.encode('utf-8')))
        # req.add_header('User-Agent', User_Agent)
        soup = BeautifulSoup(response, features="html.parser")

        estate_name_list = []
        estate_count_str = soup.find('p', {'class' :'pager-count'}).find('span', {'class' :'pager-decimal'}).text
        estate_count = int(estate_count_str)
        page_max = int(estate_count / 10)
        print(estate_count)

        for page_index in range(init_page, page_max, 1):
            time.sleep(1)
            print(page_index)
            print("https://www.sumai-surfin.com/search/result/?p="+str(page_index)+"&keyword="+urllib.request.quote(town_name.encode('utf-8')))
            new_request_response = urllib.request.urlopen("https://www.sumai-surfin.com/search/result/?p="+str(page_index)+"&keyword="+urllib.request.quote(town_name.encode('utf-8')))
            # req.add_header('User-Agent', User_Agent)
            soup_inner = BeautifulSoup(new_request_response, features="html.parser")

            estate_list = soup_inner.find_all('div', {'class' :'p-section__ttl-line'})
            for estate in estate_list:
                estate_name = estate.find('div').find('a').text

                # 物件名に地名が含まれるものに限定
                if town_name in estate_name:
                    estate_name_list.append(estate_name)
            all_estate_name_list[town_name] = estate_name_list
    return all_estate_name_list

def get_geocode_from_estate_name(all_estate_name_list, conn):
    i = 0
    for key, estate_name_list in all_estate_name_list.items():
        estate_detail_list = []
        for estate_name in estate_name_list:
            time.sleep(10)
            estate_detail = {}
            estate_detail["name"] = estate_name

            request = urllib.request.Request("https://www.geocoding.jp/api/?q="+urllib.request.quote(estate_name.encode('utf-8')))
            try:
                with urllib.request.urlopen(request) as response:
                    result_xml = response.read()
                    parse_result = xmltodict.parse(result_xml)
                    result = parse_result["result"]
                    print(parse_result["result"])
                    if "coordinate" in result:
                        estate_detail["lat"] = result["coordinate"]["lat"];
                        estate_detail["lng"] = result["coordinate"]["lng"];
                        print(estate_detail)
                        estate_detail_list.append(estate_detail)
                        i = i + 1

                        # DBへ値を格納
                        print("INSERT INTO estate_data (ID, town_name, estate_name, lat, lng) VALUES ('"+ str(i) +"','"+ key + "','" + estate_detail["name"] + "',"+ estate_detail["lat"] +','+ estate_detail["lng"] +');')

                        cur = conn.cursor()
                        cur.execute("INSERT INTO estate_data (ID, town_name, estate_name, lat, lng) VALUES ('"+ str(i) +"','"+ key + "','" + estate_detail["name"] + "',"+ estate_detail["lat"] +','+ estate_detail["lng"] +');')
                        conn.commit()
                        # table = cur.fetchall()
                        # print(table)

            except urllib.error.HTTPError as e:
                print(e.reason)

            #results = Geocoder(api_key).geocode(estate_name)
            #estate_detail["lat"] = results[0].geometry.location.lat();
            #estate_detail["lng"] = results[0].geometry.location.lng();
        f = codecs.open("output"+key+".json", "w", "utf-8")
        json.dump(estate_detail_list, f, ensure_ascii=False)
    return 0;

if __name__ == '__main__':
    root_pass = sys.argv[1]
    conn = mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        password = root_pass,
        database = 'real_estate',
        auth_plugin='mysql_native_password'
    )
    connected = conn.is_connected()
    print(connected)

    # popular_town_array = scrape_towns()
    popular_town_array = ["国分寺"]
    # print(popular_town_array)
    all_estate_name_list = get_real_estate_list(popular_town_array)
    print(all_estate_name_list)

    estate_detail_list = get_geocode_from_estate_name(all_estate_name_list, conn)
    #f = codecs.open("output.json", "w", "utf-8")
    #json.dump(estate_detail_list, f, ensure_ascii=False)
