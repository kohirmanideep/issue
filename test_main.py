from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_issuedbook():
    response = client.get('/issuedbook/')
    assert response.status_code ==200
    
def get_issued():
    response = client.get('/issuedbooks/manideep')
    assert response.status_code == 200