# BACKLOG — learn online (P2 course $)

## Tier 0 — sự cố
- [ ] Ra khỏi `$0 UNVERIFIED`: cần buyer thật hoặc payment proof — không dừng ở demo.
- STATE blocker 2026-09-18: checkout manual, `PAY_DEFAULT={bank:'',acc:''}` trống → buyer phải email admin chờ STK; cần Owner điền STK (`savePay`/PAY_DEFAULT) + duyệt target outbound DM trước khi gửi (rào: no public post/DM, no push main).

## Tier 1 — roadmap tuần
- [x] `/ship` 1 course unit bán được (b76883a: 10 course pages learner+mentor CTA + Ghim 29k upsell).
- [x] Funnel teach-path: seoPrefill prefill q+f-skill (8590cb1, 4/4 logic PASS + SEO_CHECK_OK + NODE_SYNTAX_OK).
- [ ] Thiếu checkout auto → `/feature-dev` khi Owner duyệt STK công khai.

## Tier 2 — bảo trì
- [x] Đồng bộ landing/checkout với funnel hiện tại (teach CTA → seoPrefill q+f-skill, mailto checkout giữ nguyên).

## Tier 3 — research (không đáy)
- [x] Doc cấu hình STK cho Owner 1 chạm (`docs/PAY_STK_SETUP.md` — Cách A trong app / Cách B PAY_DEFAULT).
- [x] Packaging 1 upsell / bundle nhỏ (2026-09-18: hàng Ghim Đôi 49k/14 ngày tiết kiệm 9k vào `gia/index.html`, line 24).
- [x] Theo dõi slug nào convert đầu tiên qua utm_campaign (`addBoostIntent` lưu med/camp từ `attrLast`, `boostRevenue.byCamp`, `revCampHtml` nối vào `revHtml`, self-test `boost byCamp slug` — BYCAMP_VERIFY_PASS + SEO_CHECK_OK).
- [x] So sánh 2 CTA trên landing (đã live sẵn: `applyAb()` ở init line 830, verdict + export CSV trong dashboard, AB_CTA_VERIFY_PASS 5/5).
- [x] Copy outreach cho bundle Ghim Đôi 49k (mục 6 trong `docs/OUTREACH_GHIM_29K.md`, UNVERIFIED).
- [x] Bundle ở điểm mua: hàng Ghim Đôi trong modal `boostSheetHtml` So sánh gói (`e8c6941`, GUARD_OK).
- [x] Đóng vòng byCamp: cột medium+campaign trong `don-ghim.csv` export (`b67bdbb`, CSV_ATTR_VERIFY_PASS).
- [x] Bundle trong generator `seo_build.py` (source of truth: PRICE_TMPL JSON-LD 2 offers + hàng Ghim Đôi + llms.txt; build lại `gia/` khớp — `547d7f6`, GUARD_OK + SEO_CHECK_OK). Bài học: KHÔNG sửa tay `gia/index.html`, generator sẽ ghi đè.
- [ ] Cho buyer chọn Ghim Đôi 49k trong app (peer pane đang làm, uncommitted `M index.html`: checkbox f-boost2 + plan/price plumbing + revenue sums — để peer commit).
- [x] Upsell Ghim Đôi trên 10 trang SEO khóa học (generator PAGE_TMPL line teach-path: link Ghim Đôi 49k/14d tiết kiệm 9k cạnh CTA Ghim 29k; build lại 18 pages — `56ff1f7`, GUARD_OK + SEO_CHECK_OK).
- [ ] Đóng vòng upsell: khi slug ghimdoi49k ra đơn đầu, scale copy trang SEO có convert cao nhất trước (dùng `byCamp`).
