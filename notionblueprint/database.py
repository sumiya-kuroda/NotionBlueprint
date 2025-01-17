from glob import glob

import pandas as pd

from .auth import get_config, get_notionclient

DEFAULT_DATABASE = "main_db"


def get_database(database=None, return_https=False):
    if database is None:
        database = DEFAULT_DATABASE

    config = get_config()
    dbid = config.get("database_id")[database]

    if return_https:
        print("https://www.notion.so/{}".format(dbid))
    else:
        notion = get_notionclient()
        db = notion.databases.query(**{"database_id": dbid}).get("results")

        # do not close client

        return db, dbid, notion


def get_list_project(database=None):
    db, _, notion = get_database(database=database)

    db_df = pd.json_normalize(db)
    list_project = (
        db_df["properties.Project Directory.select.name"].unique().tolist()
    )

    notion.close()

    return list_project


def _retrieve_mousename(row):
    mousename = row["properties.Name.title"][0]["plain_text"]
    return mousename


def get_list_mouse(database=None):
    db, _, notion = get_database(database=database)

    db_df = pd.json_normalize(db)
    list_mouse = db_df.apply(_retrieve_mousename, axis=1).unique().tolist()

    notion.close()

    return list_mouse


def query_mouse(
    database=None,
    project=None,
    mouse=None,
    return_https=False,
    return_path=True,
):
    _, dbid, notion = get_database(database=database)
    if mouse is None:
        list_mouse = get_list_mouse(database)
        print("Here is a list of mice available:\n{}".format(list_mouse))

    response = notion.databases.query(
        **{
            "database_id": dbid,
            "filter": {
                "property": "Name",
                "title": {
                    "contains": mouse,
                },
            },
        }
    )
    results = response.get("results")

    if len(results) > 1:
        raise NotImplementedError("Found more than one registry!")
    mouse_page = results[0]

    if return_https:
        print("{}".format(mouse_page["url"]))

    proj_name = mouse_page["properties"]["Project Directory"]["select"]["name"]
    mouse_name = mouse_page["properties"]["Name"]["title"][0]["text"][
        "content"
    ]
    if return_path:
        path = glob(
            f"{get_config().get('path')}\
                      /{proj_name}/rawdata/{mouse_name}*"
        )
    else:
        path = ""
    notion_page_id = mouse_page["id"]

    notion.close()

    return {
        "project": proj_name,
        "mouse": mouse_name,
        "path": path,
        "notion_page_id": notion_page_id,
    }


def _retrieve_session(row):
    ses = row["properties.Session.title"][0]["plain_text"]
    return ses


def query_session(database=None, project=None, mouse=None, return_path=True):
    _, _, notion = get_database(database=database)
    mouse_page_data = query_mouse(
        database=database,
        project=project,
        mouse=mouse,
        return_path=return_path,
    )

    mouse_page_contents = notion.blocks.children.list(
        **{"block_id": mouse_page_data["notion_page_id"]}
    ).get("results")
    for child in mouse_page_contents:
        if child.get("type") == "child_database":
            if child.get("child_database").get("title") == "Experiment":
                session_db_id = child.get("id")

    response = notion.databases.query(**{"database_id": session_db_id}).get(
        "results"
    )
    response_df = pd.json_normalize(response)
    list_ses = response_df.apply(_retrieve_session, axis=1).unique().tolist()
    list_ses.sort()
    session_data = mouse_page_data

    if return_path:
        ses_path = [
            glob(
                f"{mouse_page_data['path']}\
                           /{ses}*"
            )
            for ses in list_ses
        ]
        session_data["path"] = ses_path
    else:
        pass

    session_data["session"] = list_ses
    session_data["response"] = response

    notion.close()

    return session_data
