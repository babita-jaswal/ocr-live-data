from app import create_app
from flask import Flask


app = create_app()

if __name__ == '__main__':
    # app.run(host='192.168.1.70', port=5000, debug=True)
    app.run(host='0.0.0.0', port=8000, debug=True)