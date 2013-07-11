from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object('config.DevConfig')

db = MongoEngine(app)

def register_blueprint(app):
	from blog.views import posts
	app.register_blueprint(posts)

print "register blueprint"
register_blueprint(app)



if __name__ == '__main__':
    app.run()

