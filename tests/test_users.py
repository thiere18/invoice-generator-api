from jose import jwt
from app import schemas
from app.config import settings
import pytest

def test_root(client):
    res=client.get('/')
    assert res.json().get("message")=="Hello World pushing out"
    assert res.status_code == 200
    

def test_create_user(client):
    res=client.post('/users/',json={"username":"thierno","email":"thierno@gmail.com","password":"thierno"})
    new_user=schemas.UserOut(**res.json())
    assert new_user.username=="thierno"
    assert res.status_code == 201
    
def test_login_user(test_user,client):
    res=client.post('/login',data={"username":test_user['email'],"password":test_user['password']})
    login_res=schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id=payload.get('user_id')
    assert id==test_user['id']
    assert login_res.token_type=="bearer"
    assert res.status_code==200

@pytest.mark.parametrize("email, password, status_code",[
    ('user@exampld.com', 'bearer',403),
    (None, 'bearer',422),
    ('thiere','thierno',200)
    
])
def test_incorrect_user(test_user,client,email,password,status_code):
    res=client.post('/login',data={"username":email, "password":password})
    # assert res.json().get('detail')=="Invalid Credentials"
    assert res.status_code == status_code
    
    
    