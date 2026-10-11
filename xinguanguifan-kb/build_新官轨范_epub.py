# -*- coding: utf-8 -*-
"""
《新官轨范》txt → 章节目录(Markdown) + 分章 XHTML + EPUB 转换脚本
流程：解析原文 → 按「◆体立为政事情 / 牧民备用 / ○第X章 / √条目」切块
     → 生成目录 md → 生成每章 XHTML → 汇总打包 EPUB
"""
import os, re, uuid, zipfile, html as htmllib

SRC = r"C:\Users\Administrator\Downloads\新官轨范.txt"
OUT_DIR = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat"
CH_DIR = os.path.join(OUT_DIR, "新官轨范_章节")
EPUB_PATH = os.path.join(OUT_DIR, "新官轨范.epub")
TOC_MD_PATH = os.path.join(OUT_DIR, "新官轨范_目录.md")

# ---------- 1. 读取原文（编码探测） ----------
raw = open(SRC, "rb").read()
text = None
for enc in ("utf-8-sig", "utf-8", "gb18030"):
    try:
        text = raw.decode(enc)
        break
    except UnicodeDecodeError:
        continue
if text is None:
    text = raw.decode("gb18030", errors="replace")

# ---------- 2. 分离「来源说明」与「正文」 ----------
lines = text.split("\n")
book_start = next(i for i, ln in enumerate(lines) if "新官轨范" in ln)
meta_lines = [ln.strip() for ln in lines[:book_start] if ln.strip()]
book_text = "\n".join(lines[book_start:]).strip()

# ---------- 3. 解析结构 ----------
PART1_MARK = "◆体立为政事情"
PART2_MARK = "牧民备用"
CH_TITLES = ["上任第一", "直日第二", "御史第三", "民情第四",
             "公务第五", "粮料第六", "礼仪第七", "御灾第八", "词讼第九"]

i1 = book_text.find(PART1_MARK)
i2 = book_text.find(PART2_MARK)
assert 0 <= i1 < i2, "未找到卷上/卷下分界标记"

head = book_text[:i1].strip()                      # 书名+作者行
part1_text = book_text[i1 + len(PART1_MARK):i2].strip()   # 卷上正文
part2_text = book_text[i2 + len(PART2_MARK):].strip()     # 卷下正文

# 卷下章节切分
positions = []
for t in CH_TITLES:
    pos = part2_text.find("○" + t)
    assert pos >= 0, "未找到章节: " + t
    positions.append((pos, t))
positions.sort(key=lambda x: x[0])
part2_opener = part2_text[:positions[0][0]].strip()       # 牧民备用 卷首注语

chapters = []          # (title, items, has_colophon)
for k in range(len(positions)):
    start = positions[k][0]
    end = positions[k + 1][0] if k + 1 < len(positions) else len(part2_text)
    title = positions[k][1]
    seg = part2_text[start:end]
    seg_body = seg[len("○" + title):].strip()
    has_colophon = seg_body.endswith("卷终")
    if has_colophon:
        seg_body = seg_body[: -len("卷终")].rstrip()
    chapters.append((title, seg_body, has_colophon))

def split_items(t):
    """按 √ 切出条目，保留 √ 前缀"""
    parts = t.split("√")
    return [("√" + p).strip() for p in parts if p.strip()]

items_part1 = split_items(part1_text)
items_chapters = [(t, split_items(b), c) for (t, b, c) in chapters]
n1, n2 = len(items_part1), sum(len(it) for _, it, _ in items_chapters)

# 完整性校验：√ 计数应一致
assert book_text.count("√") == n1 + n2, \
    f"√ 计数不符: 原文 {book_text.count('√')} vs 解析 {n1 + n2}"

# 书名作者
book_title = "新官轨范"
m_author = re.search(r"新官轨范\s*（明）不着撰人", head)
author = "（明）不着撰人" if m_author else "不着撰人"

# ---------- 4. 样式与 HTML 生成 ----------
CSS = """body{font-family:"Songti SC","SimSun","Source Han Serif SC","Noto Serif CJK SC",serif;line-height:1.9;color:#1f1f1f;margin:5% 7%;}
h1{font-size:1.5em;text-align:center;margin:1em 0 .4em;}
h2{font-size:1.15em;text-align:center;color:#555;margin:0 0 1.2em;}
p.item{margin:.55em 0;text-align:justify;}
p.note{color:#777;font-style:italic;text-align:center;}
p.colophon{text-align:center;margin-top:2.2em;letter-spacing:.5em;color:#555;}
ul.meta{list-style:none;padding:0;font-size:.95em;}
p.lead{text-indent:2em;}"""

def esc(s):
    return htmllib.escape(s, quote=False)

def chapter_doc(cid, title, body):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<title>{esc(title)}</title>
<style type="text/css">
{CSS}
</style>
</head>
<body>
<section class="chapter" id="{cid}">
{body}
</section>
</body>
</html>"""

def item_paras(items):
    return "\n".join(f'<p class="item">{esc(it)}</p>' for it in items)

# ch00 版本说明
ver_body = f"""<h1>版本说明</h1>
<p class="lead">本书《{esc(book_title)}》{esc(author)}，为明代为官施政类文献整理本，据知乎专栏公开文本录入整理。全书分上下两卷：卷上「体立为政事情」、卷下「牧民备用」（含九章）。</p>
<h2>来源信息</h2>
<ul class="meta">
<li>作者：豆子</li>
<li>链接：<a href="https://zhuanlan.zhihu.com/p/183874152">https://zhuanlan.zhihu.com/p/183874152</a></li>
<li>来源：知乎</li>
<li>著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。</li>
</ul>
<h2>整理说明</h2>
<ul class="meta">
<li>原文以「√」标记条目，本次整理保留该标记；卷下各章以「○第X」为章题。</li>
<li>正文中「□」为原书残损或录入缺字，「£」「×」为原文录入符号，均原样保留。</li>
<li>原文夹注如「（你每=你们）」原样保留。</li>
<li>本次共分卷上 1 卷（{n1} 条）、卷下 9 章（{n2} 条），合计 {n1 + n2} 条。</li>
</ul>"""

# ch01 卷上
ch01_body = f"""<h1>{esc(book_title)}</h1>
<h2>卷上 · 体立为政事情</h2>
{item_paras(items_part1)}"""

# ch02 卷下 卷首
ch02_body = """<h1>卷下 · 牧民备用</h1>
<p class="note">但神字俱去，祭告止用香纸。</p>"""

doc_list = []  # (cid, 显示名, body)
doc_list.append(("ch00", "版本说明", ver_body))
doc_list.append(("ch01", "卷上 · 体立为政事情", ch01_body))
doc_list.append(("ch02", "卷下 · 牧民备用", ch02_body))
for k, (t, its, has_colophon) in enumerate(items_chapters, start=3):
    body = f"<h2>卷下 · 牧民备用</h2>\n<h1>{esc(t)}</h1>\n" + item_paras(its)
    if has_colophon:
        body += '\n<p class="colophon">卷　终</p>'
    doc_list.append((f"ch{k:02d}", t, body))

# 中文章节文件名（交付给用户浏览）
chinese_names = {
    "ch00": "00_版本说明.xhtml",
    "ch01": "01_卷上_体立为政事情.xhtml",
    "ch02": "02_卷下_牧民备用.xhtml",
}
for k, (t, its, _) in enumerate(items_chapters, start=3):
    chinese_names[f"ch{k:02d}"] = f"{k:02d}_卷下_{t}.xhtml"

os.makedirs(CH_DIR, exist_ok=True)
for cid, title, body in doc_list:
    with open(os.path.join(CH_DIR, chinese_names[cid]), "w", encoding="utf-8") as f:
        f.write(chapter_doc(cid, title, body))

# ---------- 5. 目录 Markdown ----------
def trunc(s, n=28):
    s = s.replace("√", "").strip()
    return s if len(s) <= n else s[:n] + "…"

md = []
md.append("# 《新官轨范》章节目录")
md.append("")
md.append(f"- 书名：{book_title}")
md.append(f"- 作者：{author}")
md.append("- 来源：知乎专栏（作者：豆子）https://zhuanlan.zhihu.com/p/183874152")
md.append("- 整理日期：2026-10-09")
md.append(f"- 条目统计：卷上 {n1} 条 ＋ 卷下 {n2} 条 ＝ 合计 {n1 + n2} 条")
md.append("")
md.append("## 卷上 · 体立为政事情（共 %d 条）" % n1)
md.append("")
for i, it in enumerate(items_part1, 1):
    md.append(f"{i}. {trunc(it)}")
md.append("")
md.append(f"## 卷下 · 牧民备用（共 {n2} 条 · 9 章）")
md.append("")
for k, (t, its, _) in enumerate(items_chapters, start=3):
    md.append(f"### {k-2}. {t}（{len(its)} 条）　〔文件：{chinese_names[f'ch{k:02d}']}〕")
    for i, it in enumerate(its, 1):
        md.append(f"{i}. {trunc(it)}")
    md.append("")
with open(TOC_MD_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

# ---------- 6. 汇总 EPUB ----------
book_uuid = "urn:uuid:" + str(uuid.uuid4())
mod_date = "2026-10-09T00:00:00Z"

manifest_items = []
spine_refs = []
for cid, title, body in doc_list:
    fn = f"text/{cid}.xhtml"
    manifest_items.append(
        f'    <item id="{cid}" href="{fn}" media-type="application/xhtml+xml"/>')
    spine_refs.append(f'    <itemref idref="{cid}"/>')

manifest = "\n".join(manifest_items)
spine = "\n".join(spine_refs)

content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="zh-CN">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{book_uuid}</dc:identifier>
    <dc:title>{esc(book_title)}</dc:title>
    <dc:creator>{esc(author)}</dc:creator>
    <dc:language>zh-Hans</dc:language>
    <meta property="dcterms:modified">{mod_date}</meta>
  </metadata>
  <manifest>
{manifest}
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
  </manifest>
  <spine toc="ncx">
{spine}
  </spine>
</package>
"""

nav_entries = []
nav_entries.append(f'<li><a href="text/ch00.xhtml">版本说明</a></li>')
nav_entries.append(f'<li><a href="text/ch01.xhtml">卷上 · 体立为政事情</a></li>')
sub = "\n".join(
    f'        <li><a href="text/ch{k:02d}.xhtml">{esc(t)}</a></li>'
    for k, (t, _, _) in enumerate(items_chapters, start=3))
nav_entries.append(
    '<li><a href="text/ch02.xhtml">卷下 · 牧民备用</a>\n      <ol>\n' + sub + "\n      </ol>\n    </li>")
nav_ol = "\n".join(nav_entries)

nav_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<title>目录</title>
</head>
<body>
<nav epub:type="toc" id="toc">
<h1>目录</h1>
<ol>
{nav_ol}
</ol>
</nav>
</body>
</html>
"""

ncx_points = []
po = 1
ncx_points.append(
    f'    <navPoint id="np-ch00" playOrder="{po}"><navLabel><text>版本说明</text></navLabel><content src="text/ch00.xhtml"/></navPoint>'); po += 1
ncx_points.append(
    f'    <navPoint id="np-ch01" playOrder="{po}"><navLabel><text>卷上 · 体立为政事情</text></navLabel><content src="text/ch01.xhtml"/></navPoint>'); po += 1
for k, (t, _, _) in enumerate(items_chapters, start=3):
    ncx_points.append(
        f'    <navPoint id="np-ch{k:02d}" playOrder="{po}"><navLabel><text>{esc(t)}</text></navLabel><content src="text/ch{k:02d}.xhtml"/></navPoint>'); po += 1
ncx_map = "\n".join(ncx_points)

toc_ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_uuid}"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>{esc(book_title)}</text></docTitle>
  <navMap>
{ncx_map}
  </navMap>
</ncx>
"""

container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

if os.path.exists(EPUB_PATH):
    os.remove(EPUB_PATH)
with zipfile.ZipFile(EPUB_PATH, "w") as z:
    z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
    z.writestr("META-INF/container.xml", container_xml, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/content.opf", content_opf, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/toc.ncx", toc_ncx, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/nav.xhtml", nav_xhtml, compress_type=zipfile.ZIP_DEFLATED)
    for cid, title, body in doc_list:
        z.writestr(f"OEBPS/text/{cid}.xhtml", chapter_doc(cid, title, body),
                   compress_type=zipfile.ZIP_DEFLATED)

print("OK")
print("章节文件目录:", CH_DIR)
print("目录文件:", TOC_MD_PATH)
print("EPUB:", EPUB_PATH)
print(f"卷上 {n1} 条 / 卷下 {n2} 条 / 合计 {n1 + n2} 条")
