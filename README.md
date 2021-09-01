#  Python Notion Database
> Notion API Database Python Implementation

created only by database from the official Notion API.


## What's new

* 2021.07.13
    * Archive Page
        * https://developers.notion.com/reference/patch-page#archive-delete-a-page
    
* 2021.07.15
    * Create new databases
        * https://developers.notion.com/changelog/create-new-databases-with-post-databases
    
* 2021.09.01
    * **Update notion-version (2021-08-16)**
    * Get/Remove Properties & Update Database

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

* For Database

```python
from notion_database.properties import Properties

PROPERTY = Properties()
PROPERTY.set_title("name")
PROPERTY.set_rich_text("description")
PROPERTY.set_number("number")
PROPERTY.set_select("select")
PROPERTY.set_multi_select("multi_select")
PROPERTY.set_checkbox("checkbox")
PROPERTY.set_url("url")
PROPERTY.set_email("email")
PROPERTY.set_phone_number("phone")
```

* For Page

```python
from notion_database.properties import Properties

PROPERTY = Properties()
PROPERTY.set_title("name", "title")
PROPERTY.set_rich_text("description", "notion-database")
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

### Create database

```python
from notion_database.database import Database

D = Database(integrations_token=NOTION_KEY)
D.create_database(page_id=page_id, title="TEST TITLE", properties=PROPERTY)
```

### Finding all pages in a database

```python
from notion_database.database import Database
import pprint

D = Database(integrations_token=NOTION_KEY)
D.find_all_page(database_id=database_id)
pprint.pprint(D.result)
```

### Get Properties

```python
from notion_database.database import Database

D = Database(integrations_token=NOTION_KEY)
D.retrieve_database(database_id, get_properties=True)
properties_list = D.properties_list
```

### Remove Properties / Update Database

```python
from notion_database.database import Database

D = Database(integrations_token=NOTION_KEY)
D.update_database(database_id=database_id, title="DB", add_properties=PROPERTY)
```

or 

```python
from notion_database.database import Database

D = Database(integrations_token=NOTION_KEY)
D.update_database(database_id=database_id, title="DB", remove_properties=D.properties_list)
```

or 

```python
from notion_database.database import Database

D = Database(integrations_token=NOTION_KEY)
D.update_database(database_id=database_id, title="DB", remove_properties=D.properties_list, add_properties=PROPERTY)
```
    
## Building / Developing

```shell
python setup.py install
```

## Features

* list database
* Retrieve database
* Create database

* Create Page object (the database item)
* update Page object 
* Retrieve Page object

* Archive Page

* Finding all pages in a database

* Get Properties
* Remove Properties 
* Update Database

## Todo

* query database (wip)  # help me!

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Links

- Notion API : https://developers.notion.com

## Licensing

The code in this project is licensed under GPL license.