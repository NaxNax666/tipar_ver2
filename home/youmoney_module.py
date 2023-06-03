from yoomoney import Authorize, Client,Quickpay

def popolny(amount, label):
    quickpay = Quickpay(
            receiver="YOU YOUMONEY BILL HERE",
            quickpay_form="shop",
            targets="1RUB - 1TETH",
            paymentType="SB",
            sum=amount,
            label=label
            )
    return [quickpay.base_url, quickpay.redirected_url]

def check_payment(label):
    token = "YOUR TOKEN HERE"
    client = Client(token)
    print("lol")
    print(client.account_info())
    history = client.operation_history(label=label)
    print(history.operations[0].status)
    return history.operations[0].status =="success"

def getamount(label):
    token = "YOUR TOKEN HERE"
    client = Client(token)
    print("lol")
    print(client.account_info())
    history = client.operation_history(label=label)
    print(history.operations[0].amount)
    return history.operations[0].amount
