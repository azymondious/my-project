from bottle import Bottle, request, run, static_file, template
import requests

app = Bottle()

# Wells Fargo API credentials (Replace with actual credentials)
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
ACCESS_TOKEN = "your_access_token"

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
    # Example: Analyze and categorize spending
    data = request.json
    transactions = data.get("transactions", [])
    spending = {}

    for txn in transactions:
        category = txn.get("category", "Uncategorized")
        amount = float(txn.get("amount", 0))
        spending[category] = spending.get(category, 0) + amount

    return {"spending": spending}


# Serve static files (e.g., CSS, JS) if needed
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080, debug=True)
