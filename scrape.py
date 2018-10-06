import urllib2
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

if __name__ == '__main__':
    popular_town_array = scrape_towns()
    print(popular_town_array)
