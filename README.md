#  Python Notion Database
> Notion API Database Python Implementation

created only by database from the official Notion API.


## What's new

* 2022.03.27
  * **Update notion-version (2022-02-22)**
    * Using officially API (out of beta!).
    * https://developers.notion.com/changelog/releasing-notion-version-2022-02-22

* 2021.10.24
  * Children Blocks are now supported!

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

### Docs

https://notion-database.readthedocs.io

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

* Add Children Block with page

## Todo

* query database (wip)  # help me!

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Links

- Notion API : https://developers.notion.com

## Licensing

The code in this project is licensed under GPL license.