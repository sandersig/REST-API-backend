# REST-API-backend

## How to set up:
1. Clone/download the repository
2. Navigate to the folder
3. Type <code>python3 -m venv venv</code> to set up a virtual environment.
4. Run <code>pip install flask</code> to install flask

## How to test the API:
I have done my testing using curl in the terminal.
1. To create a new transaction, you can for example type <code>curl -X POST -d "{\"cashAmount\": 500,\"sourceAccount\": 2,\"destinationAccount\": 1}" http://127.0.0.1:5000/transactions</code>
This transaction will return the status code "200 OK" together with the executed transaction model.
If the transaction did not go through (not enough cash on the source account), the API will return the status code 400 BAD REQUEST together with an error message.
2. To see if the transaction was correctly registered, you can use <code>curl http://127.0.0.1:5000/transactions</code>.
3. Similarly to check if the accounts have been updated after the transaction has been completed, you can type <code>curl http://127.0.0.1:5000/accounts</code>.
