notion-database
===============

`GitHub <https://github.com/minwook-shin/notion-database>`_ |
`PyPI <https://pypi.org/project/notion-database/>`_ |
`Issue Tracker <https://github.com/minwook-shin/notion-database/issues>`_

Notion 공식 API를 위한 Python 클라이언트입니다.
``NotionClient`` 하나로 시작하고, 빌더 클래스로 값을 조립하여 사용합니다.

설치
----

.. code:: shell

   pip install notion-database

시작하기
--------

Notion Integration Token을 발급받아 환경변수에 설정합니다.

.. code:: shell

   export NOTION_KEY=secret_xxx

.. code:: python

   from notion_database import NotionClient

   client = NotionClient("secret_xxx")

이후 모든 기능은 ``client.databases``, ``client.pages``, ``client.blocks``,
``client.search``, ``client.users``, ``client.comments`` 로 접근합니다.

----

데이터베이스
------------

데이터베이스 검색
~~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database import NotionClient, Sort

   client = NotionClient("secret_xxx")

   result = client.search.search_databases(
       sort={"direction": "ascending", "timestamp": "last_edited_time"},
   )
   for db in result["results"]:
       print(db["id"])

데이터베이스 조회
~~~~~~~~~~~~~~~~~

.. code:: python

   db = client.databases.retrieve("database-id")

데이터베이스 생성
~~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database import NotionClient, PropertySchema, RichText, Icon, Cover

   client = NotionClient("secret_xxx")

   db = client.databases.create(
       parent={"type": "page_id", "page_id": "page-id"},
       title=[RichText.text("내 데이터베이스")],
       properties={
           "이름":   PropertySchema.title(),
           "상태":   PropertySchema.select([
                         {"name": "진행 중", "color": "blue"},
                         {"name": "완료",   "color": "green"},
                     ]),
           "점수":   PropertySchema.number("number"),
           "날짜":   PropertySchema.date(),
           "체크":   PropertySchema.checkbox(),
       },
       icon=Icon.emoji("📋"),
   )

데이터베이스 업데이트
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from notion_database import RichText, Icon

   client.databases.update(
       "database-id",
       title=[RichText.text("새 이름")],
       icon=Icon.emoji("🗂️"),
   )

----

페이지
------

페이지 생성
~~~~~~~~~~~

``properties`` 의 키는 데이터베이스 컬럼 이름과 일치해야 합니다.

.. code:: python

   from notion_database import NotionClient, PropertyValue, BlockContent, Icon, Cover

   client = NotionClient("secret_xxx")

   page = client.pages.create(
       parent={"database_id": "database-id"},
       properties={
           "이름": PropertyValue.title("새 페이지"),
           "상태": PropertyValue.select("진행 중"),
           "점수": PropertyValue.number(100),
           "날짜": PropertyValue.date("2024-12-31"),
           "체크": PropertyValue.checkbox(False),
       },
       icon=Icon.emoji("🚀"),
       cover=Cover.external("https://example.com/cover.jpg"),
       children=[
           BlockContent.heading_1("소개"),
           BlockContent.paragraph("notion-database 2.0 으로 만든 페이지입니다."),
       ],
   )
   page_id = page["id"]

페이지 조회
~~~~~~~~~~~

.. code:: python

   page = client.pages.retrieve("page-id")

페이지 업데이트
~~~~~~~~~~~~~~~

.. code:: python

   from notion_database import PropertyValue

   client.pages.update(
       "page-id",
       properties={
           "상태": PropertyValue.select("완료"),
           "체크": PropertyValue.checkbox(True),
       },
   )

페이지 아카이브 / 복원
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   client.pages.archive("page-id")                    # 아카이브
   client.pages.archive("page-id", archived=False)    # 복원

----

속성(Property) 값 종류
-----------------------

페이지를 생성하거나 업데이트할 때 ``PropertyValue`` 로 값을 만듭니다.

.. code:: python

   from notion_database import PropertyValue, RichText

   {
       "이름":       PropertyValue.title("제목"),
       "설명":       PropertyValue.rich_text("내용"),
       "숫자":       PropertyValue.number(42),
       "단일선택":   PropertyValue.select("옵션A"),
       "다중선택":   PropertyValue.multi_select(["태그1", "태그2"]),
       "상태":       PropertyValue.status("진행 중"),
       "날짜":       PropertyValue.date("2024-01-01"),
       "날짜범위":   PropertyValue.date("2024-01-01", end="2024-01-31"),
       "체크박스":   PropertyValue.checkbox(True),
       "URL":        PropertyValue.url("https://example.com"),
       "이메일":     PropertyValue.email("hello@example.com"),
       "전화번호":   PropertyValue.phone_number("010-1234-5678"),
       "파일":       PropertyValue.files(["https://example.com/file.pdf"]),
       "관계":       PropertyValue.relation(["other-page-id"]),
       "담당자":     PropertyValue.people(["user-id"]),
   }

데이터베이스 컬럼 스키마를 정의할 때는 ``PropertySchema`` 를 사용합니다.

.. code:: python

   from notion_database import PropertySchema

   {
       "이름":   PropertySchema.title(),
       "설명":   PropertySchema.rich_text(),
       "점수":   PropertySchema.number("number"),
       "선택":   PropertySchema.select([{"name": "A"}, {"name": "B"}]),
       "다중":   PropertySchema.multi_select(),
       "날짜":   PropertySchema.date(),
       "체크":   PropertySchema.checkbox(),
       "URL":    PropertySchema.url(),
       "수식":   PropertySchema.formula("prop('점수') * 2"),
       "관계":   PropertySchema.relation("other-database-id"),
   }

----

블록 콘텐츠
-----------

페이지 콘텐츠를 추가할 때 ``BlockContent`` 를 사용합니다.

.. code:: python

   from notion_database import NotionClient, BlockContent, RichText
   from notion_database.const import BLUE, RED_BACKGROUND

   client = NotionClient("secret_xxx")

   client.blocks.append_children("page-id", children=[
       BlockContent.heading_1("제목 1"),
       BlockContent.heading_2("제목 2"),
       BlockContent.heading_3("제목 3"),

       BlockContent.paragraph("일반 단락"),
       BlockContent.paragraph("색상 단락", color=BLUE),
       BlockContent.paragraph([
           RichText.text("굵게", bold=True),
           RichText.text(", "),
           RichText.text("기울임", italic=True),
           RichText.text(", "),
           RichText.text("링크", link="https://example.com"),
       ]),

       BlockContent.callout("주의 사항", color=RED_BACKGROUND),
       BlockContent.quote("인용구"),

       BlockContent.bulleted_list_item("불릿 항목"),
       BlockContent.numbered_list_item("순서 항목"),
       BlockContent.to_do("할 일", checked=False),
       BlockContent.toggle("토글", children=[
           BlockContent.paragraph("숨겨진 내용"),
       ]),

       BlockContent.code('print("hello")', language="python"),
       BlockContent.equation("E = mc^2"),

       BlockContent.image("https://example.com/image.png", caption="그림"),
       BlockContent.video("https://example.com/video.mp4"),
       BlockContent.embed("https://www.youtube.com/watch?v=xxx"),
       BlockContent.bookmark("https://example.com"),

       BlockContent.divider(),
       BlockContent.table_of_contents(),

       BlockContent.column_list([
           [BlockContent.paragraph("왼쪽")],
           [BlockContent.paragraph("오른쪽")],
       ]),
   ])

블록 조회
~~~~~~~~~

.. code:: python

   # 첫 페이지
   response = client.blocks.retrieve_children("page-id")
   blocks = response["results"]

   # 전체 자동 수집
   all_blocks = client.blocks.retrieve_all_children("page-id")

----

쿼리 (필터 / 정렬)
------------------

``Filter`` 와 ``Sort`` 로 데이터베이스를 검색합니다.

.. code:: python

   from notion_database import NotionClient, Filter, Sort

   client = NotionClient("secret_xxx")

   # 단순 필터
   result = client.databases.query(
       "database-id",
       filter=Filter.select("상태").equals("진행 중"),
       sorts=[Sort.descending("날짜")],
   )

   # OR 복합 필터
   result = client.databases.query(
       "database-id",
       filter=Filter.or_([
           Filter.checkbox("체크").equals(False),
           Filter.number("점수").greater_than(90),
       ]),
   )

   # AND + OR 중첩 필터
   result = client.databases.query(
       "database-id",
       filter=Filter.and_([
           Filter.text("이름").is_not_empty(),
           Filter.or_([
               Filter.select("상태").equals("진행 중"),
               Filter.date("날짜").next_week(),
           ]),
       ]),
   )

   # 전체 결과 자동 페이지네이션
   all_pages = client.databases.query_all("database-id")

주요 필터 조건 목록
~~~~~~~~~~~~~~~~~~~

.. code:: python

   Filter.text("컬럼").equals("값")
   Filter.text("컬럼").contains("값")
   Filter.text("컬럼").starts_with("값")
   Filter.text("컬럼").is_empty()

   Filter.number("컬럼").greater_than(0)
   Filter.number("컬럼").less_than_or_equal_to(100)

   Filter.checkbox("컬럼").equals(True)

   Filter.select("컬럼").equals("옵션")
   Filter.multi_select("컬럼").contains("태그")

   Filter.date("컬럼").before("2025-01-01")
   Filter.date("컬럼").past_week()
   Filter.date("컬럼").next_month()

   Filter.created_time().after("2024-01-01")
   Filter.last_edited_time().past_week()

----

오류 처리
---------

.. code:: python

   from notion_database import (
       NotionClient,
       NotionNotFoundError,
       NotionRateLimitError,
       NotionAPIError,
   )
   import time

   client = NotionClient("secret_xxx")

   try:
       page = client.pages.retrieve("page-id")
   except NotionNotFoundError:
       print("페이지를 찾을 수 없습니다.")
   except NotionRateLimitError:
       time.sleep(1)
       page = client.pages.retrieve("page-id")
   except NotionAPIError as e:
       print(f"오류: [{e.status_code}] {e.code} – {e.message}")

----

기여하기
--------

버그 제보나 기능 제안은 `GitHub Issues <https://github.com/minwook-shin/notion-database/issues>`_ 에 남겨주세요.
코드 기여는 저장소를 포크한 뒤 Pull Request를 보내주시면 환영합니다.

관련 링크
---------

- Notion 공식 API: https://developers.notion.com
- GitHub: https://github.com/minwook-shin/notion-database
- PyPI: https://pypi.org/project/notion-database/

라이선스
--------

LGPLv3
