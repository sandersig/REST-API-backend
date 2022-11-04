import time
from flask import Flask, request

app = Flask(__name__)

accounts = {
      1 : {"id" : 1, "name": "Bob", "availableCash": 10000},
      2 : {"id" : 2, "name": "Alice", "availableCash": 5000},
      3 : {"id" : 3, "name": "Knut", "availableCash": 0},
      4 : {"id" : 4, "name": "Kari", "availableCash": 3000}
}

transactions = {
      1 : {'cashAmount': 500,
           'sourceAccount': 1,
           'destinationAccount': 2,
           'registeredTime': 1666801616523,
           'success': True,
           'executedTime': 1666801616524,
           'id': 1}
}
      
@app.route("/")
def hello():
    return "<p>API for transactions between bank accounts!</p>"

@app.get('/accounts')
def list_accounts():
   return {"accounts":list(accounts.values())}

@app.route('/transactions', methods=['GET', 'POST'])
def transactions_route():
   registered_time = round(time.time() * 1000)
   if request.method == 'GET':
       return {"transactions":list(transactions.values())}
   elif request.method == 'POST':
       return create_transaction(request.get_json(force=True), registered_time)

def get_account(accountID):
   return accounts[accountID]

"""
Function that updates the accounts according to the transaction
"""
def update_accounts(new_transaction):
    #update source account
    source_account_to_update = accounts[new_transaction['sourceAccount']]
    source_account_name = get_account(new_transaction['sourceAccount'])['name']
    source_account_cash = get_account(new_transaction['sourceAccount'])['availableCash'] - new_transaction['cashAmount']
    new_account_attributes = {"id" : new_transaction['sourceAccount'], "name": source_account_name, "availableCash": source_account_cash}
    source_account_to_update.update(new_account_attributes)
    #update dest account
    dest_account_to_update = accounts[new_transaction['destinationAccount']]
    dest_account_cash = get_account(new_transaction['destinationAccount'])['availableCash'] + new_transaction['cashAmount']
    dest_account_name = get_account(new_transaction['destinationAccount'])['name']
    new_account_attributes = {"id" : new_transaction['destinationAccount'], "name": dest_account_name, "availableCash": dest_account_cash}
    dest_account_to_update.update(new_account_attributes)


def create_transaction(new_transaction, registered_time):
    transactionID = list(transactions)[-1] + 1
    source_account = new_transaction['sourceAccount']
    if new_transaction['cashAmount'] <= get_account(source_account)['availableCash']:
        update_accounts(new_transaction)
        new_transaction['registeredTime'] = registered_time
        new_transaction['executedTime'] = round(time.time() * 1000)
        new_transaction['id'] = transactionID 
        new_transaction['success'] = True
        transactions[transactionID] = new_transaction
        return new_transaction