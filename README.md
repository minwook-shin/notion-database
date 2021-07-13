#  Python Notion Database
> Notion API Database Python Implementation

created only by database from the official Notion API.


## What's new

* 2021.07.13
    * Archive Page
        * https://developers.notion.com/reference/patch-page#archive-delete-a-page

## Installing / Getting started

```shell
pip install notion-database
```

### List Database

```python
from notion_database.database import Database

D = Database(integrations_token=NOTION_KEY)
D.list_databases(page_size=100)
```

### Retrieve Database

```python
from notion_database.database import Database

D = Database(integrations_token=NOTION_KEY)
D.retrieve_database(database_id=database_id)
```

### Properties

```python
from notion_database.properties import Properties

PROPERTY = Properties()
PROPERTY.set_title("name", "title")
PROPERTY.set_rich_text("description", "notion-datebase")
PROPERTY.set_number("number", 1)
PROPERTY.set_select("select", "test1")
PROPERTY.set_multi_select("multi_select", ["test1", "test2"])
PROPERTY.set_checkbox("checkbox", True)
PROPERTY.set_url("url", "www.google.com")
PROPERTY.set_email("email", "test@test.com")
PROPERTY.set_phone_number("phone", "010-0000-0000")
```

### Children

```python
from notion_database.properties import Children

children = Children()
children.set_body("hello world!")
```

### Create Page

```python
from notion_database.page import Page

P = Page(integrations_token=NOTION_KEY)
P.create_page(database_id=database_id, properties=PROPERTY, children=children)
page_id = P.result["id"]
```

### Retrieve Page

```python
from notion_database.page import Page

P = Page(integrations_token=NOTION_KEY)
P.retrieve_page(page_id=page_id)
```

### Update Page

```python
from notion_database.page import Page

P = Page(integrations_token=NOTION_KEY)
P.update_page(page_id=page_id, properties=PROPERTY)
```

### Clear Properties

```python
from notion_database.properties import Properties

PROPERTY = Properties()
PROPERTY.clear()
```

### Archive Page

```python
from notion_database.page import Page

P = Page(integrations_token=NOTION_KEY)
P.archive_page(page_id=page_id, archived=True)
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

* Archive Page

## Todo

* query database

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Links

- Notion API : https://developers.notion.com

## Licensing

The code in this project is licensed under GPL license.