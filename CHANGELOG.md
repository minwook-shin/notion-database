# Changelog

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
