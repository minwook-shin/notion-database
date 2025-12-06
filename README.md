[![Test Python Package](https://github.com/minwook-shin/notion-database/actions/workflows/python-publish.yml/badge.svg)](https://github.com/minwook-shin/notion-database/actions/workflows/python-publish.yml)

#  Python Notion Database
> Database of Pythonic Notion API

<img alt="notion-database.gif" height="100%" src="https://github.com/minwook-shin/notion-database/blob/main/media/notion-database.gif?raw=true" width="100%"/>

created by database from the official Notion API.

"notion database" is Notion API wrapper library.

```python
import os

from notion_database.service.properties import Properties
from notion_database.const.query import Direction, Timestamp
from notion_database import NotionDatabase

result = NotionDatabase.search_database(integrations_token=os.getenv('NOTION_KEY'),
                                        sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})

for i in result:
  PROPERTY = Properties()
  PROPERTY.set_title("title", "title")
  PROPERTY.set_rich_text("Description", "description text")
  NotionDatabase.create_page(integrations_token=os.getenv('NOTION_KEY'), database_id=i["id"], properties=PROPERTY)
```
See detailed example [here](example.py).

## License Notice

hope that many people will use this package, also license has been changed to LGPL 3 from 1.0. 

previous version is GPL, please be careful when using this out of version.

## What's new notion-version

* 2.0
  * refactor the code to be more readable and maintainable.

* 1.0.0
  * Now that we've implemented all features, 
  * change the version rule to the semantic version.
  * notion-version : "2022-06-28"

* 2022.08.01
  * **Update notion-version (2022-06-28)**

* 2022.03.27
  * **Update notion-version (2022-02-22)**
    * Using officially API (out of beta!).
    * https://developers.notion.com/changelog/releasing-notion-version-2022-02-22
    
* 2021.09.01
    * **Update notion-version (2021-08-16)**

## Installing / Getting started

```shell
pip install notion-database
```

### Docs

https://notion-database.readthedocs.io

## Building / Developing

```shell
python setup.py install
```

## Features

* Blocks
  * ✅ Append block children
  * ✅ Retrieve block children
* Pages
  * ✅ Create a page
  * ✅ Retrieve a page
  * ✅ Retrieve a page property item
  * ✅ Update page properties
  * ✅ Archive a page
* Databases
  * ✅ Create a database
  * ✅ Query a database
    * See detailed example [here](query_db_example.py).
  * ✅ Retrieve a database
  * ✅ Update a database
  * ✅ Update database properties
* Blocks
  * ✅ Retrieve a block
  * ✅ Retrieve block children

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Links

- Notion API : https://developers.notion.com

## Licensing

The code in this project is licensed under LGPL license.

## Example project using this package

* jira-2-notion-db
  * https://github.com/minwook-shin/jira-2-notion-db