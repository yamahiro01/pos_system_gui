'''
## １
課題３で作成したデスクトップUIを参考に、POSシステム用のUIを作成してください （必要な項目：商品コード入力欄、個数入力欄、入力した商品情報の表示欄、お預かり金額入力欄、合計金額の表示欄など） 　※必要と判断した項目は追加いただいて構いません

## ２
UIとPython側を連動させて、POSシステムのデスクトップアプリ版を完成させてください

## ３（発展版）
マスタデータ（商品コード、商品名、価格）をCSVファイルから読み込んで登録できるようにしてください

## ４（発展版）
このPOSシステムに不足している機能を１つ考えて追加してください
'''
import pandas as pd
import datetime
import os

RECEIPT_FOLDER="./receipt"
os.makedirs(RECEIPT_FOLDER, exist_ok=True)

class Item:
    '''
    商品１つを管理するためのクラス
    '''
    def __init__(self,item_code:str,item_name:str,price:int) -> None:
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self) -> int:
        return self.price


class Order:
    '''
    １つのオーダーを管理するためのクラス
    '''
    def __init__(self,item_master:list) -> None:
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        self.set_datetime()
        
    def set_datetime(self) -> None:
        '''
        現在の時刻をオーダーにセットする
        '''
        self.datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    
    def calc_sum_item_price(self):
        sum_item_price = 0
        for item,count in zip(self.item_order_list,self.item_count_list):
            for master in self.item_master:
                if item == master.item_code:
                    sum_item_price += master.price * count
                    break
        
        return sum_item_price
            
    def add_item_order(self,item_code:str,item_count:int) -> bool:
        '''
        オーダーに商品を追加する
        '''
        if self.get_item_data(item_code)[0]:
            self.item_order_list.append(item_code)
            self.item_count_list.append(item_count)
            return True
        else:
            return False
            
    def view_item_list(self) -> None:
        '''
        オーダーに登録されている全商品のコードを表示する
        '''
        for item in self.item_order_list:
            print(f"商品コード:{item}")
            
    # オーダー番号から商品情報を取得する（課題１）
    def get_item_data(self,item_code):
        for m in self.item_master:
            if item_code==m.item_code:
                return m.item_name, m.price
        return None, None
    
    # オーダー入力　課題２，４
    def input_order(self) -> None:
        '''
        オーダーに登録されている全商品のコードを表示する
        '''
        while True:
            buy_item_code=input("購入したい商品を入力してください。登録を完了する場合は、0を入力してください >>> ")
            if int(buy_item_code)!=0:
                # マスタに存在するかチェック(課題外：カスタマイズ)
                check=self.get_item_data(buy_item_code)
                if check!=None:
                    print(f"{check[0]} が登録されました")
                    buy_item_count=input("個数を入力してください　>>> ")
                    self.add_item_order(buy_item_code,buy_item_count)
                else:
                    print(f"「{buy_item_code}」は商品マスタに存在しません")
            else:
                print("商品登録を終了します。")
                break    
    
    def export_receipt(self, deposit_money: int, change_money: int):
        '''
        レシート出力
        '''
        number=1
        self.sum_price=0
        self.sum_count=0
        self.receipt_name=f"receipt_{self.datetime}.log"
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("オーダー登録された商品一覧\n")
        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            result=self.get_item_data(item_order)
            self.sum_price+=result[1]*int(item_count)
            self.sum_count+=int(item_count)
            receipt_data=f"{number}.{result[0]}({item_order}) : ￥{result[1]:,}　{item_count}個 = ￥{int(result[1])*int(item_count):,}"
            self.write_receipt(receipt_data)
            number+=1
            
        # 合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        self.write_receipt(f"合計金額:￥{self.sum_price:,} {self.sum_count}個")
        self.write_receipt(f"お預かり金額:￥{deposit_money:,}")
        self.write_receipt(f"お返し:￥{change_money:,}")
    
    def checkout(self, money):
        '''
        会計処理しお釣りの金額を返す
        '''
        change_money=int(money)-self.calc_sum_item_price()
        
        return change_money
        
    def write_receipt(self,text:str):
        '''
        レシートに１行出力する
        '''
        print(text)
        with open(RECEIPT_FOLDER + "\\" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n") 
    
    
    def get_order_items(self):
        '''
        オーダーの全情報をテキストをして取得する
        '''
        res = ""
        num = 1
        total_price = 0
        total_count = 0
        for item_code,count in zip(self.item_order_list,self.item_count_list):
            for item in self.item_master:
                if item.item_code == item_code:
                    res += f"{num} | {item_code} {item.item_name} | ￥{item.price}円 × {count} 個\n"
                    num += 1
                    total_price += item.price * count
                    total_count += count
                    break   
        res += "---------------------------------------------\n"
        res += f"合計: ￥{total_price}円 | {total_count}個\n"
        
        return res
        
class PosSystem():
    '''
    POSシステム全体を管轄するClass
    '''
    
    def __init__(self, csv_path:str=None):
        self.item_master = []
        self.csv_path = csv_path
        self.order = None
        
    # マスタ登録(課題３)
    def add_item_master(self):
        '''
        POSシステムに商品マスタを登録する
        '''
        print("------- マスタ登録開始 ---------")
        count=0
        try:
            item_master_df=pd.read_csv(self.csv_path,dtype={"item_code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
            for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
                self.item_master.append(Item(item_code,item_name,price))
                print("{}({})".format(item_name,item_code))
                count+=1
            print("{}品の登録を完了しました。".format(count))
            print("------- マスタ登録完了 ---------")
            return True
        except:
            print("マスタ登録が失敗しました")
            print("------- マスタ登録完了 ---------")
            return False
        
    def init_order(self):
        '''
        オーダーを初期化する
        '''
        self.order = Order(self.item_master)
        