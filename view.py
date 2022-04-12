import eel 

import common.desktop as desktop
from pos_system import PosSystem

# フォルダ名
app_name = "html"
end_point = "index.html"
size = (700,600)

#ystem:PosSystem

ITEM_MASTER_CSV_PATH="./item_master.csv"

'''
HTML側とのやり取りは全てview.pyファイルに纏めている
これにより、pos.py側はeelに依存する必要がなくなり
再利用性が高まる
'''

@eel.expose
def add_order_item(item_code:str,amount:str):
    '''
    オーダーに商品を追加する
    '''
    global system
    # Orderが存在しなければOrderインスタンスを作成
    if system.order == None:
        system.init_order()
    res = system.order.add_item_order(item_code, int(amount))
    if not res:
        eel.alertJs(f"『{item_code}』は商品マスターに登録されていません")
    else:
        res_text = system.order.get_order_items()
        eel.view_order_items(res_text)
    
    
@eel.expose
def checkout_order(money: str):
    '''
    会計処理
    '''
    global system
    change_money = system.order.checkout(int(money))
    if change_money < 0:
        message = f"金額が {-change_money}円 不足しています。"
    else:
        message = f"{change_money}円のお返しです。\nお買い上げありがとうございました。"
        system.order.export_receipt(deposit_money=int(money), change_money=change_money)
        system.init_order()
    eel.alertJs(message)


@eel.expose
def clear_order():
    global system
    system.init_order()
    eel.view_order_items("")


def init_pos_system():
    '''
    POSシステムの初期化処理
    '''
    global system # グローバル変数を使用する場合の宣言
    
    # POSシステムに商品マスタを登録
    system = PosSystem(ITEM_MASTER_CSV_PATH)
    system.add_item_master() # CSVからマスタへ登録


if __name__ == "__main__":
    init_pos_system()
    desktop.start(app_name,end_point,size)