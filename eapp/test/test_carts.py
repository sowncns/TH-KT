import pytest

from eapp import app
from eapp.index import carts_routes


@pytest.fixture
def test_client():
    if "add_to_cart" not in app.view_functions:
        carts_routes()

    with app.test_client() as client:
        yield client


def test_add_to_cart(test_client):
    res = test_client.post(
        "/api/carts",
        json={
            "id": "1",
            "name": "abc",
            "price": 50,
        },
    )

    assert res.status_code == 200
    data = res.get_json()
    assert data["total_quantity"] == 1
    assert data["total_amount"] == 50

def test_add_existing_cart(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
                 "2": {
                    "id": "2",
                   "name": "abc",
                   "price": 50,
                   "quantity": 2
                }
           }

    res = test_client.post(
            "/api/carts",
            json={
                "id": "2",
                "name": "abc",
                "price": 50,
            },
        )
    with test_client.session_transaction() as sess:
        assert 'cart'  in sess
        assert sess['cart']['2']['quantity'] == 3


def test_incr_cart(test_client):
    test_client.post("/api/carts", json={
        "id": "1",
        "name": "abc",
        "price": 50,

    })
    test_client.post("/api/carts", json={
        "id": "1",
        "name": "abc",
        "price": 50,

    })
    res = test_client.post("/api/carts", json={
        "id": "2",
        "name": "abcd",
        "price": 150,

    })
    data = res.get_json()
    assert data["total_quantity"] == 3
    assert data["total_amount"] == 250

    with test_client.session_transaction() as sess:
        assert 'cart' in sess
        assert len(sess['cart']) == 2
        assert sess['cart']['1']['quantity'] == 2

def test_update_cart(test_client):
    with test_client.session_transaction() as sess:

        sess['cart'] = {
                 "2": {
                    "id": "2",
                   "name": "abc",
                   "price": 50,
                   "quantity": 2
                }
          }
    res = test_client.put("/api/carts/2", json={
        "quantity": 10,
    })
    data = res.get_json()
    assert data["total_quantity"] == 10
    assert data["total_amount"] == 500

def test_delete_cart(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "2": {
                "id": "2",
                "name": "abc",
                "price": 50,
                "quantity": 2
            }
        }
    res = test_client.delete("/api/carts/2")
    data = res.get_json()
    assert data["total_quantity"] == 0
    with test_client.session_transaction() as sess:
        assert 'cart' in sess

