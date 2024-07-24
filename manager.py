
from flask_migrate import Migrate
from flask.cli import FlaskGroup

# app = Flask(__name__)
# db = SQLAlchemy(app)
from app import app,db
migrate = Migrate(app, db)

cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()
