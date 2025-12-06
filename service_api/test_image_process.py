import pytest

from fastapi.testclient import TestClient

from image_process import api


client = TestClient(api)

TEST_EMAIL = 'can_c@yahoo.ru'

TEST_IMG_PATH = 'test_image.png'


@pytest.mark.asyncio
async def test_analyze_doc_success():
    with open(TEST_IMG_PATH, 'rb') as file:
        response = client.post('/analyze_image', files={'image': file})
        
    assert response.status_code == 200
    assert 'text' in response.json()


@pytest.mark.asyncio
async def test_analyze_doc_no_image():
    response = client.post('/analyze_image', data={'email': TEST_EMAIL})
    
    assert response.status_code == 418
    assert 'text' in response.json()


@pytest.mark.asyncio
async def test_send_message_to_email_success():
    email = TEST_EMAIL
    text = 'Test message'
    response = client.post('/send_message_to_email/', json={'email': email, 'text': text})
    
    assert response.status_code == 200
    assert response.json()['message'] == 'Image has been analyzed'


@pytest.mark.asyncio
async def test_send_message_to_email_invalid_email():
    text = 'Test message'
    response = client.post('/send_message_to_email/', json={'email': 'invalid_email', 'text': text})
    
    assert response.status_code == 422
