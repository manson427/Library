import pytest


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, get_id",
    [
        ["guest", 200, True, 1],
        ["user_id2", 200, True, 1],
        ["user_id2", 404, False, 10],
    ])
async def test_get_one(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/book/get_one/", cookies=cookies, params={'book_id': get_id})
    good_json = {
        "name": "Двенадцать стульев",
        "description": "Роман Ильи Ильфа и Евгения Петрова, написанный в 1927 году и являющийся первой совместной работой соавторов. В 1928 году опубликован в художественно-литературном журнале «Тридцать дней» (№ 1—7); в том же году издан отдельной книгой. В основе сюжета — поиски бриллиантов, спрятанных в одном из двенадцати стульев мадам Петуховой, однако история, изложенная в произведении, не ограничена рамками приключенческого жанра: в ней, по мнению исследователей, дан «глобальный образ эпохи».",
        "publish_year": 1928,
        "amount": 5,
        "id": 1
    }
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json",
    [
        ["guest", 200, True, ],
        ["user_id2", 200, True, ],
    ])
async def test_get(client, create, get_tokens, test_role, test_code, check_json):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/book/get/", cookies=cookies)
    assert response.status_code == test_code
    if check_json:
        assert len(response.json()) == 3


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, phrase",
    [
        ["guest", 200, True, 'е'],
        ["user_id2", 200, True, 'е'],
        ["user_id2", 404, False, 'xyz'],
    ])
async def test_get_like(client, create, get_tokens, test_role, test_code, check_json, phrase):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/book/get_like/", cookies=cookies, params={'phrase': phrase})
    assert response.status_code == test_code
    if check_json:
        assert len(response.json()) == 2


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, description",
    [
        ["guest", 401, False, 'тест'],
        ["user_id2", 403, False, 'тест'],
        ["admin_id1", 200, True, 'тест'],
        ["admin_id1", 422, False, 123],
    ])
async def test_create(client, create, get_tokens, test_role, test_code, check_json, description):
    cookies = {'access_token': get_tokens[test_role]}
    send = {
        "id": 4,
        "name": "string",
        "description": description,
        "publish_year": 0,
        "amount": 0
    }
    response = client.post("/book/create/", cookies=cookies, json=send)
    assert response.status_code == test_code
    if check_json:
        assert response.json() == send


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, path, data, detail",
    [
        ["guest", 401, 'create_link_author', {'author_id': 1, 'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'create_link_genre', {'genre_id': 1, 'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete', {'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete_link_author', {'author_id': 1, 'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete_link_genre', {'genre_id': 1, 'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete_all_links_author', {'author_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete_all_links_genre', {'genre_id': 1}, 'Invalid token'],

        ["user_id2", 403, 'create_link_author', {'author_id': 1, 'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'create_link_genre', {'genre_id': 1, 'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete', {'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete_link_author', {'author_id': 1, 'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete_link_genre', {'genre_id': 1, 'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete_all_links_author', {'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete_all_links_genre', {'book_id': 1}, 'Your role, not in role_list'],

        ["admin_id1", 404, 'delete', {'book_id': 555}, 'Error'],
        ["admin_id1", 404, 'delete_link_author', {'author_id': 555, 'book_id': 1}, 'Error'],
        ["admin_id1", 404, 'delete_link_genre', {'genre_id': 555, 'book_id': 1}, 'Error'],
        ["admin_id1", 404, 'delete_all_links_author', {'book_id': 555}, 'Error'],
        ["admin_id1", 404, 'delete_all_links_genre', {'book_id': 555}, 'Error'],

        ["admin_id1", 200, 'create_link_author', {'author_id': 1, 'book_id': 4}, 'Link Author with id=1 to Book with id=4 created'],
        ["admin_id1", 200, 'create_link_genre', {'genre_id': 1, 'book_id': 4}, 'Link Genre with id=1 to Book with id=4 created'],
        ["admin_id1", 409, 'delete', {'book_id': 4}, 'Can not delete book, because there are 1 links to authors'],
        ["admin_id1", 200, 'delete_link_author', {'author_id': 1, 'book_id': 4}, 'Link Author with id=1 to Book with id=4 deleted'],
        ["admin_id1", 409, 'delete', {'book_id': 4}, 'Can not delete book, because there are 1 links to genres'], ##
        ["admin_id1", 200, 'delete_link_genre', {'genre_id': 1, 'book_id': 4}, 'Link Genre with id=1 to Book with id=4 deleted'], ##
        ["admin_id1", 200, 'delete', {'book_id': 4}, 'Book with id=4 deleted'], ##

        ["admin_id1", 409, 'delete', {'book_id': 1}, 'Can not delete book, because there are 2 links to authors'],
        ["admin_id1", 200, 'delete_all_links_author', {'book_id': 1},
         '2 links Author to Book with Book id=1 deleted'],
        ["admin_id1", 409, 'delete', {'book_id': 1}, 'Can not delete book, because there are 1 links to genres'],
        ["admin_id1", 200, 'delete_all_links_genre', {'book_id': 1}, '1 links Genre to Book with Book id=1 deleted'],
        ["admin_id1", 409, 'delete', {'book_id': 1}, 'Can not delete book, because there are 1 copies out'],
    ])
async def test_create_delete(client, create, get_tokens, test_role, test_code, path, data: dict, detail):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.post(f"/book/{path}/", cookies=cookies, params=data)
    assert response.status_code == test_code
    assert response.json()['detail'] == detail


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, get_id",
    [
        ["guest", 200, True, 3],
        ["user_id2", 200, True, 3],
        ["user_id2", 404, False, 100],
    ])
async def test_get_authors(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/book/get_authors/", cookies=cookies, params={'book_id': get_id})
    good_json = [
        {
            "name": "Лев Николаевич Толстой",
            "biography": "Один из наиболее известных русских писателей и мыслителей, один из величайших в мире писателей-романистов.",
            "born": "1828-09-09",
            "id": 3
        }
    ]
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, get_id",
    [
        ["guest", 200, True, 3],
        ["user_id2", 200, True, 3],
        ["user_id2", 404, False, 100],
    ])
async def test_get_genres(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/book/get_genres/", cookies=cookies, params={'book_id': get_id})
    good_json = [
        {
            "name": "Автобиографические роман",
            "description": "Прозаический жанр, описание собственной жизни; близок мемуарам, но более сосредоточен на личности и внутреннем мире автора",
            "id": 3
        }
    ]
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, get_id",
    [
        ["guest", 401, False, 3],
        ["admin_id1", 404, False, 100],
        ["admin_id1", 200, True, 3],
    ])
async def test_get_users(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/book/get_users/", cookies=cookies, params={'book_id': get_id, "returned": False})
    good_json = [
        {
            "email": "user1@test.ru",
            "born": "2024-12-29",
            "name": "user1",
            "id": 2,
            "role_id": 0,
            "verified": False,
            "books": [
                {
                    "id": 3,
                    "left_id": 2,
                    "right_id": 3,
                    "get_at": "2025-01-22",
                    "must_return_at": "2025-02-05",
                    "returned_at": None,
                    "returned": False
                }
            ]
        }
    ]
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json
