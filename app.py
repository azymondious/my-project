from bottle import Bottle, request, static_file, template
import requests
import os

app = Bottle()

# Wells Fargo API credentials (store sensitive data as environment variables in Render)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Wells Fargo API base URL
BASE_URL = "https://api.wellsfargo.com"


@app.route('/')
def home():
    # Serve the HTML file (index.html)
    return static_file('index.html', root='./templates')


@app.route('/transactions', method='GET')
def fetch_transactions():
    account_id = request.query.account_id  # Get account ID from frontend query string
    url = f"{BASE_URL}/transactions/v1/accounts/{account_id}/transactions"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        transactions = response.json()
        return transactions
    else:
        return {"error": response.text}, response.status_code


@app.route('/analyze-spending', method='POST')
def analyze_spending():
    data = request.json
    transactions = data.get("transactions", [])
    spending = {}

    for txn in transactions:
        category = txn.get("category", "Uncategorized")
        amount = float(txn.get("amount", 0))
        spending[category] = spending.get(category, 0) + amount

    return {"spending": spending}


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')


if __name__ == "__main__":
    # Use host 0.0.0.0 and port from the PORT environment variable (default 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
