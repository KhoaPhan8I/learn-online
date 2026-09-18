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
- [ ] So sánh 2 CTA trên landing.
