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
    response = client.get("/author/get_one/", cookies=cookies, params={'author_id': get_id})
    good_json = {
        "id": 1,
        "name": 'Илья Арнольдович Ильф',
        "biography": 'Русский советский писатель, драматург и сценарист, фотограф, журналист',
        "born": '1897-10-15',
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
    response = client.get("/author/get/", cookies=cookies)
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
    response = client.get("/author/get_like/", cookies=cookies, params={'phrase': phrase})
    assert response.status_code == test_code
    if check_json:
        assert len(response.json()) == 2


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, born",
    [
        ["guest", 401, False, '1917-10-25'],
        ["user_id2", 403, False, '1917-10-25'],
        ["admin_id1", 200, True, '1917-10-25'],
        ["admin_id1", 422, False, '3-23-3'],
    ])
async def test_create(client, create, get_tokens, test_role, test_code, check_json, born):
    cookies = {'access_token': get_tokens[test_role]}
    send = {
        "id": 4,
        "name": 'тест',
        "biography": 'тест',
        "born": born,
    }
    response = client.post("/author/create/", cookies=cookies, json=send)
    assert response.status_code == test_code
    if check_json:
        assert response.json() == send


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, path, data, detail",
    [
        ["guest", 401, 'create_link_book', {'author_id': 1, 'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete', {'author_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete_link_book', {'author_id': 1, 'book_id': 1}, 'Invalid token'],
        ["guest", 401, 'delete_all_links_book', {'author_id': 1}, 'Invalid token'],

        ["user_id2", 403, 'create_link_book', {'author_id': 1, 'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete', {'author_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete_link_book', {'author_id': 1, 'book_id': 1}, 'Your role, not in role_list'],
        ["user_id2", 403, 'delete_all_links_book', {'author_id': 1}, 'Your role, not in role_list'],

        ["admin_id1", 404, 'delete', {'author_id': 555}, 'Error'],
        ["admin_id1", 404, 'delete_link_book', {'author_id': 555, 'book_id': 1}, 'Error'],
        ["admin_id1", 404, 'delete_all_links_book', {'author_id': 555}, 'Error'],

        ["admin_id1", 200, 'create_link_book', {'author_id': 4, 'book_id': 1},
                     'Link Author with id=4 to Book with id=1 created'],
        ["admin_id1", 409, 'delete', {'author_id': 4}, 'Can not delete author, because there are 1 links to books'],
        ["admin_id1", 200, 'delete_link_book', {'author_id': 4, 'book_id': 1},
                     'Link Author with id=4 to Book with id=1 deleted'],
        ["admin_id1", 200, 'delete', {'author_id': 4}, 'Author with id=4 deleted'],

        ["admin_id1", 409, 'delete', {'author_id': 3}, 'Can not delete author, because there are 2 links to books'],
        ["admin_id1", 200, 'delete_all_links_book', {'author_id': 3},
                     '2 links Author to Book with Author id=3 deleted'],
        ["admin_id1", 200, 'delete', {'author_id': 3}, 'Author with id=3 deleted'],
    ])
async def test_create_delete(client, create, get_tokens, test_role, test_code, path, data: dict, detail):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.post(f"/author/{path}/", cookies=cookies, params=data)
    assert response.status_code == test_code
    assert response.json()['detail'] == detail


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, get_id",
    [
        ["guest", 200, True, 1],
        ["user_id2", 200, True, 1],
        ["user_id2", 404, False, 100],
    ])
async def test_get_books(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/author/get_books/", cookies=cookies, params={'author_id': get_id})
    good_json = [
        {
            "name": "Двенадцать стульев",
            "description": "Роман Ильи Ильфа и Евгения Петрова, написанный в 1927 году и являющийся первой совместной работой соавторов. В 1928 году опубликован в художественно-литературном журнале «Тридцать дней» (№ 1—7); в том же году издан отдельной книгой. В основе сюжета — поиски бриллиантов, спрятанных в одном из двенадцати стульев мадам Петуховой, однако история, изложенная в произведении, не ограничена рамками приключенческого жанра: в ней, по мнению исследователей, дан «глобальный образ эпохи».",
            "publish_year": 1928,
            "amount": 5,
            "id": 1
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
        ["guest", 200, True, 1],
        ["user_id2", 200, True, 1],
        ["user_id2", 404, False, 100],
    ])
async def test_get_genres(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/author/get_genres/", cookies=cookies, params={'author_id': get_id})
    good_json = [
        {
            "name": "Роман",
            "description": "Литературный жанр, чаще прозаический, зародившийся в Средние века у романских народов, как рассказ на народном языке и ныне превратившийся в самый распространённый вид эпической литературы, изображающий жизнь персонажа с её волнующими страстями, борьбой, социальными противоречиями и стремлениями к идеалу. Будучи развёрнутым повествованием о жизни и развитии личности главного героя (героев) в кризисный, нестандартный период его жизни, отличается от повести объёмом, сложностью содержания и более широким захватом описываемых явлений",
            "id": 1
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
        ["guest", 401, False, 1],
        ["admin_id1", 404, False, 100],
        ["admin_id1", 200, True, 1],
    ])
async def test_get_users(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/author/get_users/", cookies=cookies, params={'author_id': get_id, "returned": True})
    good_json = [
        {
            "email": "user1@test.ru",
            "born": "2024-12-29",
            "name": "user1",
            "id": 2,
            "role_id": 0,
            "verified": False,
        },
        {
            "email": "user3@test.ru",
            "born": "2024-12-29",
            "name": "user3",
            "id": 4,
            "role_id": 0,
            "verified": False,
        },
        {
            "email": "user4@test.ru",
            "born": "2024-12-29",
            "name": "user4",
            "id": 5,
            "role_id": 0,
            "verified": False,
        }
    ]
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json
