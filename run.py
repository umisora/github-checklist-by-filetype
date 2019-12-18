from main import app
import os
if __name__ == "__main__":
    PORT = os.getenv('PORT', '8000')
    app.run(debug=True, host='0.0.0.0', port=PORT)
