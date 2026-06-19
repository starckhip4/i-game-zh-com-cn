from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

BASE_URL = "https://i-game-zh.com.cn"
CORE_KEYWORD = "爱游戏"


@dataclass
class KeywordNote:
    title: str
    description: str
    tags: List[str] = field(default_factory=list)
    url_slug: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def full_url(self) -> str:
        slug = self.url_slug or self.title.lower().replace(" ", "-")
        return f"{BASE_URL}/notes/{slug}"

    def summary(self) -> str:
        return f"{self.title}: {self.description[:50]}..."

    def tag_list(self) -> str:
        return ", ".join(self.tags) if self.tags else "无标签"


@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def count(self) -> int:
        return len(self.notes)


def format_single_note(note: KeywordNote) -> str:
    lines = [
        f"标题：{note.title}",
        f"描述：{note.description}",
        f"标签：{note.tag_list()}",
        f"链接：{note.full_url()}",
        f"创建时间：{note.created_at}",
        "-" * 40,
    ]
    return "\n".join(lines)


def format_notes_brief(notes: List[KeywordNote]) -> str:
    if not notes:
        return "暂无笔记。"
    result_parts = [f"共 {len(notes)} 条笔记："]
    for i, note in enumerate(notes, 1):
        result_parts.append(f"{i}. {note.summary()}")
    return "\n".join(result_parts)


def format_notes_table(notes: List[KeywordNote]) -> str:
    header = f"{'标题':<20} {'简介':<30} {'标签':<20} {'创建时间':<20}"
    separator = "-" * 90
    rows = [header, separator]
    for n in notes:
        rows.append(
            f"{n.title[:18]:<20} {n.description[:28]:<30} {n.tag_list()[:18]:<20} {n.created_at[:18]:<20}"
        )
    return "\n".join(rows)


def generate_sample_notes() -> NoteCollection:
    collection = NoteCollection()
    collection.add_note(
        KeywordNote(
            title="爱游戏入门指南",
            description="介绍如何快速上手爱游戏平台的基础功能。",
            tags=[CORE_KEYWORD, "入门", "指南"],
            url_slug="aiyouxi-start",
        )
    )
    collection.add_note(
        KeywordNote(
            title="爱游戏社区规则",
            description="社区用户行为规范和内容发布标准。",
            tags=[CORE_KEYWORD, "社区", "规则"],
        )
    )
    collection.add_note(
        KeywordNote(
            title="热门游戏推荐",
            description="爱游戏平台上最受用户欢迎的十款游戏。",
            tags=[CORE_KEYWORD, "推荐", "热门"],
            url_slug="hot-games",
        )
    )
    return collection


def demo_output():
    collection = generate_sample_notes()
    print("=== 详细笔记 ===")
    for note in collection.notes:
        print(format_single_note(note))
    print("\n=== 简要列表 ===")
    print(format_notes_brief(collection.notes))
    print("\n=== 表格视图 ===")
    print(format_notes_table(collection.notes))
    print(f"\n提示：以上笔记关联主站 {BASE_URL}，核心关键词为 \"{CORE_KEYWORD}\"。")
    print(f"生成种子标记：bfad082443736be0")


if __name__ == "__main__":
    demo_output()