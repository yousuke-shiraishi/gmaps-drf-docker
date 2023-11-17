import pytest
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import GmapFactory, UserFactory, GmapNoMagicWordFactory
from gmaps.models import Gmap
from rest_framework_simplejwt.tokens import RefreshToken
pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = UserFactory()
    user.set_password('pass12345')
    user.save()
    return user

@pytest.fixture
def gmap(user, db):
    return GmapFactory(user=user)

@pytest.fixture
def gmap_no_magic_word(user, db):
    return GmapNoMagicWordFactory(user=user)

@pytest.fixture
def token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.mark.django_db
def test_create_gmap(api_client,user,gmap,token):
    # api_client.force_authenticate(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    gmap_data = {
        'title': 'Sample title',
        'comment': 'Sample comment',
        'latitude': 35.6895,
        'longitude': 139.6917,
        'picture': gmap.picture,
        'magic_word': 'magic_word',
        'user': user.id,
    }

    response = api_client.post(f'/gmaps/', {
        **gmap_data
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == gmap_data['title']


@pytest.mark.django_db
def test_delete_gmap(api_client,token,gmap):
    # api_client.force_authenticate(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    response = api_client.delete(f'/gmaps/{gmap.id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Gmap.objects.filter(id=gmap.id).exists()


@pytest.mark.django_db
def test_gmap_list_unauthenticated(api_client):
    url = reverse('gmaps-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_gmap_create_authenticated(api_client,token,gmap,user):
    # api_client.force_authenticate(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    gmap_data = {
        'title': 'Test Gmap',
        'comment': 'This is a test gmap.',
        'latitude': 35.6895,
        'longitude': 139.6917,
        'picture': gmap.picture,
        'magic_word': 'magic_word',
        'user': user.id
    }
    response = api_client.post(f'/gmaps/', {
            **gmap_data
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == gmap_data['title']
    assert response.data['comment'] == gmap_data['comment']


@pytest.mark.django_db
def test_gmap_create_unauthenticated(api_client,user, gmap):
    gmap_data = {
        'title': 'Test Gmap',
        'comment': 'This is a test gmap.',
        'latitude': 35.6895,
        'longitude': 139.6917,
        'picture': gmap.picture,
        'magic_word': 'magic_word',
    }

    response = api_client.post(f'/gmaps/', {
            **gmap_data
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_gmap_destroy_authenticated(api_client,user, token, gmap):
    # api_client.force_authenticate(user=user)
    api_client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    response = api_client.delete(f'/gmaps/{gmap.id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_gmap_destroy_unauthenticated(api_client, gmap):

    response = api_client.delete(f'/gmaps/{gmap.id}/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_public_search(api_client, user, gmap_no_magic_word):
    url = reverse('public_search')
    data = {'username': user.username, 'birth': user.birth}

    response = api_client.get(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert str(response.data[0]['id']) == str(gmap_no_magic_word.id)

@pytest.mark.django_db
def test_private_search_authenticated(api_client, token, user, gmap):
    url = reverse('private_search')
    # api_client.force_authenticate(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    data = {'email': user.email, 'magic_word': "magic_word"}

    response = api_client.get('/gmaps/private_search/', {
            **data
    })
    # breakpoint()
    assert response.status_code == status.HTTP_200_OK
    assert str(response.data[0]['id']) == str(gmap.id)

@pytest.mark.django_db
def test_private_search_unauthenticated(api_client, user, gmap):
    url = reverse('private_search')

    data = {'email': user.email, 'magic_word': "magic_word"}
    response = api_client.get(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


