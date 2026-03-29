from flask import Flask, render_template
from database import db
from routes import routes
import config

app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init DB
db.init_app(app)

# Register routes
app.register_blueprint(routes)

# Home route
@app.route("/")
def home():
    return render_template("prediction.html")


# 🔥 THIS PART IS MUST
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)