"""
notion-database 2.0 – 통합 예제

환경변수 NOTION_KEY 에 Notion Internal Integration Token 을 설정한 뒤 실행합니다.

    export NOTION_KEY=secret_xxx
    python example.py

또는 프로젝트 루트에 .env 파일을 만들고 실행하면 python-dotenv 가 자동 로드합니다.
"""
import logging
import os
import pprint
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

from notion_database import (
    NotionClient,
    PropertyValue,
    PropertySchema,
    BlockContent,
    RichText,
    Filter,
    Sort,
    Icon,
    Cover,
)
from notion_database.const import (
    BLUE, BLUE_BACKGROUND, BROWN, GREEN, RED, RED_BACKGROUND,
)

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

NOTION_KEY = os.environ["NOTION_KEY"]
client = NotionClient(NOTION_KEY)

# ──────────────────────────────────────────────
# 1. 데이터베이스 검색
# ──────────────────────────────────────────────
log.debug("=== 1. Search databases ===")
search_result = client.search.search_databases(
    sort={"direction": "ascending", "timestamp": "last_edited_time"},
)
databases = search_result["results"]
log.debug("found %d database(s)", len(databases))

if not databases:
    log.warning("접근 가능한 데이터베이스가 없습니다. Integration 이 페이지에 공유되었는지 확인하세요.")
    raise SystemExit(0)

database_id = databases[0]["id"]
log.debug("사용할 데이터베이스: %s", database_id)

# ──────────────────────────────────────────────
# 2. 데이터베이스 조회 및 업데이트
# ──────────────────────────────────────────────
log.debug("=== 2. Retrieve & update database ===")
db = client.databases.retrieve(database_id)
pprint.pprint(db)

client.databases.update(
    database_id,
    title=[RichText.text("📖 Updated DB")],
    icon=Icon.emoji("📚"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
)

# ──────────────────────────────────────────────
# 3. 페이지 생성 (전체 PropertyValue 타입 시연)
# ──────────────────────────────────────────────
log.debug("=== 3. Create page ===")
page = client.pages.create(
    parent={"database_id": database_id},
    properties={
        "title":           PropertyValue.title([
                               RichText.text("Hello, "),
                               RichText.text("Notion 2.0!", bold=True),
                           ]),
        "description":     PropertyValue.rich_text("notion-database 2.0 예제 페이지"),
        "number":          PropertyValue.number(1),
        "number-float":    PropertyValue.number(1.5),
        "select":          PropertyValue.select("test1"),
        "multi_select":    PropertyValue.multi_select(["test1", "test2"]),
        "multi_select2":   PropertyValue.multi_select(["test1", "test2", "test3"]),
        "checkbox":        PropertyValue.checkbox(True),
        "url":             PropertyValue.url("https://www.google.com"),
        "email":           PropertyValue.email("test@test.com"),
        "phone":           PropertyValue.phone_number("010-0000-0000"),
        "date":            PropertyValue.date("2024-01-01T00:00:00.000+0900"),
        "file":            PropertyValue.files([
                               "https://github.githubassets.com/images/modules/logos_page/Octocat.png"
                           ]),
    },
    icon=Icon.emoji("📚"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    children=[
        # 제목
        BlockContent.heading_1("Notion 2.0 예제"),
        BlockContent.paragraph([
            RichText.text("이 페이지는 "),
            RichText.text("notion-database 2.0", bold=True),
            RichText.text(" 으로 생성되었습니다."),
        ]),

        # 구분선 + 목차
        BlockContent.divider(),
        BlockContent.table_of_contents(),
        BlockContent.breadcrumb(),

        # 텍스트 블록
        BlockContent.heading_2("텍스트 블록"),
        BlockContent.paragraph("기본 단락", color=BLUE),
        BlockContent.heading_1("제목 1"),
        BlockContent.heading_2("제목 2", color=BLUE_BACKGROUND),
        BlockContent.heading_3("제목 3", color=GREEN),
        BlockContent.callout("주의 사항", color=RED_BACKGROUND),
        BlockContent.quote("인용구입니다.", color=RED),

        # 목록
        BlockContent.heading_2("목록 블록"),
        BlockContent.bulleted_list_item("불릿 항목 1"),
        BlockContent.bulleted_list_item("불릿 항목 2", color=BROWN),
        BlockContent.bulleted_list_item("중첩 불릿", children=[
            BlockContent.bulleted_list_item("하위 항목"),
        ]),
        BlockContent.numbered_list_item("순서 항목 1"),
        BlockContent.numbered_list_item("순서 항목 2", color=BROWN),
        BlockContent.to_do("완료된 할 일", checked=True),
        BlockContent.to_do("미완료 할 일", checked=False, color=RED),

        # 토글
        BlockContent.toggle("토글 헤더", color=BLUE, children=[
            BlockContent.paragraph("토글 내용이 여기 들어갑니다."),
        ]),

        # 코드
        BlockContent.heading_2("코드 블록"),
        BlockContent.code('print("Hello, Notion!")', language="python"),
        BlockContent.code("const a = 1;", language="javascript"),
        BlockContent.code("SELECT * FROM pages;", language="sql"),

        # 수식
        BlockContent.equation("E = mc^2"),

        # 미디어 / 임베드
        BlockContent.heading_2("미디어 블록"),
        BlockContent.image(
            "https://github.githubassets.com/images/modules/logos_page/Octocat.png",
            caption="GitHub Octocat",
        ),
        BlockContent.video("https://download.blender.org/peach/trailer/trailer_480p.mov"),
        BlockContent.file("https://github.com/microsoft/ML-For-Beginners/raw/main/pdf/readme.pdf"),
        BlockContent.pdf("https://github.com/microsoft/ML-For-Beginners/blob/main/pdf/readme.pdf"),
        BlockContent.embed("https://www.google.com"),
        BlockContent.bookmark("https://www.google.com"),

        # 2단 컬럼
        BlockContent.heading_2("컬럼 레이아웃"),
        BlockContent.column_list([
            [BlockContent.paragraph("왼쪽 컬럼")],
            [BlockContent.paragraph("오른쪽 컬럼")],
        ]),
    ],
)

page_id = page["id"]
log.debug("생성된 페이지 ID: %s", page_id)

# ──────────────────────────────────────────────
# 4. 페이지 조회
# ──────────────────────────────────────────────
log.debug("=== 4. Retrieve page ===")
page = client.pages.retrieve(page_id)
pprint.pprint(page)

# ──────────────────────────────────────────────
# 5. 페이지 업데이트
# ──────────────────────────────────────────────
log.debug("=== 5. Update page ===")
client.pages.update(
    page_id,
    properties={
        "title":       PropertyValue.title("Updated Title"),
        "description": PropertyValue.rich_text("업데이트된 설명"),
        "number":      PropertyValue.number(2),
        "checkbox":    PropertyValue.checkbox(False),
        "date":        PropertyValue.date(
                           "2024-01-01T00:00:00.000+0900",
                           end="2024-01-31T00:00:00.000+0900",
                       ),
        "file":        PropertyValue.files([
                           "https://github.githubassets.com/images/modules/logos_page/Octocat.png",
                           "https://download.blender.org/peach/trailer/trailer_480p.mov",
                       ]),
    },
    icon=Icon.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
)

# ──────────────────────────────────────────────
# 6. 블록 조회 (페이지 콘텐츠)
# ──────────────────────────────────────────────
log.debug("=== 6. Retrieve block children ===")
blocks_response = client.blocks.retrieve_children(page_id, page_size=5)
pprint.pprint(blocks_response)

# 단일 블록 조회
first_block_id = blocks_response["results"][0]["id"]
block = client.blocks.retrieve(first_block_id)
pprint.pprint(block)

# 페이지네이션: 전체 블록 자동 수집
all_blocks = client.blocks.retrieve_all_children(page_id)
log.debug("총 블록 수: %d", len(all_blocks))

# 블록 추가
client.blocks.append_children(page_id, children=[
    BlockContent.paragraph("나중에 추가된 단락입니다."),
])

# ──────────────────────────────────────────────
# 7. 데이터베이스 쿼리 (필터 + 정렬)
# ──────────────────────────────────────────────
log.debug("=== 7. Query database ===")

# 단순 필터
result = client.databases.query(
    database_id,
    filter=Filter.checkbox("checkbox").equals(False),
    sorts=[Sort.by_property("title")],
)
pprint.pprint(result)

# 복합 필터 (OR)
result = client.databases.query(
    database_id,
    filter=Filter.or_([
        Filter.checkbox("checkbox").equals(False),
        Filter.number("number").greater_than_or_equal_to(2),
    ]),
)
pprint.pprint(result)

# 복합 필터 (AND + OR 중첩)
result = client.databases.query(
    database_id,
    filter=Filter.and_([
        Filter.text("title").is_not_empty(),
        Filter.or_([
            Filter.select("select").equals("test1"),
            Filter.number("number").less_than(10),
        ]),
    ]),
    sorts=[
        Sort.descending("number"),
        Sort.by_timestamp("last_edited_time", "descending"),
    ],
)
pprint.pprint(result)

# 자동 페이지네이션으로 전체 결과 수집
all_pages = client.databases.query_all(database_id)
log.debug("전체 페이지 수: %d", len(all_pages))

# ──────────────────────────────────────────────
# 8. 페이지 아카이브 / 복원
# ──────────────────────────────────────────────
log.debug("=== 8. Archive & restore page ===")
time.sleep(1)
client.pages.archive(page_id)
log.debug("페이지 아카이브 완료")

time.sleep(1)
client.pages.archive(page_id, archived=False)
log.debug("페이지 복원 완료")

# ──────────────────────────────────────────────
# 9. 하위 데이터베이스 생성
# ──────────────────────────────────────────────
log.debug("=== 9. Create child database ===")
child_db = client.databases.create(
    parent={"type": "page_id", "page_id": page_id},
    title=[RichText.text("하위 데이터베이스")],
    properties={
        "child_name":         PropertySchema.title(),
        "child_description":  PropertySchema.rich_text(),
        "child_number":       PropertySchema.number(),
        "child_select":       PropertySchema.select([
                                  {"name": "옵션A", "color": "green"},
                                  {"name": "옵션B", "color": "red"},
                              ]),
        "child_multi_select": PropertySchema.multi_select(),
        "child_checkbox":     PropertySchema.checkbox(),
        "child_url":          PropertySchema.url(),
        "child_email":        PropertySchema.email(),
        "child_phone":        PropertySchema.phone_number(),
        "child_date":         PropertySchema.date(),
    },
    icon=Icon.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
    cover=Cover.external("https://github.githubassets.com/images/modules/logos_page/Octocat.png"),
)
log.debug("하위 데이터베이스 ID: %s", child_db["id"])

# ──────────────────────────────────────────────
# 10. 사용자 조회
# ──────────────────────────────────────────────
log.debug("=== 10. Users ===")
me = client.users.me()
log.debug("현재 봇: %s", me.get("name"))

all_users = client.users.list_all()
log.debug("워크스페이스 사용자 수: %d", len(all_users))

log.debug("=== 완료 ===")
