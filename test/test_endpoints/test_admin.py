import pytest
from datetime import date, timedelta

# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, get_id",
    [
        ["guest", 401, False, 2],
        ["user_id2", 403, False, 2],
        ["admin_id1", 200, True, 2],
        ["admin_id1", 404, False, 100],
    ])
async def test_get_user_info(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/admin/get_user_info/", cookies=cookies, params={"get_id": get_id})
    good_json = {
        "email": "user1@test.ru",
        "born": "2024-12-29",
        "name": "user1",
        "id": 2,
        "role_id": 0,
        "verified": False
    }
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json


# @pytest.mark.skip
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_role, test_code, check_json, get_id",
    [
        ["user_fake", 400, False, 2],
        ["user_text", 400, False, 2],
        ["guest", 401, False, 2],
        ["user_id2", 403, False, 2],
        ["admin_id1", 200, True, 2],
        ["admin_id1", 404, False, 100],
    ])
async def test_get_user_s__books(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/admin/get_user_s__books/", cookies=cookies, params={"get_id": get_id, "returned": True})
    good_json = [
        {
            "name": "Война и мир",
            "description": "Роман-эпопея Льва Николаевича Толстого, описывающий русское общество в эпоху войн против Наполеона в 1805—1812 годах. Эпилог романа доводит повествование до 1820 года",
            "publish_year": 1865,
            "amount": 6,
            "id": 2
        },
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
        ["guest", 401, False, 2],
        ["user_id2", 403, False, 2],
        ["admin_id1", 200, True, 2],
        ["admin_id1", 404, False, 100],
    ])
async def test_get_user_s__genres(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/admin/get_user_s__genres/", cookies=cookies, params={"get_id": get_id, "returned": True})
    good_json = [
        {
            "name": "Роман",
            "description": "Литературный жанр, чаще прозаический, зародившийся в Средние века у романских народов, как рассказ на народном языке и ныне превратившийся в самый распространённый вид эпической литературы, изображающий жизнь персонажа с её волнующими страстями, борьбой, социальными противоречиями и стремлениями к идеалу. Будучи развёрнутым повествованием о жизни и развитии личности главного героя (героев) в кризисный, нестандартный период его жизни, отличается от повести объёмом, сложностью содержания и более широким захватом описываемых явлений",
            "id": 1
        },
        {
            "name": "Эпопея",
            "description": "Обширное эпическое повествование в стихах или прозе о выдающихся национально-исторических событиях. В переносном смысле: сложная, продолжительная история чего-либо, включающая ряд крупных событий.",
            "id": 2
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
        ["guest", 401, False, 2],
        ["user_id2", 403, False, 2],
        ["admin_id1", 200, True, 2],
        ["admin_id1", 404, False, 100],
    ])
async def test_get_user_s__authors(client, create, get_tokens, test_role, test_code, check_json, get_id):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/admin/get_user_s__authors/", cookies=cookies, params={"get_id": get_id, "returned": True})
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
        },
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
    "test_role, test_code, check_json, returned",
    [
        ["guest", 401, False, True],
        ["user_id2", 403, False, True],
        ["admin_id1", 200, True, True],
        ["admin_id1", 422, False, None],
    ])
async def test_get_users_overdue(client, create, get_tokens, test_role, test_code, check_json, returned):
    cookies = {'access_token': get_tokens[test_role]}
    response = client.get("/admin/get_users_overdue/", cookies=cookies, params={"returned": returned})
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
                    "id": 1,
                    "left_id": 2,
                    "right_id": 1,
                    "get_at": str(date.today() - timedelta(days=2 + 14)),
                    "must_return_at": str(date.today() - timedelta(days=2)),
                    "returned_at": str(date.today() - timedelta(days=5)),
                    "returned": True,
                    "book": {
                        "name": "Двенадцать стульев",
                        "description": "Роман Ильи Ильфа и Евгения Петрова, написанный в 1927 году и являющийся первой совместной работой соавторов. В 1928 году опубликован в художественно-литературном журнале «Тридцать дней» (№ 1—7); в том же году издан отдельной книгой. В основе сюжета — поиски бриллиантов, спрятанных в одном из двенадцати стульев мадам Петуховой, однако история, изложенная в произведении, не ограничена рамками приключенческого жанра: в ней, по мнению исследователей, дан «глобальный образ эпохи».",
                        "publish_year": 1928,
                        "amount": 5,
                        "id": 1
                    }
                },
                {
                    "id": 2,
                    "left_id": 2,
                    "right_id": 2,
                    "get_at": str(date.today() - timedelta(days=5 + 14)),
                    "must_return_at": str(date.today() - timedelta(days=5)),
                    "returned_at": str(date.today() - timedelta(days=2)),
                    "returned": True,
                    "book": {
                        "name": "Война и мир",
                        "description": "Роман-эпопея Льва Николаевича Толстого, описывающий русское общество в эпоху войн против Наполеона в 1805—1812 годах. Эпилог романа доводит повествование до 1820 года",
                        "publish_year": 1865,
                        "amount": 6,
                        "id": 2
                    }
                }
            ]
        }
    ]
    assert response.status_code == test_code
    if check_json:
        assert response.json() == good_json
