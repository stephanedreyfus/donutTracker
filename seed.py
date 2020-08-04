# from app import app
from models import db, Donut


db.drop_all()
db.create_all()

c1 = Donut(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Donut(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://bargainhuntingmomma.files.wordpress.com/2014/05/donut.jpg"
)

db.session.add_all([c1, c2])
db.session.commit()
