from bottle import Bottle, run, request, static_file
import os

# Initialize the Bottle app
app = Bottle()

# Route: Serve the homepage
@app.route('/')
def home():
    # Serve the index.html from the "views" folder
    return static_file('index.html', root='./views')

# Route: Serve the About page
@app.route('/about')
def about():
    # Serve the about.html from the "views" folder
    return static_file('about.html', root='./views')

# Route: Serve static files (optional, if you have assets like CSS/JS)
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
