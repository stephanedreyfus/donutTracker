"""Models for Donut app."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

DEFAULT_IMAGE = "https://tinyurl.com/my-jelly-donut"


class Donut(db.Model):
    """Donut."""

    __tablename__ = "donuts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)

    def to_dict(self):
        """Serialize donut to a dict of donut info."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image,
            }


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
