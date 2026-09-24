import argparse
from pathlib import Path

from mineru.parser import MinerUParser
from mineru.parser.writer import FileBasedDataWriter


def main():
    ap = argparse.ArgumentParser(description="用本地 MinerU 模型把文档解析成 Markdown + 图片文件夹")
    ap.add_argument("input", help="输入文件路径,如 D:\\国赛\\A题\\A题.pdf")
    ap.add_argument("-o", "--output", help="输出目录,默认在输入文件旁边建同名文件夹")
    ap.add_argument("-p", "--pages", default="", help="PDF 页码范围,如 1-5,8;默认全部")
    ap.add_argument("--tier", default="basic", choices=["flash", "basic"], help="解析档位,默认 basic")
    args = ap.parse_args()

    src = Path(args.input)
    out = Path(args.output) if args.output else src.with_suffix("")
    result = MinerUParser(tier=args.tier).parse(src, page_range=args.pages)
    result.save(FileBasedDataWriter(str(out)))

    md = out / f"{src.stem}.md"
    md.unlink(missing_ok=True)
    (out / "markdown.md").rename(md)
    print(f"完成: {md}")


if __name__ == "__main__":
    main()
