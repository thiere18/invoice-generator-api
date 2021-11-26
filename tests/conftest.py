from fastapi.testclient import TestClient
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
import pytest
from app.oauth2 import create_access_token
import json
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try: 
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data={"username":"thiere","email":"thiern@gmail.com","password":"thierno"}
    res=client.post('/users/',json=user_data)
    assert res.status_code == 201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user
    
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
        }
    return client
    

@pytest.fixture
def test_products(test_user,session):
    products =[{
                   "product_name":"sac a dos",
                   "quantity_init":122,
                   "quantity_left":123
               },{
                   "product_name":"chaussure",
                   "quantity_init":150,
                   "quantity_left":133
                   },{
                   "product_name":"savon",
                   "quantity_init":133,
                   "quantity_left":100
                   },
                   {
                   "product_name":"citron",
                   "quantity_init":190,
                   "quantity_left":190
                   },
                   {
                   "product_name":"sauce",
                   "quantity_init":123,
                   "quantity_left":13
                   }
                   ]
    def create_product_model(product):
        return models.Product(**product)
    product_map=map(create_product_model,products)
    prods=list(product_map)
    session.add_all(prods)
    session.commit()
    pro=session.query(models.Product).all()
    return pro

@pytest.fixture
def test_invoices(test_user,session):
    invoice =[{   
    "product": {
    "reference": "c3405557",
    "value_net": 8870,
    "actual_payment": 30090
    }, 
      "item": [
    {
      "product_name": "sauce",
      "quantity": 10,
      "prix_unit": 3330
    },
        {
      "product_name": "sac a dos",
      "quantity":2,
      "prix_unit": 22220
    },
            {
      "product_name": "savon",
      "quantity": 30,
      "prix_unit": 333340
    }
    ]},
              {   
    "product": {
    "reference": "string2fsfs",
    "value_net": 400090,
    "actual_payment": 33300
    }, 
      "item": [
    {
      "product_name": "sac a dos",
      "quantity":33,
      "prix_unit": 90000
    }
    ]}
    ]
    for x in invoice:
        #create new schema for the invoice
        value=x['product']['value_net']
        ref=x['product']['reference']
        actual=x['product']['actual_payment']
        invo={
            "reference": ref,
            "value_net":value,
            "actual_payment":actual,
            "payment_due":value-actual,
            "invoice_owner_id":test_user['id']
        }
        new_invoice = models.Invoice( **invo)   
        session.add(new_invoice)
        session.commit()
        session.refresh(new_invoice)
        new_id=new_invoice.id

        for v in x['item']:
            #new schema for the invoice detail
            product_nam=v['product_name']
            quantity=v['quantity']
            prix=v['prix_unit']
            da={
                "product_name":product_nam, 
                "quantity":quantity,
                "prix_unit":prix
            }  
   
            session.commit()
            new_invoice_item = models.InvoiceItem(invoice_id=new_id,**da)
            session.add(new_invoice_item)
            session.commit()    
 
    # def create_product_model(product):
    #     return models.I(**product)
    # product_map=map(create_product_model,invoice)
    # prods=list(product_map)
    # for x in prods:
    #     print(x)
    # session.add_all(prods)
    # session.commit()
    # inv=json.dumps(invoice)
    # for inb  in invoice:
    #     print(inb)
        # new_invoice = models.Invoice(invoice_owner_id=test_user['id'],payment_due=(inv['value_net']-inv['actual_payment']), **inv)
        # session.add(new_invoice)
        # session.commit()
        # session.refresh(new_invoice)
    
        # new_id=new_invoice.id
        # for invoice_item in inv['items']:
        #     prod=invoice_item['product_name']
        #     quant=invoice_item['quantity']
        #     #verify if this product exist
        #     p= session.query(models.Product).filter(models.Product.product_name==prod).first()
        #     p.quantity_left-=quant
        #     session.commit()
        #     new_invoice_item = models.InvoiceItem(invoice_id=new_id,**invoice_item.dict())
        #     session.add(new_invoice_item)
        #     session.commit()
    
    
        pro=session.query(models.Invoice).all()
        return pro
