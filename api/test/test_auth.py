import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT

def test_jwt_create(api_client, create_user):
    """
    JWTを作成するエンドポイントが成功することを確認するテスト
    """
    # Setup
    url = reverse('jwt-create')
    data = {'username': create_user.username, 'password': 'testpassword'}

    # Exercise
    response = api_client.post(url, data)

    # Verify
    assert response.status_code == HTTP_200_OK
    assert 'access' in response.data

def test_jwt_refresh(api_client, create_user):
    """
    既存のJWTを更新するエンドポイントが成功することを確認するテスト
    """
    # Setup
    # まずJWTトークンを作成
    create_url = reverse('jwt-create')
    data = {'username': create_user.username, 'password': 'testpassword'}
    response = api_client.post(create_url, data)
    refresh_token = response.data['refresh']

    # そのトークンを使って更新
    url = reverse('jwt-refresh')
    data = {'refresh': refresh_token}

    # Exercise
    response = api_client.post(url, data)

    # Verify
    assert response.status_code == HTTP_200_OK
    assert 'access' in response.data

def test_jwt_verify(api_client, create_user):
    """
    JWTを検証するエンドポイントが成功することを確認するテスト
    """
    # Setup
    # まずJWTトークンを作成
    create_url = reverse('jwt-create')
    data = {'username': create_user.username, 'password': 'testpassword'}
    response = api_client.post(create_url, data)
    access_token = response.data['access']

    # そのトークンを使って検証
    url = reverse('jwt-verify')
    data = {'token': access_token}

    # Exercise
    response = api_client.post(url, data)

    # Verify
    assert response.status_code == HTTP_200_OK

