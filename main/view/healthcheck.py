from main import app


@app.route('/', methods=['GET'])
def ping():
    return "Hello World!!", 200
