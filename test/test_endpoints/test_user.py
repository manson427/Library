import pytest

#@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json",
    [
        ["guest", 401, False, ],
        ["user_id2", 200, True, ],
    ])
async def test_get_me(client, create, get_tokens, test_role, test_code, check_json):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/user/get_me/", cookies=cookies)
    good_json = {
        "email": 'user1@test.ru',
        "born": "2024-12-29",
        "name": "user1",
        "id": 2,
        "role_id": 0,
        "verified": False
    }
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json


#@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, born",
    [
        ["guest", 401, False, '2023-01-31'],
        ["user_id2", 200, True, '2023-01-31'],
        ["user_id2", 422, False, '2023-123-31'],
    ])
async def test_update_me(client, create, get_tokens, test_role, test_code, check_json, born):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.post("/user/update_me/", cookies=cookies, json={
        'email': 'user@example.com',
        'born': born})
    good_json = {
      "email": "user@example.com",
      "born": "2023-01-31",
      "name": "user1",
      "id": 2,
      "role_id": 0,
      "verified": False
    }
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json


#@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, path, data, detail",
    [
        ["guest", 401, 'delete', {}, 'Invalid token'],
        ["user_id4", 409, 'delete', {}, 'Can not delete user, because there are 1 taken books' ],
        ["user_id4", 200, 'return_book', {'book_id': 2}, 'You successfully return Book with id=2'],
        ["user_id4", 409, 'delete', {}, 'Can not delete user, because there are 2 returned books' ],
        ["user_id4", 200, 'delete_all_links_book', {}, '2 links User to Book with User id=4 deleted'],
        ["user_id4", 200, 'delete', {}, "User 'user3' with id=4 deleted" ],
    ])
async def test_delete(client, create, get_tokens, test_role, test_code, path, data: dict, detail):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.post(f"/user/{path}/", cookies=cookies, params=data)
    assert response.status_code == test_code
    assert response.json()['detail'] == detail

#@pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, path, data, detail",
    [
        ["guest", 401, 'take_book', {'book_id': 1}, 'Invalid token'],

        ["user_id3", 409, 'take_book', {'book_id': 1}, 'You already have same book'],
        ["user_id3", 409, 'take_book', {'book_id': 1}, 'You already have same book'],
        ["user_id3", 409, 'take_book', {'book_id': 3}, 'You have too many books'],
        ["user_id3", 409, 'return_book', {'book_id': 3}, 'You have not this book'],
        ["user_id3", 200, 'return_book', {'book_id': 1}, 'You successfully return Book with id=1'],
        ["user_id3", 409, 'take_book', {'book_id': 3}, 'First, you must receive overdue book'],
        ["user_id3", 200, 'return_book', {'book_id': 2}, 'You successfully return Book with id=2'],
        ["user_id3", 409, 'take_book', {'book_id': 3}, 'Not enough copies of the book'],
        ["user_id2", 200, 'return_book', {'book_id': 3}, 'You successfully return Book with id=3'],
        ["user_id3", 404, 'take_book', {'book_id': 100}, 'Error'],
        ["user_id3", 200, 'take_book', {'book_id': 3}, 'You successfully take Book with id=3'],
    ])
async def test_take_return_book(client, create, get_tokens, test_role, test_code, path, data: dict, detail):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.post(f"/user/{path}/", cookies=cookies, params=data)
    assert response.status_code == test_code
    assert response.json()['detail'] == detail


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, returned",
    [
        ["guest", 401, False, True],
        ["user_id5", 200, True, True],
        ["user_id5", 422, False, None],
    ])
async def test_get_my_books(client, create, get_tokens, test_role, test_code, check_json, returned):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/user/get_my_books/", cookies=cookies, params={"returned": returned})
    good_json = [
        {
            "name": "Двенадцать стульев",
            "description": "Роман Ильи Ильфа и Евгения Петрова, написанный в 1927 году и являющийся первой совместной работой соавторов. В 1928 году опубликован в художественно-литературном журнале «Тридцать дней» (№ 1—7); в том же году издан отдельной книгой. В основе сюжета — поиски бриллиантов, спрятанных в одном из двенадцати стульев мадам Петуховой, однако история, изложенная в произведении, не ограничена рамками приключенческого жанра: в ней, по мнению исследователей, дан «глобальный образ эпохи».",
            "publish_year": 1928,
            "amount": 6,
            "id": 1
        }
    ]
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, returned",
    [
        ["guest", 401, False, True],
        ["user_id2", 200, True, True],
        ["user_id2", 422, False, None],
    ])
async def get_my_genres(client, create, get_tokens, test_role, test_code, check_json, returned):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/user/get_my_genres/", cookies=cookies, params={"returned": returned})
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
    "test_role, test_code, check_json, returned",
    [
        ["guest", 401, False, True],
        ["user_id2", 200, True, True],
        ["user_id2", 422, False, None],
    ])
async def get_my_authors(client, create, get_tokens, test_role, test_code, check_json, returned):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/user/get_my_authors/", cookies=cookies, params={"returned": returned})
    good_json = [
        {
            "name": "Евгений Петрович Петров",
            "biography": "Русский советский писатель, сценарист и драматург, журналист, военный корреспондент. Кавалер ордена Ленина (1939). Член ВКП(б) с 1939 года.",
            "born": "1902-12-30",
            "id": 2
        },
        {
            "name": "Илья Арнольдович Ильф",
            "biography": "Русский советский писатель, драматург и сценарист, фотограф, журналист",
            "born": "1897-10-15",
            "id": 1
        }
    ]
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json

