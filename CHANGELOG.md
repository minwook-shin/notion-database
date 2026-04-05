# Changelog

## 2.0.0 (2026-04-05)

Complete redesign of the package API.  All v1.x classes have been removed and
replaced with a single `NotionClient` entry point backed by purpose-built
resource sub-clients.  Notion API version bumped to **`2026-03-11`**.

### Breaking Changes

The entire public API has been redesigned.  v1.x code is **not compatible**
with 2.0.  Migration notes:

| v1.x | v2.0 |
|---|---|
| `Page(token)` | `NotionClient(token).pages` |
| `Database(token)` | `NotionClient(token).databases` |
| `Block(token)` | `NotionClient(token).blocks` |
| `Search(token)` | `NotionClient(token).search` |
| `Properties().set_title(col, text)` | `{col: PropertyValue.title(text)}` |
| `Children().set_paragraph(text)` | `BlockContent.paragraph(text)` |
| `Cover().set_cover_image(url)` | `Cover.external(url)` |
| `Icon().set_icon_emoji(emoji)` | `Icon.emoji(emoji)` |
| `const.query.Direction` | `Sort.by_property(..., "ascending" \| "descending")` |

### New Features

* **`NotionClient`** – single entry point; all resources accessed via
  `client.databases`, `client.pages`, `client.blocks`, `client.search`,
  `client.users`, `client.comments`
* **1-to-1 Notion API mapping** – every method name and parameter matches the
  Notion REST API exactly, making the official docs directly usable
* **`PropertyValue`** – static factory methods for page property values
  (`title`, `rich_text`, `number`, `select`, `multi_select`, `status`,
  `date`, `checkbox`, `url`, `email`, `phone_number`, `people`, `files`,
  `relation`, `unique_id`, `verification`)
* **`PropertySchema`** – static factory methods for database column schemas
  (`title`, `rich_text`, `number`, `select`, `multi_select`, `status`,
  `date`, `checkbox`, `url`, `email`, `phone_number`, `people`, `files`,
  `relation`, `rollup`, `formula`, `created_time`, `created_by`,
  `last_edited_time`, `last_edited_by`, `unique_id`, `verification`,
  `button`, `location`, `last_visited_time`)
* **`BlockContent`** – static factory methods for all supported block types
  (`paragraph`, `heading_1/2/3`, `callout`, `quote`, `bulleted_list_item`,
  `numbered_list_item`, `to_do`, `toggle`, `code`, `image`, `video`, `file`,
  `pdf`, `embed`, `bookmark`, `divider`, `table_of_contents`, `breadcrumb`,
  `equation`, `column_list`, `tab`, `tab_group`)
* **`RichText`** – rich-text element builder (`text`, `mention_page`,
  `mention_database`, `mention_user`, `mention_date`, `equation`)
* **`Filter`** – fluent filter builder for database queries covering all
  property types (`text`, `title`, `number`, `checkbox`, `select`,
  `multi_select`, `status`, `date`, `people`, `files`, `relation`,
  `url`, `email`, `phone_number`, `unique_id`, `created_by`,
  `last_edited_by`, `formula`, `rollup`, `verification`) plus compound
  `and_`/`or_` and timestamp filters (`created_time`, `last_edited_time`)
* **`Sort`** – sort builder (`by_property`, `by_timestamp`, `ascending`,
  `descending`)
* **`Icon` / `Cover`** – icon and cover object builders
* **Auto-pagination helpers** – `databases.query_all()`,
  `blocks.retrieve_all_children()`, `users.list_all()`, `search.search_all()`
* **Typed exceptions** – `NotionAPIError` with subclasses
  `NotionValidationError`, `NotionUnauthorizedError`, `NotionForbiddenError`,
  `NotionNotFoundError`, `NotionConflictError`, `NotionRateLimitError`,
  `NotionInternalError`
* **Users API** – `users.retrieve()`, `users.list()`, `users.list_all()`,
  `users.me()`
* **Comments API** – `comments.retrieve()`, `comments.create()`
* Dropped `urllib3<2.0` constraint
* Minimum Python version raised to 3.10

### Notion API 2026-03-11 additions

* **`pages.retrieve_markdown(page_id)`** – retrieve page content as enhanced
  Markdown (`GET /pages/{id}/markdown`)
* **`pages.update_markdown(page_id, markdown)`** – replace page content with
  Markdown (`POST /pages/{id}/markdown`)
* **`pages.create(timezone=...)`** – IANA timezone string for resolving
  template variables (`@now`, `@today`)
* **`blocks.append_children(position=...)`** – insert blocks at `"start"`,
  `"end"`, or `"after_block"` instead of always appending to the end
* **`databases.query(in_trash=...)`** – filter trashed / non-trashed rows
* **`databases.query_all(in_trash=...)`** – same param forwarded through the
  auto-pagination helper
* **`databases.create(initial_data_source=...)`** – pre-populate a new
  database from a data source on creation
* **`databases.update(is_inline=..., in_trash=..., is_locked=...)`** – toggle
  inline layout, move to trash, or lock the database
* **`PropertySchema.button()`** – automation button column
* **`PropertySchema.location()`** – geographic location column
* **`PropertySchema.last_visited_time()`** – read-only last-visited-time column
* **`PropertySchema.rollup(relation_property_id=..., rollup_property_id=...)`**
  – optional ID-based lookup params for stable rollup definitions
* **`PropertySchema.verification()`** – wiki page verification column
* **`PropertyValue.verification()`** – set verification state on wiki pages
* **`BlockContent.tab()` / `tab_group()`** – tab layout blocks
* **`Filter.created_by()`** / **`Filter.last_edited_by()`** – filter by
  creator or last editor
* **`Filter.formula(name, value_type)`** – filter on formula property results
  (`"string"`, `"number"`, `"checkbox"`, `"date"`)
* **`Filter.rollup(name, aggregate, value_type)`** – filter on rollup
  aggregates (`"any"`, `"every"`, `"none"`, `"number"`)
* **`Filter.verification()`** – filter on wiki verification state

## 1.4.1 (2026-04-05)

### Bug Fixes

* Fix `Search.search_pages()` pagination — when `start_cursor` was provided, a second
  unconditional API call immediately overwrote the result, making pagination effectively broken
* Fix `Properties.set_date()` silently dropping `end` when `start` is not provided — the `end`
  date is now correctly included alongside the auto-generated `start` (current datetime)

### Improvements

* Add `response.raise_for_status()` to all HTTP methods in `Request`
  (`call_api_post`, `call_api_get`, `call_api_patch`) so HTTP 4xx/5xx errors
  raise an exception immediately instead of silently returning an error JSON object

### Code Quality

* Add `Optional[str]` to all parameters that accept `None` as a default value
  (`start_cursor`, `text`, `url`) across `Block`, `Database`, `Page`, `Search`,
  `Icon`, and `Cover`
* Fix PEP 8 spacing in `Database`: `page_size:int =100` → `page_size: int = 100`,
  `title:str` → `title: str`
* Add missing `: str` type annotation to `Page.__init__` `integrations_token` parameter

## 1.4.0 (2026-04-04)

### Features

* Add relation property support — finally resolving [#9](https://github.com/minwook-shin/notion-database/issues/9), open since Nov 21, 2022, with the help of vibe coding!
  * Add `Properties.set_relation()` to set relation values (list of page IDs) or define relation schema for database columns
* Add `Page.retrieve_page_property()` to fetch full property values via `/pages/{page_id}/properties/{property_id}` endpoint
  * Required to read relation data that Notion API truncates in query results

### Dependency

* Update requests library to 2.33.1

### Python Version Support

* Drop Python 3.8, 3.9 support
* Add Python 3.13, 3.14 support

## 1.3.0 (2025-06-28)

### Features
* Add Feature to get Created Time and Last Edited Time of a Page
* Add Feature to get Created By and Last Edited By of a Page
    * Issue #30 : Request to Add Feature to get Create Time
    * https://github.com/minwook-shin/notion-database/issues/30

### Dependency

* Update requests library to 2.32.4
  * Version 2.32.4 of the requests library includes security fixes.

## 1.2.2 (2024-09-09)

### Dependency

* Update requests library to 2.32.3
  * https://github.com/minwook-shin/notion-database/issues/22
* Update setuptools library to 74.1.2
  * fix security issue

## 1.2.1 (2024-06-03)

### Dependency

* Update requests library to 2.32.0
  * #20 Bump requests from 2.31.0 to 2.32.0

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
