# Changelog

## 1.2.0 (2024-03-26)

### Features

* Add support for is_inline param to create_database function
  * Notion API supports creating new databases as inline of parent pages.
  * https://github.com/minwook-shin/notion-database/pull/19
  * contribution by @cl-fl

## 1.1.0 (2023-5-30)

### Features

* Add retrieve block children
  * https://github.com/minwook-shin/notion-database/issues/16

## 1.0.0 (2023-5-28)

we've implemented all features, change the version rule to the semantic version.

and changed the license to LGPL 3 in the hope that many people use it.

### Features

* Apply tox, pylint tool
* Add type-hint code
* Implement run_query_database function
* Add support for Python 3.11

### Improvements

* Bump requests from 2.28.2 to 2.31.0

### Migration guide

* past version
```pycon
from notion_database.query import Direction, Timestamp
import notion_database.color as clr
```

* current version (>1.0.0)
```pycon
from notion_database.const.query import Direction, Timestamp
import notion_database.const.color as clr
```



### Deprecate

* Drop support for Python 3.7
* Deprecate query_database function
  * move to run_query_database function 

## 2022-06-28.8 (2023-04-22)

### Bug Fixes

* HOTFIX : Fix wrong path for new Cover and Icon features

## 2022-06-28.7 (2023-04-22)

### Features

* Add Cover and Icon for DB, Page
  * used to create and update method
  * optional parameter

### Bug Fixes

* FIX : fixed set_title, set_rich_text method
  * PROPERTY.set_rich_text("summary", "")
  * https://github.com/minwook-shin/notion-database/issues/13

### Tests

* Add cover, icon part test

## 2022-06-28.6 (2023-03-01)

### Bug Fixes

* HOTFIX : fixed set_number method
  * https://github.com/minwook-shin/notion-database/issues/12

## 2022-06-28.5 (2023-02-22)

### Bug Fixes

* Fix set_number method
  * https://github.com/minwook-shin/notion-database/issues/11

### Improvements

* Update requests (2.28.2)
* Update typing-extensions (4.5.0)

### Tests

* Add children part test

## 2022-06-28.4 (2023-01-15)

* Add property
  * Files Property.

* Add parameter
  * colors parameters for Children

## 2022-06-28.3 (2023-01-01)

HAPPY NEW YEAR!

### Features

* Add Date property
  * PROPERTY.set_date("date", "2022-12-31T01:01:01.000+0900")
  * PROPERTY.set_date("date", "2022-12-31T01:01:01.000+0900", "2023-01-10T01:01:01.000+0900")

### Improvements

* Fix set_checkbox bug

## 2022-06-28.2 (2022-10-10)

### Improvements

* Fix checkbox issue
  * https://github.com/minwook-shin/notion-database/issues/8

## 2022-06-28.1 (2022-08-01)

### Features

* Update notion-version 2022-06-28
* Add Search Pages with Pagination
* Add Query Databases with Pagination

### Improvements

* Update requests (2.28.1)
* Update typing-extensions (4.3.0)

### Deprecate

* Drop support for Python 3.6

## 2022-02-22.2 (2022-03-27)

### Bug Fixes

* Add python 3.6, 3.7 compatibility
  * typing-extensions

## 2022-02-22.1 (2022-03-27)

### Features

* Update notion-version 2022-02-22
* Add search_database, search_pages functions
* Add Direction, Timestamp Enum for search

### Improvements

* Update requests package version (2.27.1)

### Deprecate

* List databases
  * https://developers.notion.com/reference/get-databases

## 2021-08-16.4 (2022-01-23)

### Bug Fixes

* PR : Update setup.py
  * https://github.com/minwook-shin/notion-database/pull/5

## 2021-08-16.3 (2021-10-24)

### Bug Fixes

* hotfix : fix ModuleNotFoundError

## 2021-08-16.2 (2021-10-24)

### Features

* Add Children Blocks
  * paragraph
  * heading 1, heading 2, heading 3
  * callout
  * quote
  * bulleted, numbered list item
  * to do
  * toggle
  * code
  * embed
  * external image, video, file, pdf
  * bookmark
  * equation
  * divider, table of contents, breadcrumb

### Bug Fixes


### Deprecate

* Children.set_body

## 2021-08-16.1 (2021-09-01)

### Features

* Update notion-version 2021-08-16
  * https://developers.notion.com/changelog/notion-version-2021-08-16
  
* Get/Remove Properties and Update Database


### Bug Fixes

## 2021-05-13.7 (2021-07-15)

### Features

* Finding all pages in a database
  * https://github.com/minwook-shin/notion-database/issues/2

### Bug Fixes

## 2021-05-13.6 (2021-07-15)

### Features

* Add Create database
    * https://developers.notion.com/reference/create-a-database

### Bug Fixes

## 2021-05-13.5 (2021-07-13)

### Features

* Add Archive Page
    * https://developers.notion.com/reference/patch-page#archive-delete-a-page

### Bug Fixes

## 2021-05-13.4 (2021-07-11)

### Features

* Add check_field function

### Bug Fixes

* Database duplicate issue
    * https://github.com/minwook-shin/notion-database/issues/1

## 2021-05-13.3 (2021-07-03)

### Features

* Add list database
* Add Retrieve database
* Add update Page object
* Add Retrieve Page object

### Bug Fixes

## 2021-05-13.2 (2021-06-27)

### Features

### Bug Fixes

* Fix module path

## 2021-05-13.1 (2021-06-27)

### Features

* Initial project
* Add Create Page object
