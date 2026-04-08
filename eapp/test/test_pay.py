from eapp.test.test_base import test_client, test_app
import flask_login

def test_pay_success(test_client, mocker):
     class FakeUser:
        id =1
        is_authenticated = True
     mocker.patch("flask_login.utils._get_user", return_value=FakeUser())
     # mock current_user trong dao
     mocker.patch("eapp.dao.current_user", new=FakeUser())
     # setup session cart
     with test_client.session_transaction() as sess:
         sess["cart"] = {
         "1": {"id": 1, "price": 100, "quantity": 20}
         }
     mock_add = mocker.patch("eapp.dao.add_receipt")

     response = test_client.post("/api/pay")
     data = response.get_json()
     assert data["status"] == 200
     mock_add.assert_called_once()
