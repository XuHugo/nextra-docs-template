#!/usr/bin/env python3
"""Import the Gas Optimization Master manuscript into the Nextra blog.

The Markdown export is the text source of truth. The DOCX is used for image
assets because its images are embedded, while the Markdown points at expiring
Feishu URLs. The importer intentionally generates plain Markdown pages: the
manuscript contains many Solidity/Yul braces that do not need MDX semantics.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


GITHUB_REPO = "https://github.com/XuHugo/gas_optimization_master"


@dataclass
class Article:
    source_title: str
    lines: list[str] = field(default_factory=list)
    title: str = ""
    slug: str = ""


@dataclass
class Section:
    source_title: str
    intro: list[str] = field(default_factory=list)
    articles: list[Article] = field(default_factory=list)
    key: str = ""
    title: str = ""
    description: str = ""
    slugs: list[str] = field(default_factory=list)


SECTION_CONFIG = [
    {
        "key": "basics",
        "title": "基础知识",
        "description": "理解 Gas 费用、EVM 数据区、Yul 与 Foundry 测试方法。",
        "slugs": [
            "01-gas-fee",
            "02-opcode-gas-costs",
            "03-storage-and-transient-storage",
            "04-evm-memory",
            "05-calldata",
            "06-yul",
            "07-foundry",
        ],
    },
    {
        "key": "storage",
        "title": "存储优化",
        "description": "围绕 Storage、Memory、Calldata 和瞬态存储降低读写成本。",
        "slugs": [
            "01-reduce-nonzero-bytes",
            "02-avoid-zero-to-one-storage",
            "03-cache-storage-data",
            "04-variable-packing",
            "05-short-strings",
            "06-constants-and-immutables",
            "07-mapping-over-array",
            "08-bitmaps",
            "09-sstore2-and-sstore3",
            "10-storage-pointer",
            "11-calldata-over-memory",
            "12-remove-redundant-operations",
            "13-data-type-selection",
            "14-transient-storage",
            "15-gas-refunds",
            "16-events",
        ],
    },
    {
        "key": "contract",
        "title": "合约优化",
        "description": "从部署、调用、错误处理和架构选择优化合约成本。",
        "slugs": [
            "01-payable",
            "02-predict-contract-addresses",
            "03-contract-metadata",
            "04-selfdestruct-temporary-contracts",
            "05-internal-functions-and-modifiers",
            "06-modifier-view-functions",
            "07-clones",
            "08-monolithic-architecture",
            "09-gas-optimized-libraries",
            "10-fallback-and-receive",
            "11-eip2930-access-lists",
            "12-custom-errors",
            "13-existing-create2-factory",
            "14-safemath",
            "15-external-vs-public",
            "16-inheritance",
            "17-token-transfer-hooks",
            "18-inline-single-use-functions",
        ],
    },
    {
        "key": "assembly",
        "title": "汇编优化",
        "description": "使用内联汇编控制内存、调用、哈希和常见数学操作。",
        "slugs": [
            "01-memory-expansion",
            "02-error-messages",
            "03-contract-calls",
            "04-multiple-contract-creation",
            "05-multiple-external-calls",
            "06-events",
            "07-hashing",
            "08-address-zero-check",
            "09-min-max",
            "10-even-odd",
            "11-selfbalance",
        ],
    },
    {
        "key": "compiler",
        "title": "编译器优化",
        "description": "比较条件、循环、运算符、可见性和编译器配置的 Gas 差异。",
        "slugs": [
            "01-gte-vs-gt",
            "02-not-vs-eq",
            "03-nonzero-comparison",
            "04-short-circuit-booleans",
            "05-split-boolean-expressions",
            "06-unchecked",
            "07-do-while-vs-for",
            "08-loop-unrolling",
            "09-function-name-selector",
            "10-hash-array-string-comparison",
            "11-prefix-increment",
            "12-bit-shifts",
            "13-cube-vs-exponentiation",
            "14-private-internal-visibility",
            "15-compound-assignment",
            "16-enums-over-strings",
            "17-compiler-optimizer",
            "18-lookup-tables",
            "19-precompiles",
            "20-named-returns",
        ],
    },
    {
        "key": "patterns",
        "title": "场景与设计模式",
        "description": "把批量调用、签名、代理和代币标准用于真实业务场景。",
        "slugs": [
            "01-multidelegatecall",
            "02-ecdsa-whitelist-airdrop",
            "03-uups",
            "04-erc20-permit",
            "05-erc1155-vs-erc721",
            "06-erc1155-erc6909-vs-erc20",
            "07-vote-delegation",
        ],
    },
    {
        "key": "unconventional",
        "title": "非常规技巧",
        "description": "实验性较强的优化方法，以及它们的适用边界和风险。",
        "slugs": [
            "01-gasprice-msgvalue-data",
            "02-gasleft-branching",
            "03-payable-functions",
            "04-external-library-jumps",
            "05-append-bytecode",
        ],
    },
]


TITLE_OVERRIDES = {
    "GasFee计算方法": "Gas Fee 计算方法",
    "Gas 常量：操作成本": "Gas 常量：EVM 操作成本",
    "Storage&Transient": "Storage 与 Transient Storage",
    "Yul介绍": "Yul 介绍",
    "Foundry介绍": "Foundry 介绍",
    "避免存储零到一": "避免存储值从零变为非零",
    "不会改变的变量": "使用 constant 和 immutable",
    "使用mapping避免长度检查": "使用 mapping 避免数组长度检查",
    "使用位图替换大量bool": "使用位图替换大量 bool",
    "使用sstore2或sstore3存储大量数据": "使用 SSTORE2 或 SSTORE3 存储大量数据",
    "Calldata 替换 Memory": "使用 Calldata 替换 Memory",
    "❓冗余操作": "待验证：冗余操作",
    "通过使单体架构": "使用单体架构",
    "选择gas优化的库": "选择 Gas 优化库",
    "尽量使用自定义错误": "使用自定义错误",
    "不再需要SafeMath": "Solidity 0.8+ 不再需要 SafeMath",
    "external VS public": "external 与 public",
    "❓修改器中使用内部视图函数": "待验证：修改器中使用内部视图函数",
    "❓selfbalance VS address(this).balance": "待验证：selfbalance 与 address(this).balance",
    "条件优化：！替换 ==": "条件优化：使用 ! 代替 == 判断",
    "条件优化：❓无符号整数，!=0替换>0": "待验证：无符号整数使用 != 0 代替 > 0",
    "++i替换i++": "使用 ++i 替换 i++",
    "（>>、<<) 替换 （/、*）": "使用位移替换乘除运算",
    "n * n * n替换n ** 3": "使用 n * n * n 替换 n ** 3",
    "变量尽量设置private\\internal": "合理使用 private 和 internal",
    "x=x+y替换x+=y": "x = x + y 与 x += y",
    "编译器": "编译器优化器设置",
    "使用 multidelegatecall 批量处理事务": "使用 Multidelegatecall 批量处理交易",
    "使用 ECDSA 签名进行白名单和空投": "使用 ECDSA 签名实现白名单和空投",
    "UUPS 升级模式更节省gas": "使用 UUPS 降低代理部署成本",
    "使用 ERC20Permit 批量执行交易的批准和转账": "使用 ERC20 Permit 合并授权与转账",
    "ERC1155 是一种比 ERC721 更便宜的非同质化代币": "ERC1155 与 ERC721 的 Gas 对比",
    "使用ERC1155 或 ERC6909 代币代替多个 ERC20 代币": "使用 ERC1155 或 ERC6909 管理多种代币",
    "让所有函数都Payable": "将函数设为 Payable",
}


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\((https?://[^)]+)\)")
SOURCE_PATH_RE = re.compile(r"(?<![\w/])((?:src|test|script)/[A-Za-z0-9_./-]+\.s\.sol|(?:src|test|script)/[A-Za-z0-9_./-]+\.t\.sol|(?:src|test|script)/[A-Za-z0-9_./-]+\.sol)")

PATH_CORRECTIONS = {
    "script/create2.sol": "script/Create2.s.sol",
    "src/assembly/Mathopt.sol": "src/assembly/MathOpt.sol",
    "test/assembly/Mathopt.t.sol": "test/assembly/MathOpt.t.sol",
    "src/compiler/Spilt.sol": "src/compiler/Split.sol",
    "test/compiler/Spilt.t.sol": "test/compiler/Split.t.sol",
    "src/compiler/Unroll.sol": "src/compiler/UnRoll.sol",
    "test/compiler/Unroll.t.sol": "test/compiler/UnRoll.t.sol",
    "src/compiler/precompiles.sol": "src/compiler/Precompiles.sol",
    "test/compiler/precompiles.t.sol": "test/compiler/Precompiles.t.sol",
    "src/contract/Accesslist.sol": "src/contract/AccessList.sol",
    "test/contract/Accesslist.t.sol": "test/contract/AccessList.t.sol",
    "test/compiler/NameReturn.t.sol": "test/compiler/NameReturn.sol",
}


def plain_heading(text: str) -> str:
    text = text.strip().replace("**", "").replace("`", "")
    text = re.sub(r"\\([\\`*{}\[\]()#+.!_><=&+\-])", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def display_title(source_title: str) -> str:
    cleaned = plain_heading(source_title)
    return TITLE_OVERRIDES.get(cleaned, cleaned)


def parse_manuscript(markdown: Path) -> list[Section]:
    sections: list[Section] = []
    current_section: Section | None = None
    current_article: Article | None = None
    in_fence = False

    for raw_line in markdown.read_text(encoding="utf-8-sig").splitlines():
        if re.match(r"^\s*(```|~~~)", raw_line):
            in_fence = not in_fence
            if current_article:
                current_article.lines.append(raw_line)
            elif current_section:
                current_section.intro.append(raw_line)
            continue

        match = HEADING_RE.match(raw_line) if not in_fence else None
        if match and len(match.group(1)) == 2:
            current_section = Section(source_title=plain_heading(match.group(2)))
            sections.append(current_section)
            current_article = None
            continue

        if match and len(match.group(1)) == 3:
            title = plain_heading(match.group(2))
            if not title:
                current_article = None
                continue
            if current_section is None:
                raise ValueError(f"Article found before section: {raw_line}")
            current_article = Article(source_title=title)
            current_section.articles.append(current_article)
            continue

        if current_article:
            current_article.lines.append(raw_line)
        elif current_section:
            current_section.intro.append(raw_line)

    if in_fence:
        raise ValueError("The source Markdown has an unclosed code fence")
    return sections


def apply_config(sections: list[Section]) -> None:
    if len(sections) != len(SECTION_CONFIG):
        raise ValueError(f"Expected {len(SECTION_CONFIG)} sections, found {len(sections)}")
    for section, config in zip(sections, SECTION_CONFIG, strict=True):
        section.key = config["key"]
        section.title = config["title"]
        section.description = config["description"]
        section.slugs = config["slugs"]
        if len(section.articles) != len(section.slugs):
            raise ValueError(
                f"{section.source_title}: expected {len(section.slugs)} articles, "
                f"found {len(section.articles)}"
            )
        for article, slug in zip(section.articles, section.slugs, strict=True):
            article.title = display_title(article.source_title)
            article.slug = slug


def docx_image_targets(docx: Path) -> list[str]:
    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    with ZipFile(docx) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        relationships = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        rels = {
            node.attrib["Id"]: node.attrib["Target"]
            for node in relationships.findall(f"{{{rel_ns}}}Relationship")
        }
    targets: list[str] = []
    embed_key = f"{{{ns['r']}}}embed"
    for blip in document.iter(f"{{{ns['a']}}}blip"):
        relationship_id = blip.attrib.get(embed_key)
        if relationship_id and relationship_id in rels:
            targets.append(rels[relationship_id])
    return targets


def demote_article_headings(lines: list[str]) -> list[str]:
    result: list[str] = []
    in_fence = False
    for line in lines:
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            result.append(line)
            continue
        match = HEADING_RE.match(line) if not in_fence else None
        if match and len(match.group(1)) >= 4:
            level = max(2, len(match.group(1)) - 2)
            result.append(f"{'#' * level} {plain_heading(match.group(2))}")
        else:
            result.append(line)
    return result


def trim_blank_lines(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def source_links(body: str, solidity_repo: Path, commit: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    seen: set[str] = set()
    for match in SOURCE_PATH_RE.finditer(body):
        relative = match.group(1).replace("\\", "/")
        if relative in seen or not (solidity_repo / relative).is_file():
            continue
        seen.add(relative)
        found.append((relative, f"{GITHUB_REPO}/blob/{commit}/{relative}"))
    return found


def correct_source_paths(body: str) -> str:
    for incorrect, correct in PATH_CORRECTIONS.items():
        body = body.replace(incorrect, correct)
    return body


def js_meta(entries: list[tuple[str, str]]) -> str:
    rows = ["export default {"]
    for index, (key, title) in enumerate(entries):
        comma = "," if index < len(entries) - 1 else ""
        rows.append(f"  {json.dumps(key, ensure_ascii=False)}: {json.dumps(title, ensure_ascii=False)}{comma}")
    rows.append("}")
    return "\n".join(rows) + "\n"


def write_site(
    sections: list[Section],
    docx: Path,
    site: Path,
    solidity_repo: Path,
    commit: str,
) -> dict[str, object]:
    pages_root = site / "pages" / "gas-optimization-master"
    images_root = site / "public" / "images" / "gas-optimization-master"
    if pages_root.exists():
        shutil.rmtree(pages_root)
    if images_root.exists():
        shutil.rmtree(images_root)
    pages_root.mkdir(parents=True)
    images_root.mkdir(parents=True)

    image_targets = docx_image_targets(docx)
    expected_images = sum(
        len(IMAGE_RE.findall("\n".join(article.lines)))
        for section in sections
        for article in section.articles
    )
    if len(image_targets) != expected_images:
        raise ValueError(
            f"Image mismatch: DOCX body has {len(image_targets)}, "
            f"Markdown has {expected_images}"
        )

    section_meta = [("index", "专栏导读")]
    section_meta.extend((section.key, section.title) for section in sections)
    (pages_root / "_meta.js").write_text(js_meta(section_meta), encoding="utf-8")

    index_lines = [
        "# Gas 优化大师课",
        "",
        "这套专栏系统整理 Solidity 与 EVM Gas 优化方法，从费用模型和底层数据区出发，",
        "逐步进入存储、合约架构、内联汇编、编译器技巧和真实业务场景。",
        "",
        f"配套代码仓库：[XuHugo/gas_optimization_master]({GITHUB_REPO})。",
        f"本文内容对应代码版本：[`{commit}`]({GITHUB_REPO}/tree/{commit})。",
        "",
        "> Gas 优化不是越低越好。可读性、安全性、可维护性和协议版本差异，",
        "> 都应当与节省的 Gas 一起评估。带有“待验证”标记的内容保留了原稿中的疑问性质。",
        "",
        "## 学习路线",
        "",
    ]
    for number, section in enumerate(sections, 1):
        index_lines.extend(
            [
                f"### {number}. [{section.title}](./{section.key}/)",
                "",
                section.description,
                "",
                f"共 {len(section.articles)} 篇。",
                "",
            ]
        )
    index_lines.extend(
        [
            "## 如何复现实验",
            "",
            "```bash",
            "git clone https://github.com/XuHugo/gas_optimization_master.git",
            "cd gas_optimization_master",
            f"git checkout {commit}",
            "git submodule update --init --recursive",
            "forge build",
            "forge test --gas-report",
            "```",
            "",
        ]
    )
    (pages_root / "index.md").write_text("\n".join(index_lines), encoding="utf-8")

    article_count = 0
    image_index = 0
    unresolved_paths: list[str] = []
    with ZipFile(docx) as archive:
        for section in sections:
            section_dir = pages_root / section.key
            section_image_dir = images_root / section.key
            section_dir.mkdir()
            section_image_dir.mkdir()

            article_meta = [("index", "模块导读")]
            article_meta.extend((article.slug, article.title) for article in section.articles)
            (section_dir / "_meta.js").write_text(js_meta(article_meta), encoding="utf-8")

            module_lines = [f"# {section.title}", "", section.description, ""]
            intro = trim_blank_lines(demote_article_headings(section.intro))
            if intro:
                module_lines.extend(intro + [""])
            module_lines.extend(["## 文章目录", ""])
            for idx, article in enumerate(section.articles, 1):
                module_lines.append(f"{idx}. [{article.title}](./{article.slug})")
            module_lines.append("")
            (section_dir / "index.md").write_text("\n".join(module_lines), encoding="utf-8")

            for article in section.articles:
                body_lines = trim_blank_lines(demote_article_headings(article.lines))
                body = "\n".join(body_lines)
                body = correct_source_paths(body)
                local_image_number = 0

                def replace_image(_: re.Match[str]) -> str:
                    nonlocal image_index, local_image_number
                    target = image_targets[image_index]
                    local_image_number += 1
                    suffix = Path(target).suffix.lower() or ".png"
                    filename = f"{article.slug}-{local_image_number:02d}{suffix}"
                    destination = section_image_dir / filename
                    destination.write_bytes(archive.read(f"word/{target}"))
                    image_index += 1
                    alt = f"{article.title}图示"
                    if local_image_number > 1:
                        alt += f" {local_image_number}"
                    return f"![{alt}](/images/gas-optimization-master/{section.key}/{filename})"

                body = IMAGE_RE.sub(replace_image, body)
                links = source_links(body, solidity_repo, commit)
                for raw_path in SOURCE_PATH_RE.findall(body):
                    normalized = raw_path.replace("\\", "/")
                    if not (solidity_repo / normalized).is_file():
                        unresolved_paths.append(normalized)

                article_lines = [f"# {article.title}", "", body.rstrip(), ""]
                article_lines.extend(["## 对应源码", ""])
                if links:
                    article_lines.extend(f"- [`{path}`]({url})" for path, url in links)
                else:
                    article_lines.append(
                        f"- [Gas Optimization Master 配套代码]({GITHUB_REPO}/tree/{commit})"
                    )
                article_lines.extend(
                    [
                        "",
                        f"> 本文配套代码固定到提交 `{commit}`；Gas 数据会随编译器、优化器参数和 EVM 版本变化。",
                        "",
                    ]
                )
                (section_dir / f"{article.slug}.md").write_text(
                    "\n".join(article_lines), encoding="utf-8"
                )
                article_count += 1

    return {
        "sections": len(sections),
        "articles": article_count,
        "images": image_index,
        "unresolved_source_paths": sorted(set(unresolved_paths)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--docx", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--solidity-repo", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()

    sections = parse_manuscript(args.markdown)
    apply_config(sections)
    report = write_site(sections, args.docx, args.site, args.solidity_repo, args.commit)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
