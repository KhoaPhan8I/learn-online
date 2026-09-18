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
- [x] So sánh 2 CTA trên landing (đã live sẵn: `applyAb()` def 825 / init 833, verdict + export CSV trong dashboard, AB_CTA_VERIFY_PASS 5/5).
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
- [x] FAQ Ghim trên trang `gia/` (3 hỏi: đặt Ghim thế nào / Đôi khác gì 2 lần lẻ / không duyệt thì sao; copy khớp quy trình manual + số tiền thật; GUARD_OK + SEO_CHECK_OK).
- [x] Địa chỉ admin trên mọi điểm chạm mua (trước đây `gia/` + bundle chỉ ghi "email admin" không địa chỉ — buyer từ SEO kẹt; thêm `khoaphanofficial@gmail.com` vào hàng bundle, FAQ, llms.txt; GUARD_OK + SEO_CHECK_OK).
- [x] Copy chốt đơn khớp 2 mức giá (mục 4 outreach chỉ ghi CK 29k — buyer Ghim Đôi nhận sai số tiền; thêm tick Đôi + CK 29k/49k theo gói; UNVERIFIED, DM-gated).
- [x] Doc STK đồng bộ `payLine(code)` của peer (PAY_STK_SETUP còn quote fallback cũ `CK 29k` + anchor dòng stale; sửa quote 3 nhánh + anchor `savePay:678/setPay:296/PAYK:293/getPay:295/payLine:297/boostPrice:420/tests:1232-1234`; docs-only, không chạm hunk peer).
- [x] Outreach §5 blocker đồng bộ 2 giá (còn quote `CK 29k` + anchor `index.html:293` stale + `payLine()` cũ; sửa `index.html:294`, CK 29k/49k, `payLine(code)`; docs-only).
- [ ] App-lane: `ghimRoi()` (`index.html:440`) luôn hoàn vốn trên `GHIM_PRICE=29000` — buyer tick Ghim Đôi 49k thấy dòng "hoàn vốn 29k Ghim" sai số tiền; cần truyền giá theo đơn như `payLine(code)` (ghi nhận, không sửa — lane peer).
- [x] Copy xử lý từ chối 49k (mục 8 outreach: công thức hoàn vốn Đôi `ceil(49000/giá lớp)` + mẫu nhắn reframe 58k→49k tiết kiệm 9k; UNVERIFIED, DM-gated).
- [x] Guard content-drift cho trang build (`seo_build.py --check` chỉ check tồn tại/sitemap/llms/og nên sửa tay `gia/index.html` mất lặng khi rebuild — đúng lớp lỗi bundle-revert; thêm so disk vs render in-memory, in `DRIFT: <file>`, exit 1; proof: chèn comment → `1 files drifted`, restore → `SEO_CHECK_OK`; GUARD_OK).
- [x] Dòng hoàn vốn `gia/` khớp outreach §8 (trước đây ví dụ chỉ 200k/50k, thiếu case 30k mà §8 đã chốt: lẻ 1 hv / Đôi 2 hv; sửa PRICE_TMPL + rebuild `gia/`; GUARD_OK + SEO_CHECK_OK).
- [x] Guard tag bundle `-ghimdoi` (`--check` xanh dù page nhắc Ghim Đôi mà mất tag thì `byCamp` mù bundle-vs-lẻ; thêm `untagged` fail + in `UNTAGGED:`, `gia/` exempt vì pass-through giữ tag inbound; proof: template regression → `untagged-probe` bắt, cây thật `untagged-now: []`; GUARD_OK).
- [x] Guard drift `llms.txt` (`--check` chỉ check keyword nên sửa tay biến mất lặng khi rebuild — đúng lớp lỗi bundle-revert còn sót; thêm so disk vs `write_llms(seed)` in-memory, in `llms.txt drifted from generator`, exit 1; proof: append comment → `DIRTY_EXIT=1`, restore → `SEO_CHECK_OK`; GUARD_OK).
- [x] Guard drift `sitemap.xml` (`--check` chỉ check missing/stale URL nên sửa tay cấu trúc (<priority>/<changefreq>) biến mất lặng khi rebuild — lớp revert còn sót cuối; thêm so disk vs `write_sitemap()` strip `<lastmod>` (tránh false-positive theo ngày), in `sitemap drifted from generator`, exit 1; proof: append comment → `DIRTY_EXIT=1`, restore → `SEO_CHECK_OK`; GUARD_OK).
- [x] Guard cover `og-*.png` (`covers_vi` chỉ check `.stat().st_size>=7000` nên PNG hỏng >7k qua mặt, thiếu file thì crash thay vì fail đẹp; dùng chung `_og_has_vi` của build (size+`Image.verify()`+crash-safe); proof: 8k rác → `og covers ascii` EXIT=1, xóa file → `og covers missing` EXIT=1 (không traceback), restore → `SEO_CHECK_OK`; GUARD_OK).
- [ ] Đóng vòng upsell: khi slug ghimdoi49k ra đơn đầu, scale copy trang SEO có convert cao nhất trước (dùng `byCamp`).
