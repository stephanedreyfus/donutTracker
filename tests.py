from unittest import TestCase

from app import app
from models import db, Donut

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///donut_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


DONUT_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/donut.jpg"
}

DONUT_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/donut2.jpg"
}

# Updating two entries on DONUT_DATA: flavor, and image.
DONUT_UPDATE = {
    "flavor": "UpdatedFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/update.jpg"
}


class DonutViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Donut.query.delete()

        donut = Donut(**DONUT_DATA)
        db.session.add(donut)
        db.session.commit()

        self.donut = donut

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_donuts(self):
        with app.test_client() as client:
            resp = client.get("/api/donuts")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "donuts": [
                    {
                        "id": self.donut.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/donut.jpg"
                    }
                ]
            })

    def test_get_donut(self):
        with app.test_client() as client:
            url = f"/api/donuts/{self.donut.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "donut": {
                    "id": self.donut.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/donut.jpg"
                }
            })

    def test_get_non_donut(self):
        with app.test_client() as client:
            url = "/api/donuts/9999999"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 404)

    def test_create_donut(self):
        with app.test_client() as client:
            url = "/api/donuts"
            resp = client.post(url, json=DONUT_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['donut']['id'], int)
            del data['donut']['id']

            self.assertEqual(data, {
                "donut": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/donut2.jpg"
                }
            })

            self.assertEqual(Donut.query.count(), 2)

    def test_update_donut(self):
        with app.test_client() as client:
            # If the get test passes, then we know DONUT_DATA is present
            # We are simply confirming that we can change it without adding
            # a donut.
            url = f"/api/donuts/{self.donut.id}"
            resp = client.patch(url, json=DONUT_UPDATE)

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertIsInstance(data['donut']['id'], int)
            del data['donut']['id']

            self.assertEqual(data, {
                "donut": {
                    "flavor": "UpdatedFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/update.jpg"
                }
            })

            self.assertEqual(Donut.query.count(), 1)

    def test_update_non_donut(self):
        with app.test_client() as client:
            url = "/api/donuts/9999999"
            resp = client.patch(url, json=DONUT_UPDATE)

            self.assertEqual(resp.status_code, 404)

    def test_delete_donut(self):
        with app.test_client() as client:
            url = f"/api/donuts/{self.donut.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(Donut.query.count(), 0)

            data = resp.json

            self.assertEqual(data, {
                "message": f"{self.donut.flavor} donut deleted."
            })

    def test_delete_non_donut(self):
        with app.test_client() as client:
            url = "/api/donuts/9999999"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)
