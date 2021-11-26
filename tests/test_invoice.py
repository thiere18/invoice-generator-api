from app import schemas
import pytest
def test_get_all_invoices(authorized_client,test_invoices):
    res=authorized_client.get("/invoices/")
    assert res.status_code ==200

def test_unathorized_get_all_invoices(client,test_invoices):
    res=client.get("/invoices/")
    assert res.status_code ==401
    
def test_unathorized_get_one_invoice(client,test_invoices):
    res=client.get(f"/invoices/{test_invoices[0].id}")
    assert res.status_code ==401
    
def test_get_one_invoice_not_exixst(authorized_client,test_invoices):
    res=authorized_client.get("/invoices/456478955")
    assert res.json().get("detail")==f"invoice with id: 456478955 was not found"
    assert res.status_code == 404
    
def test_get_one_invoice(authorized_client,test_invoices):
    res=authorized_client.get(f"/invoices/{test_invoices[0].id}")
    product=schemas.InvoiceOut(**res.json())
    assert product.id == test_invoices[0].id
    assert product.reference == test_invoices[0].reference

# @pytest.mark.parametrize("product_name, quantity_init, quantity_left, status_code",[
#     (None,None,33,422),
#     ("chambre",23,44,201)
# ])
# def test_create_product(authorized_client,test_user,test_invoices,product_name,quantity_init, quantity_left, status_code):
#     res=authorized_client.post("/invoices/",json={"product_name":product_name, "quantity_init":quantity_init, "quantity_left":quantity_left})
#     assert res.status_code ==status_code
    
# def test_unathorized_create_products(client,test_user):
#     res=client.post("/invoices/",json={"product_name":"product_name", "quantity_init":23,"quantity_left":23})
#     assert res.status_code ==401
    
def test_unathorized_delete_invoice(client,test_user,test_invoices):
    res=client.delete(f"/invoices/{test_invoices[0].id}")
    assert res.status_code ==401
    
def test_authorize_delete_invoices(authorized_client,test_user,test_invoices):
    res=authorized_client.delete(f"/invoices/{test_invoices[0].id}")
    assert res.status_code ==204
    
def test_authorize_delete_non_existing(authorized_client,test_user,test_invoices):
    res=authorized_client.delete(f"/invoices/3456")
    assert res.json().get('detail') =="invoice with id: 3456 does not exist"
    assert res.status_code ==404
    
def test_update_invoice(authorized_client,test_invoices,test_user):
    h=200000
    c=4500
    data={
        "reference":"savon_de_merde",
        "value_net":h,
        "actual_payment":h
        

    }
    res=authorized_client.put(f"/invoices/{test_invoices[0].id}",json=data)
    updated_product=schemas.InvoiceCreate(**res.json())
    assert res.status_code == 200
    assert updated_product.reference==data["reference"]
    assert updated_product.actual_payment==h