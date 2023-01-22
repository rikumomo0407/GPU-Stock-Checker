from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
import keyboard as ky
import csv
import datetime
import requests
import os


site_1 = ['パソコン工房','https://www.pc-koubou.jp/user_data/search.php?searchbox=1&q=RTX%203050&s5[]=0&path=%E8%87%AA%E4%BD%9CPC%E3%83%91%E3%83%BC%E3%83%84&limit=20&sort=Score&limit=20',1,1,'/html/body/div[2]/main/div/div/article/header/div/div[3]/div/ul/li[2]/label/span','','']
site_2 = ['ツクモ','https://shop.tsukumo.co.jp/search/c20:2018:2018200:201820088000400/?keyword=3050',1,1,'/html/body/div[4]/div/main/div/div[1]/div[1]/div/span[1]','','']
site_3 = ['ソフマップ','https://www.sofmap.com/search_result.aspx?gid=001030060&keyword=RTX+3050&keyword_not=&price_from=&price_to=',1,1,'/html/body/div[8]/main/section/section[2]/p/span','','']
site_4 = ['アーク','https://www.ark-pc.co.jp/search/?category=c25&p3=h25031&p6=w25302',1,1,'/html/body/div[6]/div[1]/div/div[2]/div[1]/div[1]/ul/li','','']
site_5 = ['アプライド','https://shop.applied-net.co.jp/shopbrand/ct2358/page1/order/',3,4,'/html/body/div[3]/div/main/article/section/div/div[4]/ul[',']/li[',']/div/div[2]/p[1]/a']
site_6 = ['ドスパラ','https://www.dospara.co.jp/5search/search.php?ft=3050&search_for=category&sort=&cate=bg1&br=31&sbr=1487',1,1,'/html/body/div[4]/div[1]/div[2]/div/div/div[2]/form/div[1]/span','','']
site_7 = ['PCワンズ','https://www.1-s.jp/products/list/252?mode=search&name=RTX%203050&name_op=AND&size=20',1,1,'/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/div[2]/ul/li[1]','','']
site_8 = ['ヨドバシ','https://www.yodobashi.com/category/19531/252001/250035/?sorttyp=NEW_ARRIVAL_RANKING',1,10,'/html/body/div[1]/div[5]/div/div[1]/div/div[3]/div[3]/div[','',']/a/div[2]/p[2]']

site_all = [site_1,site_2,site_3,site_4,site_5,site_6,site_7,site_8]


#設定
product_name = 'RTX3050' #商品名
product_keyword_a = 'RTX' #キーワード1
product_keyword_b = '3050' #キーワード2
set_i = 1 # スクレイピング回数設定 1:有 2:無(停止しない)
set_i_how = 1 # スクレイピング回数[回]
set_wait = 1 # スクレイピング待機時間[s]
set_csv = 1 # CSV出力 1:有 2:無
set_web_open = 1 # Webを開く 1:有 2:無 (無しはエラー)
set_web_size = [1000,1000] # Webのサイズ (x,y)
set_csv_open = 2 # CSVを開く 1:有 2:無
set_notify = 2 # LINENotifyに通知を送信 1:有 2:無
line_notify_token = 'SwB5P7J4GXHp2QWrqr2YjgkChKxKsf7HQ1ZTLbCxgVY' # LINEトークン
set_notify_how = 1 # LINENotifyへの通知回数[回]
set_notify_rehow = 2 # 在庫の再入荷を通知する 1:有 2:無


#設定の適用
options = Options()
if set_web_open == 2:
    options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver.exe',options=options)

if set_csv == 1:
    csv_date = datetime.datetime.today().strftime("%Y-%m-%d %H%M%S")
    csv_file_name = os.getcwd() + '\\' + product_name + '_' + csv_date + '.csv'
    f = open(csv_file_name, 'w', encoding='cp932', errors='ignore')
    writer = csv.writer(f, lineterminator='\n')
    csv_header = ["日付","時間",site_1[0],site_2[0],site_3[0],site_4[0],site_5[0],site_6[0],site_7[0],site_8[0]]
    writer.writerow(csv_header)

driver.set_window_size(set_web_size[0],set_web_size[1])


#関数
def scraping(shoplist):
    driver.get(shoplist[1])
    result = 0
    for x in range(shoplist[2]):
        for y in range(shoplist[3]):
            if (shoplist[2] and shoplist[3]) == 1:
                diva_str = ''
                divb_str = ''
            elif (shoplist[2] or shoplist[3]) == 1:
                diva_str = str(y+1)
                divb_str = ''
            else:
                diva_str = str(y+1)
                divb_str = str(x+1)
            for res in driver.find_elements_by_xpath(shoplist[4] + diva_str + shoplist[5] + divb_str + shoplist[6]):
                if shoplist[2] and shoplist[3] == 1:
                    result = re.sub(r'\D', '', res.text[:2])
                else:
                    index = res.text.find(product_keyword_a and product_keyword_b)
                    if index != -1:
                        result += 1
            if result is None:
                return 0
            else:         
                return int(result)


#スクレイピング
i = set_i_how + 1
list_notify_how = [0]*len(site_all)
while True:

    time.sleep(set_wait)

    if set_csv == 1:
        csvlist = []
        csvlist.append(datetime.datetime.today().strftime("%Y-%m-%d"))
        csvlist.append(datetime.datetime.today().strftime("%H") + ":" + datetime.datetime.today().strftime("%M") + ":" + datetime.datetime.today().strftime("%S"))

    print('---------------------------------------------')
    print(datetime.datetime.today().strftime("%H") + ":" + datetime.datetime.today().strftime("%M") + ":" + datetime.datetime.today().strftime("%S") + '  ' + str(i-set_i_how) + '回目の' + product_name + "のスクレイピング結果")
    print('---------------------------------------------')

    for list_i in range(0,len(site_all)):
        result = scraping(site_all[list_i])
        print(site_all[list_i][0],end='')
        if result >= 10 and site_all[list_i][2]*site_all[list_i][3] != 1:
            print(':9+個入荷')
        elif result == 0:
            print(':在庫なし')
        else:
            print(':' + str(result) + '個入荷')
        if set_csv == 1:
            if result == 0:
                csvlist.append('在庫なし')
            else:
                csvlist.append(str(result))
        if (set_notify == 1) and (result >= 1) and (list_notify_how[list_i] < set_notify_how):
            line_message = product_name + 'が' + site_all[list_i][0] + 'に' + str(result) + '個入荷しました!!'
            headers = {'Authorization': f'Bearer {line_notify_token}'}
            data = {'message': f' {line_message}'}
            requests.post('https://notify-api.line.me/api/notify', headers = headers, data = data)
            list_notify_how[list_i] += 1
        if (set_notify_rehow == 1) and (list_notify_how[list_i] >= 0) and (result == 0):
            list_notify_how[list_i] = 0
        driver.refresh()

    if set_csv == 1:
        writer.writerow(csvlist)

    if set_i == 2:
        set_i_how -= 1
        if ky.is_pressed("s"):
            break
    else:
        if set_i_how == 1:
            break
        else:
            set_i_how -= 1


#プログラムの終了
if set_csv == 1:
    f.close()

driver.close()