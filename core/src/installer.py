import platform
import time

import pyjson5
import questionary


def clear_terminal():
    if platform.system() == "Windows":
        import os

        os.system("cls")
    else:
        import os

        os.system("clear")


def generate_json_config(
    app_name, version, repo, description, db_username, db_password, features
):
    data = {
        "license": {"key": ""},
        "application": {
            "name": app_name,
            "version": version,
            "repo_link": repo,
            "description": description,
        },
        "developer_details": {
            "dashboard_login": {"username": db_username, "password": db_password}
        },
        "features": features,
    }

    return data


def make_json(data, filename):
    with open(filename, "w") as f:
        pyjson5.dump(data, f, indent=4)


def loading():
    for i in range(10):
        clear_terminal()
        print("Generating config file.")
        time.sleep(0.1)
        clear_terminal()
        print("Generating config file..")
        time.sleep(0.1)
        clear_terminal()
        print("Generating config file...")
        time.sleep(0.1)
    clear_terminal()
    print("Config file generated.")
    time.sleep(1)
    clear_terminal()


features_list = ["foo", "bar", "bazz"]

app_name = questionary.text("Enter your application's name").ask()
version = questionary.text("Version Number:").ask()
repo = questionary.text("Enter your repository URL").ask()
description = questionary.text("Enter your application's description").ask()

questionary.confirm("Are you sure?").ask()

db_username = questionary.text("Dashboard Username:").ask()
db_password = questionary.password("Dashboard Password:").ask()

questionary.confirm("Are you sure?").ask()

features = questionary.checkbox("Toggle Features", choices=features_list).ask()

questionary.confirm("Are you sure?").ask()

make_json(
    generate_json_config(
        app_name, version, repo, description, db_username, db_password, features
    ),
    "config.json5",
)
loading()
