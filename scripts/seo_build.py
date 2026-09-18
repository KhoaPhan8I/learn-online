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
SITE_FOOT = ('<footer><nav aria-label="Trang"><a href="https://khoaphan8i.github.io/learn-online/">Trang chủ</a> - '
             '<a href="https://khoaphan8i.github.io/learn-online/gia/">Bảng giá</a> - '
             '<a href="https://khoaphan8i.github.io/learn-online/bao-chi/">Báo chí</a> - '
             '<a href="https://khoaphan8i.github.io/learn-online/cho-nguoi-moi-day/">Cho người mới dạy</a> - '
             '<a href="https://khoaphan8i.github.io/learn-online/cho-nguoi-hoc/">Cách tìm lớp</a> - '
             '<a href="https://khoaphan8i.github.io/learn-online/so-sanh/trung-tam/">So sánh trung tâm</a></nav></footer>')

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
<p>🎓 <b>Học {name}:</b> <a href="{site}/?utm_source=seo&utm_medium=course&utm_campaign={slug}">tìm lớp {name} trên Learn Online</a> — hỏi mentor trước khi đăng ký, học phí do mentor tự đặt.</p>
<p>🚀 <b>Dạy {name}:</b> <a href="{site}/?utm_source=seo&utm_medium=teach&utm_campaign={slug}">đăng lớp miễn phí trong 1 phút</a> — muốn có học viên đầu tiên trong 7 ngày thì <a href="{site}/gia/">Ghim Nổi Bật 29k/7 ngày</a> (duyệt 24h, không duyệt hoàn tiền) · ở lại top 2 tuần liền: <a href="{site}/gia/?utm_source=seo&utm_medium=teach&utm_campaign={slug}-ghimdoi">Ghim Đôi 49k/14 ngày, tiết kiệm 9k</a>.</p>
<h2>Khóa học khác</h2>
<ul>
{related}
</ul>
{foot}
</body>
</html>
"""

MENTOR_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}
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
{foot}
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
{foot}
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
        title=html.escape(title), desc=html.escape(desc), name=html.escape(skill["name"]),
        url=url, site=SITE, slug=slug, related=related_links(others), foot=SITE_FOOT).replace(
        f"{SITE}/og-cover.png", f"{SITE}/og-{slug}.png")


def render_mentor(mentor, all_skills):
    slug = slugify(mentor["name"])
    skills = " · ".join(mentor.get("skills", [])[:3]) or "đa kỹ năng"
    desc = f"{mentor['name']} — mentor {skills} trên Learn Online. {mentor.get('bio', '')}".strip()
    url = f"{SITE}/giao-vien/{slug}/"
    mine = {s.strip().lower() for s in mentor.get("skills", [])}
    rel = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/")
           for s in all_skills if s["name"].strip().lower() in mine][:3]
    sample = 'mẫu' in mentor.get('bio', '').lower() or 'mẫu' in mentor.get('name', '').lower()
    robots = '<meta name="robots" content="noindex, follow">' if sample else '<meta name="robots" content="index, follow">'
    return f"giao-vien/{slug}/index.html", MENTOR_TMPL.format(
        robots=robots,
        name=html.escape(mentor["name"]), skills=html.escape(skills),
        desc=html.escape(desc), contact=html.escape(mentor.get("contact", "xem trong bài")),
        url=url, site=SITE, slug=slug, related=related_links(rel), foot=SITE_FOOT)


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
<tr><td>Tìm học viên</td><td>Chạy quảng cáo, phát tờ rơi</td><td>Chia sẻ link, streak, Ghim 29k/7 ngày · ở top 2 tuần: <a href="{site}/gia/?utm_source=seo&utm_medium=compare&utm_campaign=trung-tam-ghimdoi">Ghim Đôi 49k/14 ngày</a></td></tr>
</table>
<p>Trung tâm phù hợp khi bạn cần phòng học vật lý và giáo trình chuẩn. Learn Online phù hợp khi bạn có kỹ năng và muốn dạy ngay, không vốn.</p>
<h2>Nền tảng khóa học đóng gói thì sao?</h2>
<table>
<tr><th>Tiêu chí</th><th>Unica / Edumall / Kyna</th><th>Learn Online</th></tr>
<tr><td>Dạng học</td><td>Video thu sẵn, tự học</td><td>Lớp kèm trực tiếp, hỏi trước khi đăng ký</td></tr>
<tr><td>Ai dạy được</td><td>Qua kiểm duyệt / tuyển chọn</td><td>Bất cứ ai, mở lớp trong 1 phút</td></tr>
<tr><td>Học phí</td><td>Nền tảng định giá</td><td>Mentor tự đặt</td></tr>
</table>
<p>Chi tiết trung thực từng nhà (re-verify 2026-09-18: Unica 49.000đ–999.000đ/khóa qua fetch; Kyna 51.000đ–990.000đ/khóa qua render JS; Edumall chặn fetch nên chưa verify giá). Khe của Learn Online là lớp kèm trực tiếp cho mentor cá nhân — điều cả ba chưa làm.</p>
<p><a href="{site}/?utm_source=seo&utm_medium=compare&utm_campaign=trung-tam">Đăng lớp đầu tiên trên Learn Online</a> — miễn phí, 1 phút xong, không cần mặt bằng.</p>
<h2>Khóa học khác</h2>
<ul>
{related}
</ul>
{foot}
</body>
</html>
"""


PRICE_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bảng giá — Đăng miễn phí, Ghim 29k/7 ngày | Learn Online</title>
<meta name="description" content="Bảng giá Learn Online: đăng lớp miễn phí vĩnh viễn. Ghim Nổi Bật 29.000đ/7 ngày: có học viên đầu tiên trong 7 ngày — kệ Nổi Bật + badge đếm ngược + đứng đầu tìm kiếm. Ghim Đôi 49.000đ/14 ngày (tiết kiệm 9k).">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Product","name":"Ghim Nổi Bật — Learn Online","description":"Có học viên đầu tiên trong 7 ngày: ghim lớp lên kệ Nổi Bật kèm badge đếm ngược. Thanh toán chuyển khoản, duyệt 24h; quá 24h chưa duyệt hoàn đủ trong 24h tiếp.","offers":[{{"@type":"Offer","price":"29000","priceCurrency":"VND","availability":"https://schema.org/InStock","url":"{url}"}},{{"@type":"Offer","name":"Ghim Đôi 14 ngày","price":"49000","priceCurrency":"VND","availability":"https://schema.org/InStock","url":"{url}"}}]}}
</script>
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / Bảng giá</nav>
<h1>Bảng giá: đăng miễn phí vĩnh viễn</h1>
<p>Quy&#7871;t &#273;&#7883;nh h&#7897;i &#273;&#7891;ng 129: <b>kh&#244;ng bao gi&#7901; thu ph&#237; &#273;&#259;ng b&#224;i</b>. Thu nh&#7853;p c&#7911;a b&#7841;n do b&#7841;n t&#7921; &#273;&#7863;t h&#7885;c ph&#237;.</p>
<table>
<tr><th>Gói</th><th>Giá</th><th>Được gì</th></tr>
<tr><td>Miễn phí</td><td>0đ, vĩnh viễn</td><td>Đăng lớp không giới hạn, tự đặt học phí, hỏi/đăng ký/bình luận, streak + referral, lên kệ theo thời gian</td></tr>
<tr><td>Ghim Nổi Bật</td><td>29.000đ / 7 ngày</td><td>Có học viên đầu tiên trong 7 ngày: kệ Nổi Bật + badge đếm ngược + đứng đầu tìm kiếm. Duyệt 24h; quá 24h chưa duyệt hoàn đủ trong 24h tiếp. Bonus đóng đúng lo: Chợ tuần + kịch bản video 60s + mẫu quảng cáo</td></tr>
<tr><td>Ghim Đôi (tiết kiệm 9k)</td><td>49.000đ / 14 ngày</td><td>Ghim 2 đợt 7 ngày liên tiếp cho cùng 1 lớp — phủ 2 tuần vàng tuyển sinh. Quyền lợi như Ghim Nổi Bật ×2. Đặt qua email admin (khoaphanofficial@gmail.com) cùng mã đơn Ghim.</td></tr>
</table>
<p><b>Tính nhanh hoàn vốn:</b> lớp 200.000đ/học viên chỉ cần thêm 1 học viên là hoàn vốn Ghim (29k Ghim / 49k Ghim Đôi 14 ngày). Lớp 50.000đ cần 1 học viên. Lớp 30.000đ cần 1 học viên (Ghim lẻ) / 2 học viên (Ghim Đôi). Ghim càng rẻ khi học phí càng cao.</p>
<h2>Hỏi nhanh trước khi Ghim</h2>
<ul>
<li><b>Đặt Ghim thế nào?</b> Đăng lớp trong app, tick Ghim (29k) hoặc Ghim Đôi (49k), app tạo mã đơn <b>LO-XXXXXX</b> + nội dung CK <b>LEARNONLINE GHIM + mã đơn</b>; gửi mail cho admin (<b>khoaphanofficial@gmail.com</b>) theo hướng dẫn trong app để nhận STK.</li>
<li><b>Ghim Đôi khác gì 2 lần Ghim lẻ?</b> Cùng 1 lớp, 2 đợt 7 ngày liên tiếp (14 ngày, 49k — tiết kiệm 9k), giữ top tìm kiếm liền 2 tuần tuyển sinh thay vì rơi khỏi kệ giữa chừng.</li>
<li><b>Không duyệt thì sao?</b> Duyệt trong 24h; quá 24h chưa duyệt hoàn đủ trong 24h tiếp.</li>
</ul>
<p><a href="{site}/?utm_source=seo&utm_medium=pricing&utm_campaign=gia">Mở lớp đầu tiên miễn phí</a></p>
<script>
// pass incoming utm_* through to CTA so byCamp keeps bundle source (e.g. slug-ghimdoi)
(function(){{var q=new URLSearchParams(location.search),c=q.get('utm_campaign');if(!c)return;var s=q.get('utm_source'),m=q.get('utm_medium');document.querySelectorAll('a[href*=\"utm_\"]').forEach(function(a){{var u=new URL(a.href);u.searchParams.set('utm_campaign',c);if(s)u.searchParams.set('utm_source',s);if(m)u.searchParams.set('utm_medium',m);a.href=u.toString()}})}})();
</script>
<h2>Khóa học khác</h2>
<ul>
{related}
</ul>
{foot}
</body>
</html>
"""


LEARNER_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Muốn học kỹ năng? Tìm lớp kèm trực tiếp 3 bước | Learn Online</title>
<meta name="description" content="Muốn học thêm kỹ năng? 3 bước tìm lớp kèm trực tiếp: gõ kỹ năng, hỏi mentor trước, đăng ký giữ chỗ — miễn phí tìm kiếm.">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / Cho người muốn học</nav>
<h1>Muốn học kỹ năng? Tìm lớp kèm 3 bước</h1>
<ol>
<li>Gõ kỹ năng vào ô tìm kiếm (VD: guitar, tiếng Anh, nấu ăn)</li>
<li>Bấm hỏi mentor trước khi đăng ký — hỏi học phí, lịch, trình độ</li>
<li>Đăng ký giữ chỗ + để lại giờ học mong muốn để mentor xác nhận</li>
</ol>
<p>Khác video thu sẵn: lớp kèm trực tiếp, đi theo tốc độ của bạn.</p>
<p><a href="{site}/?utm_source=seo&utm_medium=usecase&utm_campaign=nguoi-muon-hoc">Tìm lớp ngay</a></p>
<h2>Khóa học gợi ý</h2>
<ul>
{related}
</ul>
{foot}
</body>
</html>
"""


USECASE_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chưa từng dạy ai? Bắt đầu với lớp đầu tiên | Learn Online</title>
<meta name="description" content="Bạn giỏi một kỹ năng nhưng chưa từng dạy? 5 bước mở lớp đầu tiên trong 1 phút — miễn phí đăng bài, học phí tự đặt.">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / Cho người mới dạy</nav>
<h1>Chưa từng dạy ai? Bắt đầu với lớp đầu tiên</h1>
<ol>
<li>Chọn 1 kỹ năng bạn tự tin nhất</li>
<li>Đặt tên lớp rõ ràng: kỹ năng + trình độ + đối tượng</li>
<li>Đặt học phí theo giá thật trên trang, mới dạy lấy giá giữa</li>
<li>Để lại cách liên hệ để học viên nhắn tin</li>
<li>Bấm đăng bài, copy link chia sẻ — mỗi người mở link +2 điểm</li>
</ol>
<p>Muốn có học viên đầu tiên trong 7 ngày? <a href="{site}/gia/">Ghim 29k/7 ngày</a>: lên kệ Nổi Bật + badge đếm ngược, duyệt 24h, quá 24h chưa duyệt hoàn đủ trong 24h tiếp. Ở top 2 tuần liền: <a href="{site}/gia/?utm_source=seo&utm_medium=usecase&utm_campaign=nguoi-moi-day-ghimdoi">Ghim Đôi 49k/14 ngày, tiết kiệm 9k</a>.</p>
<p><a href="{site}/?utm_source=seo&utm_medium=usecase&utm_campaign=nguoi-moi-day">Mở lớp đầu tiên ngay</a></p>
<h2>Khóa học gợi ý</h2>
<ul>
{related}
</ul>
{foot}
</body>
</html>
"""




PRESS_TMPL = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Press kit — Learn Online | Learn Online</title>
<meta name="description" content="Press kit Learn Online: câu chuyện, số liệu, logo và ảnh. Nền tảng chia sẻ khóa học — ai cũng dạy được.">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-cover.png">
</head>
<body>
<nav aria-label="breadcrumb"><a href="{site}/">Learn Online</a> / Báo chí</nav>
<h1>Press kit — Learn Online</h1>
<p>Learn Online là chợ kỹ năng sharing online: ai cũng dạy được, ai cũng học được. Đăng bài miễn phí, học phí do mentor tự đặt.</p>
<h2>Câu chuyện (1 đoạn)</h2>
<p>Học thêm kỹ năng mới ở Việt Nam vẫn đồng nghĩa với đóng học phí cao cho trung tâm. Learn Online đảo ngược mô hình: bất cứ ai giỏi một kỹ năng đều mở lớp trong 1 phút, tự đặt học phí, tự tìm học viên bằng link chia sẻ. Hiện có {nskills} nhóm kỹ năng và {nmentors} mentor khởi đầu.</p>
<h2>Số liệu nhanh</h2>
<ul>
<li>{nskills} nhóm kỹ năng</li>
<li>{nmentors} mentor</li>
<li>Đăng bài miễn phí; Ghim Nổi Bật 29.000đ / 7 ngày — có học viên đầu tiên trong 7 ngày (duyệt 24h; quá 24h chưa duyệt hoàn đủ trong 24h tiếp; kèm Chợ tuần + kịch bản video + mẫu quảng cáo); <a href="{site}/gia/?utm_source=seo&utm_medium=press&utm_campaign=bao-chi-ghimdoi">Ghim Đôi 49.000đ / 14 ngày (tiết kiệm 9k)</a></li>
</ul>
<h2>Asset</h2>
<ul>
<li><a href="{site}/og-cover.png">Logo/cover 1200x630 (PNG)</a></li>
<li><a href="{site}/sitemap.xml">Sitemap đầy đủ</a></li>
<li><a href="{site}/llms.txt">Tóm tắt AI-readable (llms.txt)</a></li>
</ul>
<p>Liên hệ báo chí: xem thông tin trên trang chủ {site}/</p>
<h2>Khóa học</h2>
<ul>
{related}
</ul>
{foot}
</body>
</html>
"""


def render_hub(path, title, desc, crumb, items):
    links = "\n".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for t, u in items)
    return path, HUB_TMPL.format(title=html.escape(title), desc=html.escape(desc),
                                 url=f"{SITE}/{path.replace('index.html', '')}",
                                 site=SITE, crumb=crumb, links=links, foot=SITE_FOOT)


def build():
    seed = load_seed()
    pages = {}
    noindex = set()
    for skill in seed["skills"]:
        p, h = render_course(skill, seed["skills"])
        pages[p] = h
    for mentor in seed["mentors"]:
        p, h = render_mentor(mentor, seed["skills"])
        pages[p] = h
        if 'noindex' in h.split('</head>')[0]:
            noindex.add(p)
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
        url=f"{SITE}/so-sanh/trung-tam/", site=SITE, related=related_links(rel), foot=SITE_FOOT)
    usecase = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/")
               for s in seed["skills"]][:3]
    pages["gia/index.html"] = PRICE_TMPL.format(
        site=SITE, url=f"{SITE}/gia/",
        related=related_links(rel), foot=SITE_FOOT)
    pages["cho-nguoi-hoc/index.html"] = LEARNER_TMPL.format(
        site=SITE, url=f"{SITE}/cho-nguoi-hoc/",
        related=related_links(usecase), foot=SITE_FOOT)
    pages["cho-nguoi-moi-day/index.html"] = USECASE_TMPL.format(
        site=SITE, url=f"{SITE}/cho-nguoi-moi-day/",
        related=related_links(usecase), foot=SITE_FOOT)
    press_rel = [(f"Học {s['name']} online", f"{SITE}/khoa-hoc/{slugify(s['slug'])}/")
                 for s in seed["skills"]][:3]
    pages["bao-chi/index.html"] = PRESS_TMPL.format(
        site=SITE, url=f"{SITE}/bao-chi/",
        nskills=len(seed["skills"]), nmentors=len(seed["mentors"]),
        related=related_links(press_rel), foot=SITE_FOOT)
    return pages, noindex


def write_llms(seed):
    lines = ["# Learn Online", "",
             "Nền tảng chia sẻ khóa học: ai cũng dạy được, ai cũng học được.",
             "Học phí do mentor tự đặt. Đăng bài miễn phí.", "",
             "## Khóa học"]
    for s in seed["skills"]:
        lines.append(f"- [{s['name']}]({SITE}/khoa-hoc/{slugify(s['slug'])}/): {s['blurb']}")
    lines += ["", "## Mentor"]
    for m in seed["mentors"]:
        lines.append(f"- [{m['name']}]({SITE}/giao-vien/{slugify(m['name'])}/): "
                     f"{', '.join(m.get('skills', []))}. {m.get('bio', '')}".rstrip())
    lines += ["", "## Chính sách",
              "- Ghim Nổi Bật: 29.000 VND / 7 ngày — có học viên đầu tiên trong 7 ngày (kệ Nổi Bật + badge đếm ngược + đứng đầu tìm kiếm). Duyệt 24h; quá 24h chưa duyệt hoàn đủ trong 24h tiếp. Bonus đóng đúng lo: Chợ tuần + kịch bản video 60s + mẫu quảng cáo.",
              "- Ghim Đôi: 49.000 VND / 14 ngày (tiết kiệm 9k) — Ghim 2 đợt 7 ngày liên tiếp cho cùng 1 lớp. Đặt qua email admin (khoaphanofficial@gmail.com) cùng mã đơn Ghim.",
              "", "## Trang",
              f"- [Bảng giá]({SITE}/gia/): đăng miễn phí, Ghim 29k/7 ngày · Ghim Đôi 49k/14 ngày.",
              f"- [Báo chí / Press kit]({SITE}/bao-chi/): câu chuyện + số liệu.",
              f"- [Cho người mới dạy]({SITE}/cho-nguoi-moi-day/): 5 bước mở lớp đầu.",
              f"- [Cách tìm lớp]({SITE}/cho-nguoi-hoc/): 3 bước tìm lớp kèm.",
              f"- [So sánh trung tâm]({SITE}/so-sanh/trung-tam/): mở lớp không vốn.",
              f"- Sitemap đầy đủ: {SITE}/sitemap.xml"]
    return "\n".join(lines) + "\n"


def write_og_covers(seed):
    """Sinh og-cover riêng từng kỹ năng (PIL). Trả về {slug: filename}."""
    from PIL import Image, ImageDraw, ImageFont
    import os
    def vi_font(sz):
        for p in [r"C:\Windows\Fonts\arial.ttf", "/c/Windows/Fonts/arial.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
            if os.path.isfile(p):
                try:
                    return ImageFont.truetype(p, sz)
                except Exception:
                    pass
        return ImageFont.load_default()
    out = {}
    for s in seed["skills"]:
        slug = slugify(s["slug"])
        fn = f"og-{slug}.png"
        dest = ROOT / fn
        if dest.is_file() and _og_has_vi(dest):
            out[slug] = fn
            continue
        im = Image.new("RGB", (1200, 630), (15, 15, 20))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 560, 1200, 630], fill=(254, 44, 85))
        d.rectangle([90, 140, 110, 420], fill=(251, 191, 36))
        d.text((140, 200), f"Học {s['name']} online", font=vi_font(64), fill=(244, 244, 246))
        d.text((140, 300), "Learn Online — ai cũng dạy được", font=vi_font(44), fill=(167, 167, 184))
        im.save(dest)
        out[slug] = fn
    return out


def _og_has_vi(path):
    """Covers cũ vẽ không dấu thì vẽ lại. Size>=7KB là điều kiện cần; Image.verify() loại file hỏng/giả PNG."""
    try:
        if path.stat().st_size < 7000:
            return False
        from PIL import Image
        with Image.open(path) as im:
            im.verify()
        return True
    except Exception:
        return False


def write_sitemap(pages, noindex=None):
    import datetime
    today = datetime.date.today().isoformat()
    noindex = noindex or set()
    def prio(u):
        if u == f"{SITE}/":
            return ("daily", "1.0")
        if "/khoa-hoc/" in u or "/giao-vien/" in u:
            return ("weekly", "0.8")
        return ("monthly", "0.6")
    urls = [f"{SITE}/"] + sorted(f"{SITE}/{p.replace('index.html', '')}" for p in pages
                                if p not in noindex)
    body = "\n".join(
        (lambda cf_pr: f"<url><loc>{u}</loc><lastmod>{today}</lastmod>"
         f"<changefreq>{cf_pr[0]}</changefreq><priority>{cf_pr[1]}</priority></url>")(prio(u))
        for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{body}\n</urlset>\n")


def main():
    check = "--check" in sys.argv
    pages, noindex = build()
    if check:
        bad = [p for p in pages if not (ROOT / p).is_file()]
        # content check: generated page on disk must equal rendered output,
        # so hand-edits to built files (e.g. gia/index.html) fail loudly
        # instead of being silently overwritten on next build
        drift = [p for p, h in pages.items()
                 if (ROOT / p).is_file()
                 and (ROOT / p).read_text(encoding="utf-8") != h]
        # bundle-tag check: every page mentioning Ghim Đôi must carry a
        # -ghimdoi campaign tag, or byCamp can't split bundle vs single
        # orders (gia/ exempt: it's the destination, pass-through JS keeps
        # the inbound tag instead of hardcoding one)
        untagged = [p for p, h in pages.items()
                    if p != "gia/index.html"
                    and "Ghim Đôi" in h and "ghimdoi" not in h]
        cur = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        missing = [u for u in [f"{SITE}/{p.replace('index.html', '')}" for p in pages if p not in noindex] if u not in cur]
        stale = [u for u in [f"{SITE}/{p.replace('index.html', '')}" for p in noindex] if u in cur]
        llms = ROOT / "llms.txt"
        llms_txt = llms.read_text(encoding="utf-8") if llms.is_file() else ""
        llms_ok = bool(llms_txt) and all(
            slugify(s["slug"]) in llms_txt
            for s in load_seed()["skills"]) and "Chợ tuần" in llms_txt and "học viên đầu tiên" in llms_txt
        # llms drift: same revert class as pages — generator overwrites
        # llms.txt on every build, so a hand-edit must fail loudly here
        # instead of vanishing silently on the next rebuild
        llms_drift = bool(llms_txt) and llms_txt != write_llms(load_seed())
        llms_state = ("missing" if not llms_txt else
                      "drifted from generator" if llms_drift else
                      "missing keywords" if not llms_ok else "ok")
        covers_ok = all((ROOT / f"og-{slugify(s['slug'])}.png").is_file()
                        for s in load_seed()["skills"])
        covers_vi = all((ROOT / f"og-{slugify(s['slug'])}.png").stat().st_size >= 7000
                        for s in load_seed()["skills"])
        if bad or drift or untagged or missing or stale or not llms_ok or llms_drift or not covers_ok or not covers_vi:
            print("STALE:", len(bad), "files missing,", len(drift), "files drifted from generator,", len(untagged), "bundle pages untagged,", len(missing), "urls missing from sitemap,",
                  len(stale), "noindex urls leaked in sitemap,",
                  "llms.txt " + llms_state + ",",
                  "og covers missing" if not covers_ok else "og covers ok,",
                  "og covers ascii" if not covers_vi else "og covers vi ok")
            if drift:
                print("DRIFT:", ", ".join(drift[:10]))
            if untagged:
                print("UNTAGGED:", ", ".join(untagged[:10]))
            return 1
        print(f"SEO_CHECK_OK ({len(pages)} pages in sync)")
        return 0
    for p, h in pages.items():
        dest = ROOT / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(h, encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(write_sitemap(pages, noindex), encoding="utf-8")
    (ROOT / "llms.txt").write_text(write_llms(load_seed()), encoding="utf-8")
    covers = write_og_covers(load_seed())
    print(f"SEO_BUILD_OK ({len(pages)} pages + sitemap + llms.txt + {len(covers)} og covers)")


if __name__ == "__main__":
    raise SystemExit(main())
