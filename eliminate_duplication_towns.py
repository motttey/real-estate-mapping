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

def  get_new_estate_name_list(conn, town_id, eliminate_str):
    # keyの再検討
    estate_detail_list = []
    data_id = 0
    cursor = conn.cursor()

    cursor = conn.cursor()
    try:
        cursor.execute('select * from estate_data where town_id=' + str(town_id) + '')
        results = cursor.fetchall()
        for record in results:
            estate_name = record[2]
            if eliminate_str not in estate_name:
                estate_detail = {}
                estate_detail["name"] = estate_name
                estate_detail["lat"] = record[3]
                estate_detail["lng"] = record[4]
                estate_detail_list.append(estate_detail)
            else:
                print(estate_name)
    finally:
        cursor.close()

    f = codecs.open("output"+str(town_id)+"_new.json", "w", "utf-8")
    json.dump(estate_detail_list, f, ensure_ascii=False)
    return 0;

if __name__ == '__main__':
    root_pass = sys.argv[1]
    town_id = int(sys.argv[2])
    # TODO: 複数キーワード入力に対応
    eliminate_str = sys.argv[3]

    conn = mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        password = root_pass,
        database = 'real_estate',
        auth_plugin='mysql_native_password'
    )
    connected = conn.is_connected()
    print(connected)

    estate_detail_list = get_new_estate_name_list(conn, town_id, eliminate_str)
    conn.close()
