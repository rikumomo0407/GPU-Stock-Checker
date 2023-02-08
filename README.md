# GPU-Stock-Checker

GPU在庫チェックプログラムです。

パソコン工房,ツクモ,ソフマップ,アーク,アプライド,ドスパラ,PCワンズ,ヨドバシにグラフィックボードが入荷されたらことをチェックし、CSVへの出力やLINE Notifyで通知することができます。

## 実績

・22/12/28 RTX3050 (ツクモ)

・22/12/27 RTX3050 (アーク)

## 使い方

```
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
line_notify_token = '' # LINEトークン
set_notify_how = 1 # LINENotifyへの通知回数[回]
set_notify_rehow = 2 # 在庫の再入荷を通知する 1:有 2:無
```
