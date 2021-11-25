from fastapi.testclient import TestClient
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
import pytest
from app.oauth2 import create_access_token

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
                   "quantity_init":12,
                   "quantity_left":123
               },{
                   "product_name":"chaussure",
                   "quantity_init":133,
                   "quantity_left":13
                   },{
                   "product_name":"savon",
                   "quantity_init":123,
                   "quantity_left":13
                   }]
    def create_product_model(product):
        return models.Product(**product)
    product_map=map(create_product_model,products)
    prods=list(product_map)
    session.add_all(prods)
    session.commit()
    pro=session.query(models.Product).all()
    return pro

