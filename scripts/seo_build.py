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
        url=url, site=SITE, slug=slug, related=related_links(others))


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
<p><a href="{site}/?utm_source=seo&utm_medium=compare&utm_campaign=trung-tam">Đăng lớp đầu tiên trên Learn Online</a></p>
<h2>Khóa học khác</h2>
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
        if bad or missing or not llms_ok:
            print("STALE:", len(bad), "files missing,", len(missing), "urls missing from sitemap,",
                  "llms.txt missing" if not llms_ok else "llms.txt ok")
            return 1
        print(f"SEO_CHECK_OK ({len(pages)} pages in sync)")
        return 0
    for p, h in pages.items():
        dest = ROOT / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(h, encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(write_sitemap(pages), encoding="utf-8")
    (ROOT / "llms.txt").write_text(write_llms(load_seed()), encoding="utf-8")
    print(f"SEO_BUILD_OK ({len(pages)} pages + sitemap + llms.txt)")


if __name__ == "__main__":
    raise SystemExit(main())
