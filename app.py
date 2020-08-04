"""Flask app for Donuts"""

from flask import Flask, render_template, jsonify, request

from models import db, connect_db, Donut

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///donuts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "too-much-sugar"

connect_db(app)


@app.route("/")
def root():
    """Render homepage."""

    return render_template("index.html")


@app.route("/api/donuts")
def see_donuts():
    """Return all donuts in system.

    Returns JSON like:
        {donuts: [{id, flavor, rating, size, image}, ...]}
    """

    donuts = [donut.to_dict() for donut in Donut.query.all()]
    return jsonify(donuts=donuts)


@app.route("/api/donuts", methods=["POST"])
def create_donut():
    """Add a donut, and return data about the new donut.

    Return JSON like:
        {donut: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    donut = Donut(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None,
    )

    db.session.add(donut)
    db.session.commit()

    return (jsonify(donut=donut.to_dict()), 201)


@app.route("/api/donuts/<int:donut_id>")
def get_donut(donut_id):
    """Return data on a specific donut.

    Returns JSON like:
        {donut: [{id, flavor, rating, size, image}]}
    """

    donut = Donut.query.get_or_404(donut_id)
    return jsonify(donut=donut.to_dict())


@app.route("/api/donuts/<int:donut_id>", methods=["PATCH"])
def update_donut(donut_id):
    """Update and then return data on a specific donut.

    Returns JSON like:
        {donut: [{id, flavor, rating, size, image}]}
    """

    donut = Donut.query.get_or_404(donut_id)
    data = request.json

    donut.flavor = data['flavor']
    donut.rating = data['rating']
    donut.size = data['size']
    donut.image = data['image']

    db.session.add(donut)
    db.session.commit()

    return (jsonify(donut=donut.to_dict()))


@app.route("/api/donuts/<int:donut_id>", methods=["DELETE"])
def delete_donut(donut_id):
    """Delete a specific donut.

    Returns JSON like:
        {message: "{flavor} donut deleted."}
    """

    donut = Donut.query.get_or_404(donut_id)
    name = donut.flavor

    db.session.delete(donut)
    db.session.commit()

    return jsonify(message=f"{name} donut deleted.")
