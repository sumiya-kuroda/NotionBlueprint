from notionblueprint import auth


def test_get_notionclient():
    _ = auth.get_notionclient()


def test_get_config():
    config = auth.get_config()
    assert len(config.keys()) == 3
