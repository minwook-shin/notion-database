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

from notion_database.page import Page
from notion_database.properties import Properties, Children

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

NOTION_KEY = os.getenv('NOTION_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

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

PAGE = Page(integrations_token=NOTION_KEY, database_id=NOTION_DATABASE_ID)
PAGE.create_page(properties=PROPERTIES, children=[Children().set_body("hello world!")])
pprint.pprint(PAGE.result)
```

## Building / Developing

```shell
python setup.py install
```

## Features

* Create Page object (the database item)

## Todo

* update Page object 
* Retrieve Page object

* Retrieve database
* query database
* list database

 
## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Links

- Related projects:
  - Notion API : https://developers.notion.com

## Licensing

The code in this project is licensed under GPL license.