from app import create_app
from flask import session

app = create_app()
first_request = True

@app.before_request
def clear_sessions():
    global first_request
    if first_request:
        session.clear()
        first_request = False

if __name__ == '__main__':
    app.run(debug=True)
