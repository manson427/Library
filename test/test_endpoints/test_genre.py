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
    response = client.get("/genre/get_one/", cookies=cookies, params={'genre_id': get_id})
    good_json = {
        "name": "Роман",
        "description": "Литературный жанр, чаще прозаический, зародившийся в Средние века у романских народов, как рассказ на народном языке и ныне превратившийся в самый распространённый вид эпической литературы, изображающий жизнь персонажа с её волнующими страстями, борьбой, социальными противоречиями и стремлениями к идеалу. Будучи развёрнутым повествованием о жизни и развитии личности главного героя (героев) в кризисный, нестандартный период его жизни, отличается от повести объёмом, сложностью содержания и более широким захватом описываемых явлений",
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
    response = client.get("/genre/get/", cookies=cookies)
    assert response.status_code == test_code
    if check_json:
        assert len(response.json()) == 3


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, phrase",
    [
        ["guest", 200, True, 'оман'],
        ["user_id2", 200, True, 'оман'],
        ["user_id2", 404, False, 'xyz'],
    ])
async def test_get_like(client, create, get_tokens, test_role, test_code, check_json, phrase):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/genre/get_like/", cookies=cookies, params={'phrase': phrase})
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
        "name": 'тест',
        "description": description,
    }
    response = client.post("/genre/create/", cookies=cookies, json=send)
    assert response.status_code == test_code
    if check_json:
        assert response.json() == send


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, path, data, detail",
    [
        ["guest", 401, 'create_link_book', {'genre_id': 1, 'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete', {'genre_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete_link_book', {'genre_id': 1, 'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete_all_links_book', {'genre_id': 1}, 'Invalid token'],

        ["user_id2", 403, 'create_link_book', {'genre_id': 1, 'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete', {'genre_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete_link_book', {'genre_id': 1, 'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete_all_links_book', {'genre_id': 1}, 'Your role, not in role_list'],

        ["admin_id1", 404, 'delete', {'genre_id': 555}, 'Error'],
        ["admin_id1", 404, 'delete_link_book', {'genre_id': 555, 'book_id': 1}, 'Error'],
        ["admin_id1", 404, 'delete_all_links_book', {'genre_id': 555}, 'Error'],

        ["admin_id1", 200, 'create_link_book', {'genre_id': 4, 'book_id': 1},
         'Link Genre with id=4 to Book with id=1 created'],
        ["admin_id1", 409, 'delete', {'genre_id': 4}, 'Can not delete genre, because there are 1 links to books'],
        ["admin_id1", 200, 'delete_link_book', {'genre_id': 4, 'book_id': 1},
         'Link Genre with id=4 to Book with id=1 deleted'],
        ["admin_id1", 200, 'delete', {'genre_id': 4}, 'Genre with id=4 deleted'],

        ["admin_id1", 409, 'delete', {'genre_id': 1}, 'Can not delete genre, because there are 2 links to books'],
        ["admin_id1", 200, 'delete_all_links_book', {'genre_id': 1},
         '2 links Genre to Book with Genre id=1 deleted'],
        ["admin_id1", 200, 'delete', {'genre_id': 1}, 'Genre with id=1 deleted'],
    ])
async def test_create_delete(client, create, get_tokens, test_role, test_code, path, data: dict, detail):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.post(f"/genre/{path}/", cookies=cookies, params=data)
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
async def test_get_books(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/genre/get_books/", cookies=cookies, params={'genre_id': get_id})
    good_json = [
        {
            "name": "Детство",
            "description": "Первая повесть автобиографической трилогии Льва Толстого, впервые напечатана в 1852 году в журнале «Современник», № 9. Эта книга описывает психологические переживания, которые испытывают многие мальчики в детстве: первая влюблённость, чувство несправедливости, обида, стеснение.",
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
async def test_get_authors(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/genre/get_authors/", cookies=cookies, params={'genre_id': get_id})
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
        ["guest", 401, False, 3],
        ["admin_id1", 404, False, 100],
        ["admin_id1", 200, True, 3],
    ])
async def test_get_users(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/genre/get_users/", cookies=cookies, params={'genre_id': get_id, "returned": False})
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
                    "returned": False,
                    "book": {
                        "name": "Детство",
                        "description": "Первая повесть автобиографической трилогии Льва Толстого, впервые напечатана в 1852 году в журнале «Современник», № 9. Эта книга описывает психологические переживания, которые испытывают многие мальчики в детстве: первая влюблённость, чувство несправедливости, обида, стеснение.",
                        "publish_year": 1852,
                        "amount": 0,
                        "id": 3
                    }
                }
            ]
        }
    ]
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json
