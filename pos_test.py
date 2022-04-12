from pos import Order

def test_write_order():
    Order.write_order("商品A","10")
    
def test_view_order_list():
    print(Order.view_order_list())
    
    