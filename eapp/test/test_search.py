import pytest
# from sqlalchemy.sql.coercions import expect

from eapp.models import Product
from eapp.dao import load_products
from eapp.test.test_base import  test_session,test_app




@pytest.fixture
def sample_product(test_session):
    p1 = Product(name="iphone 17", price=30, category_id=1)
    p2 = Product(name="iphone 18", price=40, category_id=1)
    p3 = Product(name="ss 19", price=15, category_id=2)
    p4 = Product(name="ss 20", price=10, category_id=2)
    p5 = Product(name="ipad 21", price=60, category_id=3)

    test_session.add_all([p1, p2, p3, p4, p5])
    test_session.commit()
    return [p1, p2, p3, p4, p5]


def test_all(sample_product):
    actual_product=load_products()
    assert len(actual_product)==5

def test_paging(test_app,sample_product):
    actual_product=load_products(page=1)
    assert len(actual_product)==test_app.config['PAGE_SIZE']
    actual_product=load_products(page=3)
    assert len(actual_product)==1



@pytest.mark.parametrize(
    "category_id,expected",[
    (1,2),
    (2,2),
    (3,1),
    (4,0),
    (None,5)])
def test_cate(sample_product,expected,category_id):
    actual_product=load_products(cate_id=category_id)
    assert len(actual_product)==expected

# @pytest.mark.parametrize(
#     "prices,expected",
#     [
#     ([10,14],1),
#     ([30,40],2),
#     ([90,100],0),
#     (None,5)])
# def test_price(sample_product,prices,expected):
#     actual_product=load_products(price=prices)
#     assert len(actual_product) == expected


@pytest.mark.parametrize(
    "kw,expected",[
    ("iphone",2),
    ("iphone 17",1),
    ("aas",0),
    (None,5)])
def test_kw(sample_product,kw,expected):
    actual_product=load_products(kw=kw)
    assert len(actual_product) == expected