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
- [x] Cho buyer chọn Ghim Đôi 49k trong app (checkbox f-boost2 + plan/price plumbing + revenue sums — `a90b5f7`, DOI_VERIFY_PASS 16/16 + GUARD_OK).
- [x] expRev theo giá từng đơn (pending-sum × conv thay vì flat 29k — EXPREV_VERIFY_PASS + GUARD_OK).
- [x] Upsell Ghim Đôi trên 10 trang SEO khóa học (generator PAGE_TMPL line teach-path: link Ghim Đôi 49k/14d tiết kiệm 9k cạnh CTA Ghim 29k; build lại 18 pages — `56ff1f7`, GUARD_OK + SEO_CHECK_OK).
- [x] Follow-up cho traffic SEO thấy CTA Ghim Đôi (mục 7 `docs/OUTREACH_GHIM_29K.md`: mẫu nhắn cho visitor `utm_medium=teach|course` chưa tick Ghim — `d5a607d`, UNVERIFIED, DM-gated chờ Owner duyệt target).
- [x] Ghim Đôi vào bảng so-sanh trung tâm (generator COMPARE_TMPL hàng "Tìm học viên": Ghim Đôi 49k/14d cạnh Ghim 29k; build lại khớp — `14d3348`, GUARD_OK + SEO_CHECK_OK).
- [x] Ghim Đôi vào trang usecase + báo chí (generator USECASE_TMPL CTA + PRESS_TMPL dòng giá; build lại 18 pages — `7a74165`, GUARD_OK + SEO_CHECK_OK).
- [x] Copy 29k lẻ còn sót trong generator đồng bộ bundle (meta description + dòng hoàn vốn + llms link bảng giá đều nhắc Ghim Đôi; title giữ nguyên cho gọn SEO; build lại 18 pages, GUARD_OK + SEO_CHECK_OK).
- [x] Tag campaign riêng cho link Ghim Đôi (course: `{slug}-ghimdoi`, usecase: `nguoi-moi-day-ghimdoi`; 10 trang khóa học + usecase rebuild khớp; `byCamp` tách được click bundle khỏi Ghim lẻ; GUARD_OK + SEO_CHECK_OK).
- [x] Giữ tag bundle qua trang `gia/` (pass-through JS: CTA mang `utm_campaign` đến thay vì hardcode `gia`; fix `KeyError: 'slug'` do brace trong comment template; GUARD_OK + SEO_CHECK_OK).
- [x] Guard kiểm tra JS cả trang `gia/` (trước đây chỉ `index.html`; gia có script pass-through mà không ai check — `GIA_JS_SYNTAX_OK`, GUARD_OK).
- [x] Tag campaign cho 2 CTA Ghim Đôi còn sót (so-sanh: `trung-tam-ghimdoi`, báo chí: `bao-chi-ghimdoi`; mọi CTA bundle giờ đều có tag riêng; GUARD_OK + SEO_CHECK_OK).
- [ ] Đóng vòng upsell: khi slug ghimdoi49k ra đơn đầu, scale copy trang SEO có convert cao nhất trước (dùng `byCamp`).
