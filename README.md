#  Python Notion Database
> Notion API Database Python Implementation

created only by database from the official Notion API.

## Installing / Getting started

```shell
pip install notion-database
```

```python
import os
import pprint

from notion_database.database import Database
from notion_database.page import Page
from notion_database.properties import Properties, Children

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

NOTION_KEY = os.getenv('NOTION_KEY')

PROPERTY = Properties()
PROPERTIES = {
    "name": PROPERTY.set_title("title"),
    "description": PROPERTY.set_rich_text("description"),
    "number": PROPERTY.set_number(1),
    "select": PROPERTY.set_select("test1"),
    "multi_select": PROPERTY.set_multi_select(["test1", "test2"]),
    "checkbox": PROPERTY.set_checkbox(True),
    "url": PROPERTY.set_url("www.google.com"),
    "email": PROPERTY.set_email("test@test.com"),
    "phone": PROPERTY.set_phone_number("010-0000-0000"),
}

# List Database
D = Database(integrations_token=NOTION_KEY)
D.list_databases(page_size=100)

for i in D.result["results"]:
    database_id = i["id"]

    # Retrieve Database
    D = Database(integrations_token=NOTION_KEY)
    D.retrieve_database(database_id=database_id)
    pprint.pprint(D.result)

    # Create Page
    P = Page(integrations_token=NOTION_KEY, database_id=database_id)
    P.create_page(properties=PROPERTIES, children=[Children().set_body("hello world!")])

    # Retrieve Page
    page_id = P.result["id"]
    P.retrieve_page(page_id=page_id)
    pprint.pprint(P.result)

    PROPERTIES = {
        "name": PROPERTY.set_title("Custom_title"),
        "description": PROPERTY.set_rich_text("Custom_description"),
        "number": PROPERTY.set_number(2),
    }

    # Update Page
    P.update_page(page_id=page_id, properties=PROPERTIES)
    pprint.pprint(P.result)
```

## Building / Developing

```shell
python setup.py install
```

## Features

* list database
* Retrieve database

* Create Page object (the database item)
* update Page object 
* Retrieve Page object

## Todo

* query database

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Links

- Notion API : https://developers.notion.com

## Licensing

The code in this project is licensed under GPL license.