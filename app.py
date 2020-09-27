from flask import Flask
from resources.courses import course_api
from resources.reviews import reviews_api
import models

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.register_blueprint(course_api)
app.register_blueprint(reviews_api, url_prefix='/api/v1')


@app.route('/')
def index():
    return "hi l am glen"


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
