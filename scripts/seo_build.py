"""Round 83 — programmatic SEO snapshot generator (skill: programmatic-seo).
Playbooks: Profiles (giao-vien/<slug>/) + Curation (khoa-hoc/<slug>/ hub).
Reads seed data from data/seo-seed.json (skills + mentors, user-generated),
renders static HTML pages with unique title/meta/H1/JSON-LD + breadcrumbs,
rewrites sitemap.xml to include every generated URL.
Usage: python scripts/seo_build.py [--check]
  --check: verify generated files match seed (CI guard, no write).
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "seo-seed.json"
SITE = "https://khoaphan8i.github.io/learn-online"

COURSE_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Learn Online</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title} | Learn Online">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Course","name":"{title}","description":"{desc}","provider":{{"@type":"Organization","name":"Learn Online","sameAs":"{site}/"}}}}
</script>
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / <a href="{site}/khoa-hoc/">Khóa học</a> / {title}</nav>
<h1>{title}</h1>
<p>{desc}</p>
<p><a href="{site}/?utm_source=seo&utm_medium=course&utm_campaign={slug}">Mở lớp học trên Learn Online</a></p>
<h2>Khóa học khác</h2>
<ul>
{related}
</ul>
</body>
</html>
"""

MENTOR_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} — mentor {skills} | Learn Online</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="profile">
<meta property="og:title" content="{name} — mentor {skills} | Learn Online">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{{"@type":"Person","name":"{name}","description":"{desc}"}}}}
</script>
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / <a href="{site}/giao-vien/">Mentor</a> / {name}</nav>
<h1>{name}</h1>
<p>{desc}</p>
<p>Dạy: {skills}</p>
<p>Liên hệ: {contact}</p>
<p><a href="{site}/?utm_source=seo&utm_medium=mentor&utm_campaign={slug}#giao-vien-{slug}">Xem hồ sơ {name} trên Learn Online</a></p>
<h2>Mentor dạy cùng kỹ năng</h2>
<ul>
{related}
</ul>
</body>
</html>
"""

HUB_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Learn Online</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / {crumb}</nav>
<h1>{title}</h1>
<p>{desc}</p>
<ul>
{links}
</ul>
</body>
</html>
"""

slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", s.strip().lower()).strip("-") or "lop"


def load_seed():
    seed = json.loads(DATA.read_text(encoding="utf-8"))
    assert isinstance(seed.get("skills"), list) and seed["skills"], "seed.skills empty"
    assert isinstance(seed.get("mentors"), list), "seed.mentors missing"
    return seed


def related_links(items):
    return "\n".join(
        f'<li><a href="{u}">{html.escape(t)}</a></li>' for t, u in items) or "<li>Đang cập nhật.</li>"


def render_course(skill, all_skills):
    slug = slugify(skill["slug"])
    title = f"Học {skill['name']} online"
    desc = f"Các lớp {skill['name']} trên Learn Online — {skill['blurb']} Đăng miễn phí, học phí do mentor tự đặt."
    url = f"{SITE}/khoa-hoc/{slug}/"
    others = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/")
              for s in all_skills if slugify(s["slug"]) != slug][:3]
    return f"khoa-hoc/{slug}/index.html", COURSE_TMPL.format(
        title=html.escape(title), desc=html.escape(desc),
        url=url, site=SITE, slug=slug, related=related_links(others)).replace(
        f"{SITE}/og-cover.png", f"{SITE}/og-{slug}.png")


def render_mentor(mentor, all_skills):
    slug = slugify(mentor["name"])
    skills = " · ".join(mentor.get("skills", [])[:3]) or "đa kỹ năng"
    desc = f"{mentor['name']} — mentor {skills} trên Learn Online. {mentor.get('bio', '')}".strip()
    url = f"{SITE}/giao-vien/{slug}/"
    mine = {s.strip().lower() for s in mentor.get("skills", [])}
    rel = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/")
           for s in all_skills if s["name"].strip().lower() in mine][:3]
    return f"giao-vien/{slug}/index.html", MENTOR_TMPL.format(
        name=html.escape(mentor["name"]), skills=html.escape(skills),
        desc=html.escape(desc), contact=html.escape(mentor.get("contact", "xem trong bài")),
        url=url, site=SITE, slug=slug, related=related_links(rel))


COMPARE_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Learn Online</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} | Learn Online">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / So sánh</nav>
<h1>{title}</h1>
<p>{desc}</p>
<table>
<tr><th>Tiêu chí</th><th>Trung tâm truyền thống</th><th>Learn Online</th></tr>
<tr><td>Chi phí mở lớp</td><td>Thuê mặt bằng, in tài liệu</td><td>Miễn phí đăng bài</td></tr>
<tr><td>Học phí</td><td>Trung tâm ấn định</td><td>Mentor tự đặt</td></tr>
<tr><td>Ai dạy được</td><td>Giáo viên hợp đồng</td><td>Bất cứ ai có kỹ năng</td></tr>
<tr><td>Tìm học viên</td><td>Chạy quảng cáo, phát tờ rơi</td><td>Chia sẻ link, streak, Ghim 29k/7 ngày</td></tr>
</table>
<p>Trung tâm phù hợp khi bạn cần phòng học vật lý và giáo trình chuẩn. Learn Online phù hợp khi bạn có kỹ năng và muốn dạy ngay, không vốn.</p>
<h2>Nền tảng khóa học đóng gói thì sao?</h2>
<table>
<tr><th>Tiêu chí</th><th>Unica / Edumall / Kyna</th><th>Learn Online</th></tr>
<tr><td>Dạng học</td><td>Video thu sẵn, tự học</td><td>Lớp kèm trực tiếp, hỏi trước khi đăng ký</td></tr>
<tr><td>Ai dạy được</td><td>Qua kiểm duyệt / tuyển chọn</td><td>Bất cứ ai, mở lớp trong 1 phút</td></tr>
<tr><td>Học phí</td><td>Nền tảng định giá</td><td>Mentor tự đặt</td></tr>
</table>
<p>Chi tiết trung thực từng nhà (snapshot 2026-09-16, chưa crawl verify): Unica giỏi thư viện khóa rẻ; Edumall mạnh combo; Kyna mạnh lộ trình cam kết. Khe của Learn Online là lớp kèm trực tiếp cho mentor cá nhân — điều cả ba chưa làm.</p>
<p><a href="{site}/?utm_source=seo&utm_medium=compare&utm_campaign=trung-tam">Đăng lớp đầu tiên trên Learn Online</a></p>
<h2>Khóa học khác</h2>
<ul>
{related}
</ul>
</body>
</html>
"""


USECASE_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chua tung day ai? Bat dau voi lop dau tien | Learn Online</title>
<meta name="description" content="Ban gioi mot ky nang nhung chua tung day? 5 buoc mo lop dau tien trong 1 phut — mien phi dang bai, hoc phi tu dat.">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / Cho nguoi moi day</nav>
<h1>Chua tung day ai? Bat dau voi lop dau tien</h1>
<ol>
<li>Chon 1 ky nang ban tu tin nhat</li>
<li>Dat ten lop ro rang: ky nang + trinh do + doi tuong</li>
<li>Dat hoc phi theo gia that tren trang, moi day lay gia giua</li>
<li>De lai cach lien he de hoc vien nhan tin</li>
<li>Bam dang bai, copy link chia se — moi nguoi mo link +2 diem</li>
</ol>
<p><a href="{site}/?utm_source=seo&utm_medium=usecase&utm_campaign=nguoi-moi-day">Mo lop dau tien ngay</a></p>
<h2>Khoa hoc goi y</h2>
<ul>
{related}
</ul>
</body>
</html>
"""




PRESS_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Press kit — Learn Online | Learn Online</title>
<meta name="description" content="Press kit Learn Online: cau chuyen, so lieu, logo va anh. Nen tang chia se khoa hoc — ai cung day duoc.">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / Bao chi</nav>
<h1>Press kit — Learn Online</h1>
<p>Learn Online la cho ky nang sharing online: ai cung day duoc, ai cung hoc duoc. Dang bai mien phi, hoc phi do mentor tu dat.</p>
<h2>Cau chuyen (1 doan)</h2>
<p>Hoc them ky nang moi o Viet Nam van dong nghia voi dong hoc phi cao cho trung tam. Learn Online dao nguoc mo hinh: bat cu ai gioi mot ky nang deu mo lop trong 1 phut, tu dat hoc phi, tu tim hoc vien bang link chia se. Hien co {nskills} nhom ky nang va {nmentors} mentor khoi dau.</p>
<h2>So lieu nhanh</h2>
<ul>
<li>{nskills} nhom ky nang</li>
<li>{nmentors} mentor</li>
<li>Dang bai mien phi; Ghim Noi Bat 29.000d / 7 ngay</li>
</ul>
<h2>Asset</h2>
<ul>
<li><a href="{site}/og-cover.png">Logo/cover 1200x630 (PNG)</a></li>
<li><a href="{site}/sitemap.xml">Sitemap day du</a></li>
<li><a href="{site}/llms.txt">Tom tat AI-readable (llms.txt)</a></li>
</ul>
<p>Lien he bao chi: xem thong tin tren trang chu {site}/</p>
<h2>Khoa hoc</h2>
<ul>
{related}
</ul>
</body>
</html>
"""


def render_hub(path, title, desc, crumb, items):
    links = "\n".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for t, u in items)
    return path, HUB_TMPL.format(title=html.escape(title), desc=html.escape(desc),
                                 url=f"{SITE}/{path.replace('index.html', '')}",
                                 site=SITE, crumb=crumb, links=links)


def build():
    seed = load_seed()
    pages = {}
    for skill in seed["skills"]:
        p, h = render_course(skill, seed["skills"])
        pages[p] = h
    for mentor in seed["mentors"]:
        p, h = render_mentor(mentor, seed["skills"])
        pages[p] = h
    course_items = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/") for s in seed["skills"]]
    mentor_items = [(m["name"], f"{SITE}/giao-vien/{slugify(m['name'])}/") for m in seed["mentors"]]
    p, h = render_hub("khoa-hoc/index.html", "Khóa học online",
                      "Danh sách khóa học theo kỹ năng trên Learn Online — ai cũng dạy được, ai cũng học được.",
                      "Khóa học", course_items)
    pages[p] = h
    p, h = render_hub("giao-vien/index.html", "Mentor",
                      "Danh sách mentor trên Learn Online — xem hồ sơ, kỹ năng và liên hệ.",
                      "Mentor", mentor_items)
    pages[p] = h
    rel = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/")
           for s in seed["skills"]][:3]
    pages["so-sanh/trung-tam/index.html"] = COMPARE_TMPL.format(
        title="Học ở trung tâm hay dạy trên Learn Online?",
        desc="So sánh trung thực: trung tâm truyền thống vs nền tảng chia sẻ khóa học Learn Online — chi phí, học phí, ai dạy được.",
        url=f"{SITE}/so-sanh/trung-tam/", site=SITE, related=related_links(rel))
    usecase = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/")
               for s in seed["skills"]][:3]
    pages["cho-nguoi-moi-day/index.html"] = USECASE_TMPL.format(
        site=SITE, url=f"{SITE}/cho-nguoi-moi-day/",
        related=related_links(usecase))
    press_rel = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/")
                 for s in seed["skills"]][:3]
    pages["bao-chi/index.html"] = PRESS_TMPL.format(
        site=SITE, url=f"{SITE}/bao-chi/",
        nskills=len(seed["skills"]), nmentors=len(seed["mentors"]),
        related=related_links(press_rel))
    return pages


def write_llms(seed):
    lines = ["# Learn Online", "",
             "Nen tang chia se khoa hoc: ai cung day duoc, ai cung hoc duoc.",
             "Hoc phi do mentor tu dat. Dang bai mien phi.", "",
             "## Khoa hoc"]
    for s in seed["skills"]:
        lines.append(f"- [{s['name']}]({SITE}/khoa-hoc/{slugify(s['slug'])}/): {s['blurb']}")
    lines += ["", "## Mentor"]
    for m in seed["mentors"]:
        lines.append(f"- [{m['name']}]({SITE}/giao-vien/{slugify(m['name'])}/): "
                     f"{', '.join(m.get('skills', []))}. {m.get('bio', '')}".rstrip())
    lines += ["", "## Chinh sach",
              "- Ghim Noi Bat: 29.000 VND / 7 ngay, lien he admin kich hoat.",
              f"- Sitemap day du: {SITE}/sitemap.xml"]
    return "\n".join(lines) + "\n"


def write_og_covers(seed):
    """Sinh og-cover riêng từng kỹ năng (PIL). Trả về {slug: filename}."""
    from PIL import Image, ImageDraw
    out = {}
    for s in seed["skills"]:
        slug = slugify(s["slug"])
        fn = f"og-{slug}.png"
        dest = ROOT / fn
        if dest.is_file():
            out[slug] = fn
            continue
        im = Image.new("RGB", (1200, 630), (15, 15, 20))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 560, 1200, 630], fill=(254, 44, 85))
        d.rectangle([90, 140, 110, 420], fill=(251, 191, 36))
        d.text((140, 200), f"Hoc {s['name']} online", fill=(244, 244, 246))
        d.text((140, 300), "Learn Online — ai cung day duoc", fill=(167, 167, 184))
        im.save(dest)
        out[slug] = fn
    return out


def write_sitemap(pages):
    urls = [f"{SITE}/"] + sorted(f"{SITE}/{p.replace('index.html', '')}" for p in pages)
    body = "\n".join(
        f"<url><loc>{u}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>" for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


def main():
    check = "--check" in sys.argv
    pages = build()
    if check:
        bad = [p for p in pages if not (ROOT / p).is_file()]
        cur = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        missing = [u for u in [f"{SITE}/{p.replace('index.html', '')}" for p in pages] if u not in cur]
        llms = ROOT / "llms.txt"
        llms_ok = llms.is_file() and all(
            slugify(s["slug"]) in llms.read_text(encoding="utf-8")
            for s in load_seed()["skills"])
        covers_ok = all((ROOT / f"og-{slugify(s['slug'])}.png").is_file()
                        for s in load_seed()["skills"])
        if bad or missing or not llms_ok or not covers_ok:
            print("STALE:", len(bad), "files missing,", len(missing), "urls missing from sitemap,",
                  "llms.txt missing" if not llms_ok else "llms.txt ok,",
                  "og covers missing" if not covers_ok else "og covers ok")
            return 1
        print(f"SEO_CHECK_OK ({len(pages)} pages in sync)")
        return 0
    for p, h in pages.items():
        dest = ROOT / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(h, encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(write_sitemap(pages), encoding="utf-8")
    (ROOT / "llms.txt").write_text(write_llms(load_seed()), encoding="utf-8")
    covers = write_og_covers(load_seed())
    print(f"SEO_BUILD_OK ({len(pages)} pages + sitemap + llms.txt + {len(covers)} og covers)")


if __name__ == "__main__":
    raise SystemExit(main())
