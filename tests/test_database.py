from notionblueprint import database

TEST_DATABASE = "test_db"


def test_get_database():
    _, _, notion = database.get_database(database=TEST_DATABASE)
    notion.close()


def test_get_list_project():
    list_project = database.get_list_project(database=TEST_DATABASE)
    assert len(list_project) == 2


def test_get_list_mouse():
    list_mouse = database.get_list_mouse(database=TEST_DATABASE)
    assert len(list_mouse) == 2


def test_query_mouse():
    mouse_data = database.query_mouse(
        database=TEST_DATABASE, mouse="SK001", return_path=False
    )
    assert (
        mouse_data["notion_page_id"] == "17ec2c1a-d6a4-81c5-ad8e-d0a5f394a8b3"
    )


def test_query_session():
    session_data = database.query_session(
        database=TEST_DATABASE, mouse="SK001", return_path=False
    )
    assert len(session_data["session"]) == 2
