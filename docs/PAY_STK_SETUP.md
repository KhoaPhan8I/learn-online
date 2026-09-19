# Cấu hình STK nhận Ghim 29k/49k — LIVE 2026-09-18 (SELL FIRST)

Trạng thái live: **PAY live, $0 UNVERIFIED** — `PAY_DEFAULT={bank:'VietQR VPBank',acc:'10902967868'}` (STK Owner, SELL FIRST 2026-09-18); buyer thấy STK + nội dung CK `LEARNONLINE GHIM + mã đơn` ngay, honor-system xác nhận tay.
Đổi STK sau này = Cách A (trong app, không đụng code) hoặc Cách B (sửa `index.html:294`).

## Cách A — trong app, 1 phút (khuyên dùng, không đụng code)

1. Mở app → mở sheet **Ghim Nổi Bật** (tick "Ghim Nổi Bật" lúc đăng lớp, hoặc nút Ghim).
2. Cuối sheet có 2 ô: `Admin: ngân hàng` + `Admin: số tài khoản` → điền → bấm **Lưu STK**.
3. Xong: `payLine(code)` hiện `CK <bank> <acc> — CK 29k/49k — nội dung: LEARNONLINE GHIM + mã đơn` (số tiền theo đơn qua `boostFind`+`boostPrice`; không truyền mã đơn thì hiện STK chung không kèm số tiền).
   Đổi STK sau này = lặp lại 3 bước; có Hoàn tác nếu nhập nhầm.

Kỹ thuật: `window.savePay()` (`index.html:678`) + `setPay()` (`index.html:296`) lưu vào `localStorage['learn-online-pay-v1']`
(`PAYK`, `index.html:293`), được backup/restore tự động (`backupKeys`, `index.html:511`).

## Cách B — cứng trong repo (STK theo mọi máy, cần sửa code + deploy)

Sửa 1 dòng `index.html:294`:

```js
const PAY_DEFAULT={bank:'VietQR VPBank',acc:'10902967868'}; // live 2026-09-18 (SELL FIRST)
```

Để trống lại `{bank:'',acc:''}` = quay về fallback cũ (báo chưa cấu hình — chỉ dùng khi Owner đổi STK).
`getPay()` (`index.html:295`) ưu tiên localStorage (Cách A) trước `PAY_DEFAULT`.

## Buyer thấy gì (không đổi code)

- Live 2026-09-18 (có STK): `CK VietQR VPBank 10902967868[ — CK 29k/49k] — nội dung: LEARNONLINE GHIM + mã đơn` + nút Copy nội dung CK / Copy link đơn / Gửi đơn cho admin trong sheet.
- Dự phòng khi mất STK, gọi không kèm mã đơn: `Gửi đơn cho admin qua email khoaphanofficial@gmail.com để nhận STK + CK 29k (Ghim 7 ngày) / 49k (Ghim Đôi 14 ngày) — nội dung: LEARNONLINE GHIM + mã đơn` (`payLine`, `index.html:297`).
- Dự phòng khi mất STK, gọi kèm mã đơn (`payLine(code)`): thêm `CK 29k` hoặc `CK 49k` theo đúng đơn (tra qua `boostFind(code)` + `boostPrice()`; `boostPrice` ở `index.html:420` suy ra từ `plan`/`price`).

## Verify sau khi điền (30 giây)

1. Mở app `?test=1` → 3 test phải xanh: `pay cfg`, `pay undo`, `pay rerender` (`index.html:1232-1234`).
2. Mở sheet Ghim → dòng Thanh toán hiện đúng STK vừa nhập.

## Rào Owner (không tự làm)

- STK live là của Owner cung cấp (SELL FIRST 2026-09-18): agent KHÔNG tự bịa STK khác; đổi STK sau này Owner tự nhập 1 trong 2 cách trên.
- Outbound DM/post công khai vẫn cần Owner duyệt target (rào anti-spam).
- Push `main`/production: Owner gate.
