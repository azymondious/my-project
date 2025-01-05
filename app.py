from bottle import Bottle, run, request, static_file
import os
import json

# Initialize the Bottle app
app = Bottle()

# Route: Serve the homepage
@app.route('/')
def home():
    return static_file('index.html', root='./templates')

# Route: Fetch transactions (dummy data for now)
@app.route('/transactions')
def get_transactions():
    account_id = request.query.get('account_id')
    # Replace this with a real API call to fetch transactions
    transactions = [
        {"date": "2025-01-01", "description": "Groceries", "amount": 54.99},
        {"date": "2025-01-02", "description": "Gas Station", "amount": 40.00},
        {"date": "2025-01-03", "description": "Coffee Shop", "amount": 5.50},
    ]
    return {"transactions": transactions}

# Route: Analyze spending (dummy analysis for now)
@app.route('/analyze-spending', method='POST')
def analyze_spending():
    data = request.json
    transactions = data.get("transactions", [])
    
    # Simple analysis: Sum amounts by category
    spending = {}
    for txn in transactions:
        category = txn.get("description", "Other")
        amount = float(txn.get("amount", 0))
        if category in spending:
            spending[category] += amount
        else:
            spending[category] = amount

    return {"spending": spending}

# Route: Serve static files (e.g., CSS, JS)
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

# Error Handler for 404
@app.error(404)
def error404(error):
    return "The page you're looking for does not exist. Check the URL and try again."

# Run the app when executed directly
if __name__ == "__main__":
    # Use host "0.0.0.0" and a dynamic port from Render (or default to 8080 locally)
    port = int(os.getenv("PORT", 8080))
    run(app, host="0.0.0.0", port=port, debug=True)
