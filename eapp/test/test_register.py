from eapp.test.test_base import  test_app ,test_session
from eapp.dao import add_user
from eapp.dao import User
import pytest

def test_success(test_session,test_app):
    add_user(username="admin123", password="Abc@1234", name='admin', avatar=None)
    acctually = User.query.filter_by(username="admin123").first()
    assert acctually is not None
    assert acctually.name == "admin"

@pytest.mark.parametrize('password',['1a'*3,'12'*4,'a'*8,'a'])
def test_password(password,test_app):
    with pytest.raises(ValueError):
        add_user(username="1a"*4,password=password,name='admin',avatar=None)


@pytest.fixture
def test_cloudinary(monkeypatch):
    def fake_upload(file):
        return { 'secure_url':'https:fake-image.png'}
    monkeypatch.setattr('cloudinary.uploader.upload', fake_upload)


def test_avt(test_session,test_cloudinary):
    add_user(username="admin123", password="Abc@1234", name='admin', avatar="abcb")
    acctually = User.query.filter_by(username="admin123").first()
    assert acctually.avatar == "https:fake-image.png"
