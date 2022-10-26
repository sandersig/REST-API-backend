import time
from flask import Flask, request

app = Flask(__name__)

accounts = {
      1 : {"id" : 1, "name": "Bob", "availableCash": 500},
      2 : {"id" : 2, "name": "Alice", "availableCash": 500}
}

transactions = {
      1 : {"id" : 1,
      "registeredTime" : 1666550252873,
      "executedTime": 1666550259079,
      "success": True,
      "cashAmount": 500,
      "sourceAccount": 1,
      "destinationAccount": 2}
}

#{\"id\" : 1,\"cashAmount\": 500,\"SourceAccount\": 1,\"destinationAccount\": 2}
      
@app.route("/")
def hello():
    return "<p>Hello!</p>"

@app.get('/accounts')
def list_accounts():
   return {"accounts":list(accounts.values())}

@app.get('/transactions')
def list_transactions():
   return {"transactions":list(transactions.values())}

@app.get('/accounts/<accountID>')
def get_account(accountID):
   return accounts[accountID]

@app.get('/transactions/<transactionID>')
def get_transaction(transactionID):
   return transactions[transactionID]

@app.route('/transactions', methods=['GET', 'POST'])
def transactions_route():
   registered_time = round(time.time() * 1000)
   if request.method == 'GET':
       return list_transactions()
   elif request.method == 'POST':
       return create_transaction(request.get_json(force=True), registered_time)

def create_transaction(new_transaction, registered_time):
    transactionID = list(transactions)[-1] + 1
    source_account = new_transaction['sourceAccount']
    dest_account = new_transaction['destinationAccount']
    if new_transaction['cashAmount'] <= get_account(source_account)['availableCash']:
        #set registeredTime
        new_transaction['registeredTime'] = registered_time
        #set success
        new_transaction['success'] = True
        #update source account
        source_account_cash = get_account(source_account)['availableCash'] - new_transaction['cashAmount']
        source_account_name = get_account(source_account)['name']
        update_account(new_transaction['sourceAccount'], {"id" : new_transaction['sourceAccount'], "name": source_account_name, "availableCash": source_account_cash})
        #update destination account
        dest_account_cash = get_account(dest_account)['availableCash'] + new_transaction['cashAmount']
        dest_account_name = get_account(dest_account)['name']
        update_account(new_transaction['destinationAccount'], {"id" : new_transaction['destinationAccount'], "name": dest_account_name, "availableCash": dest_account_cash})
        #set executedTime
        new_transaction['executedTime'] = round(time.time() * 1000)
        new_transaction['id'] = transactionID
        transactions[transactionID] = new_transaction
        return "200 OK. " + str(new_transaction) 
    else:
        return "400 Bad Request. The source account does not have the sufficient amount of cash to proceed with this transaction."
    
"""
@app.route('/accounts/<accountID>', methods=['GET', 'PUT'])
def accounts_route(accountID):
   if request.method == 'GET':
       return list_accounts()
   elif request.method == 'PUT':
       return update_account(accountID, request.get_json(force=True))
"""

def update_account(accountID, new_account_attributes):
    account_to_update = accounts[accountID]
    account_to_update.update(new_account_attributes)
    return accountID

"""
User sends post-request with an transaction. 
Method needs to get info from the source_account and check if there is enough cash. If there is enough cash, update the two accounts.
And return code 200.
If not, return code 400 or similar.
"""