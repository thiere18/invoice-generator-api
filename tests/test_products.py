from app import schemas
import pytest
def test_get_all_products(authorized_client,test_products):
    res=authorized_client.get("/products/")
    assert len(res.json()) ==len(test_products)
    assert res.status_code ==200

def test_unathorized_get_all_products(client,test_products):
    res=client.get("/products/")
    assert res.status_code ==401
    
def test_unathorized_get_one_products(client,test_products):
    res=client.get(f"/products/{test_products[0].id}")
    assert res.status_code ==401
    
def test_get_one_product_not_exixst(authorized_client,test_products):
    res=authorized_client.get("/products/456478955")
    assert res.json().get("detail")==f"product with id: 456478955 was not found"
    assert res.status_code == 404
    
def test_get_one_product(authorized_client,test_products):
    res=authorized_client.get(f"/products/{test_products[0].id}")
    product=schemas.ProductOut(**res.json())
    assert product.id == test_products[0].id
    assert product.product_name == test_products[0].product_name

@pytest.mark.parametrize("product_name, quantity_init, quantity_left, status_code",[
    (None,None,33,422),
    ("chambre",23,44,201)
])
def test_create_product(authorized_client,test_user,test_products,product_name,quantity_init, quantity_left, status_code):
    res=authorized_client.post("/products/",json={"product_name":product_name, "quantity_init":quantity_init, "quantity_left":quantity_left})
    assert res.status_code ==status_code
    
def test_unathorized_create_products(client,test_user):
    res=client.post("/products/",json={"product_name":"product_name", "quantity_init":23,"quantity_left":23})
    assert res.status_code ==401
    
def test_unathorized_delete_products(client,test_user,test_products):
    res=client.delete(f"/products/{test_products[0].id}")
    assert res.status_code ==401
    
def test_authorize_delete_products(authorized_client,test_user,test_products):
    res=authorized_client.delete(f"/products/{test_products[0].id}")
    assert res.status_code ==204
    
def test_authorize_delete_non_existing(authorized_client,test_user,test_products):
    res=authorized_client.delete(f"/products/3456")
    assert res.json().get('detail') =="product with id: 3456 does not exist"
    assert res.status_code ==404
    
def test_update_product(authorized_client,test_products,test_user):
    data={
        "product_name":"savon",
        "quantity_init":32,
        "quantity_left":452,
        "id":test_products[0].id
    }
    res=authorized_client.put(f"/products/{test_products[0].id}",json=data)
    updated_product=schemas.ProductOut(**res.json())
    assert res.status_code == 200
    assert updated_product.product_name==data["product_name"]
    print(res.json())
    assert updated_product.quantity_init==data["quantity_init"]
