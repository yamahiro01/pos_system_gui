const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

undisplay()
// ツールを表示する関数
eel.expose(display)
function display(){
    control_panel.style.display = "block";
}
// ツールを非表示にする関数
eel.expose(undisplay)
function undisplay(){
    control_panel.style.display = "none";
}

login_btn.addEventListener("click", () => {
    if (employee_no.value != "") {
        alert("いつもお疲れ様です！")
        display()
    } else {
        alert("従業員番号を入力してください")
    }
})


add_order_btn.addEventListener("click", () => {
    if (item_code.value != "" && amount.value != "") {
        eel.add_order_item(item_code.value, amount.value);
    } else {
        alert("商品コードおよび個数の入力は必須です")
    }
})

clear_order_btn.addEventListener("click", () => {
    eel.clear_order();
})

checkout_btn.addEventListener("click", () => {
    if (deposit_money.value == ""){
        alert("お支払い金額が入力されていません");
        return false;
    }
    eel.checkout_order(deposit_money.value);
})


eel.expose(view_order_items)
function view_order_items(text) {
    order_list.value = text;
}

eel.expose(alertJs)
function alertJs(text){
    alert(text)
}
