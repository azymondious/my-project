import os
from bottle import Bottle, run, template

# Define the port dynamically for Render
port = int(os.environ.get('PORT', 4000))
app = Bottle()

@app.route('/')
def index():
    return template('index')

@app.route('/about')
def about():
    return template('about')

if __name__ == "__main__":
    # Use the dynamically set port
    run(app, host='0.0.0.0', port=port, debug=True)