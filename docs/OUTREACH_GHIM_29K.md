# Outreach Ghim 29k — copy gửi được ngay (verify live 2026-09-18)

Nguồn copy: hàm trong `index.html` đã eval trên live
(`inviteText` / `adText` / `videoScript` / `followupText` / `objectionText` /
`payLine` / `ckText`). Doanh thu live lúc chốt pack: **$0 UNVERIFIED**
(`rev got=0 pending=0`, `boost=[]`, `posts=[]`).

## 1. Nhắn mời (Zalo / FB / comment)

> Chào Bạn! Thấy bạn hỏi/đăng ký 3 lần trên Learn Online — bạn rõ kỹ năng bạn
> quan tâm lắm rồi. Mở lớp đầu tiên chỉ 1 phút, miễn phí, học phí tự đặt.
> Muốn có học viên đầu tiên trong 7 ngày thì tick Ghim 29k — duyệt 24h,
> không duyệt hoàn tiền. Mình hướng dẫn nếu cần!

Link kèm (utm invite):

- https://khoaphan8i.github.io/learn-online/?utm_source=zalo&utm_medium=invite&utm_campaign=ghim29k
- Bảng giá: https://khoaphan8i.github.io/learn-online/gia/
- Ví dụ lớp: https://khoaphan8i.github.io/learn-online/khoa-hoc/guitar/

## 2. Mẫu quảng cáo + video 60s (đăng group / story)

```
🔥 [Guitar] Guitar đệm hát cơ bản
💰 Học phí: 200k/buổi — học thử buổi đầu, không hợp không mất gì
👨‍🏫 Mentor: Khoa (xem hồ sơ + đánh giá trên Learn Online)
👉 Đăng ký ngay — số chỗ có hạn mỗi tuần!
```

Kịch bản video 60s (quay bằng điện thoại):

- [0-5s] HOOK (nhìn thẳng camera): "Bạn muốn Guitar mà không tốn tiền triệu?
  Nghe mình 60 giây."
- [5-25s] VẤN ĐỀ + GIẢI PHÁP: "Mình là Khoa. Lớp Guitar đệm hát cơ bản,
  học phí 200k/buổi. Bạn được gì sau buổi đầu: ..." (kể 1 kết quả cụ thể)
- [25-45s] BẰNG CHỨNG: quay màn hình bài giảng / học viên cũ nói 1 câu /
  mở lớp demo 30 giây
- [45-60s] CTA: "Link đăng ký mình để dưới phần mô tả — nhắn tin là học
  ngay tuần này."

## 3. Follow-up + xử lý từ chối

- Follow-up (ngày 2): "Khoa chào bạn — hôm trước mình có nhắn về lớp Guitar
  đệm hát cơ bản. Không biết bạn đã xem qua chưa? Chỉ cần rep "1" mình gửi
  link chi tiết nhé."
- Từ chối "đắt": "Hiểu mà! So với trung tâm (vài triệu/khóa) thì lớp mình
  200k/buổi là nhẹ lắm. Mà buổi đầu học thử — không hợp không mất gì, bạn
  có muốn thử 1 buổi không?"

## 4. Chốt đơn Ghim (buyer tick Ghim lúc Đăng bài)

1. Buyer điền tên / kỹ năng / tiêu đề / liên hệ → tick
   📌 Ghim Nổi Bật 7 ngày (29k) hoặc 📌📌 Ghim Đôi 14 ngày (49k) → Đăng bài.
2. App tạo đơn pending mã `LO-XXXXXX` + nội dung CK `LEARNONLINE GHIM LO-XXXXXX`
   (hàm `ckText`, đã verify live).
3. Thanh toán hiện tại (chưa có STK công khai — P2):
   `Gửi đơn cho admin qua email khoaphanofficial@gmail.com để nhận STK + CK 29k (Ghim lẻ) / 49k (Ghim Đôi)
   — nội dung: LEARNONLINE GHIM + mã đơn` (hàm `payLine`, đã verify live).
4. Share link đơn: `https://khoaphan8i.github.io/learn-online/?code=LO-XXXXXX`
   — mở link là thấy đơn + modal Ghim.
5. Admin duyệt trong 24h, quá 24h chưa duyệt hoàn đủ trong 24h tiếp.

## 5. Blocker P2 — cần Khoa (không bịa STK)

- `index.html:294` còn `const PAY_DEFAULT={bank:'',acc:''};`
- Cần: STK thật + Zalo nhận đơn + check mailbox
  `khoaphanofficial@gmail.com` để thấy mailto đơn đầu và xác nhận CK 29k (Ghim lẻ) / 49k (Ghim Đôi).
- Khi có STK: điền vào `PAY_DEFAULT`, chạy `scripts/guard.cmd`,
  T count tick, push live, re-eval `payLine(code)` + `boostRevenue()`.

## 6. Bundle Ghim Đôi 49k/14 ngày (mở rộng 2026-09-18, UNVERIFIED)

Hàng bundle trên `gia/` (tiết kiệm 9k so với 2×29k). Kịch bản dùng:
buyer đã Ghim 1 tuần, còn 1–2 ngày hết hạn mà chưa đủ học viên → upsell Ghim tiếp.

> Tuần Ghim đầu sắp hết mà lớp bạn mới có X đăng ký — đừng để rơi khỏi kệ
> Nổi Bật đúng lúc đang nóng. Ghim Đôi 49k/14 ngày (tiết kiệm 9k so với
> Ghim lẻ 2 lần): giữ top tìm kiếm liền 2 tuần tuyển sinh. Rep "DOI" mình
> giữ suất + gửi nội dung CK nhé!

Link kèm: https://khoaphan8i.github.io/learn-online/gia/
Quy trình chốt đơn giữ nguyên mục 4 (mã `LO-XXXXXX`, nội dung CK
`LEARNONLINE GHIM + mã đơn`), chỉ khác số tiền 49k — ghi rõ trong mail
gửi admin khi STK về.

## 7. Follow-up cho traffic SEO thấy CTA Ghim Đôi (mở rộng 2026-09-18, UNVERIFIED)

10 trang `khoa-hoc/*` đã có link Ghim Đôi cạnh CTA Ghim 29k (`56ff1f7`).
Khi có đăng ký/hỏi bài từ nguồn `utm_medium=teach|course` mà chưa tick
Ghim, dùng mẫu này (chờ Owner duyệt target trước khi gửi — rào:
no public post/DM):

> Bạn vào xem lớp [TÊN LỚP] từ trang [TÊN KHÓA HỌC] đúng không? Mở lớp
> miễn phí 1 phút là xong. Muốn có học viên đầu tiên trong 7 ngày thì
> tick Ghim 29k (duyệt 24h, không duyệt hoàn tiền); muốn giữ top 2 tuần
> tuyển sinh liền thì Ghim Đôi 49k/14 ngày — tiết kiệm 9k so với Ghim lẻ
> 2 lần. Rep "GHIM" hoặc "DOI" mình giữ suất + gửi nội dung CK nhé!

Link kèm: https://khoaphan8i.github.io/learn-online/gia/ + link lớp cụ thể.
Chốt đơn giữ nguyên mục 4, số tiền 29k/49k ghi rõ trong mail gửi admin
khi STK về.

## 8. Chốt khi buyer chê 49k "đắt" (mở rộng 2026-09-18, UNVERIFIED)

Hoàn vốn app (`ghimRoi`, `index.html:440`) hiện luôn tính trên Ghim lẻ
29k — buyer Đôi cần nghe con số 49k. Công thức nói miệng: **lớp [GIÁ]/hv
chỉ cần [N]=ceil(49000/GIÁ) học viên là hoàn vốn Ghim Đôi 14 ngày**;
ví dụ lớp 200k → 1 học viên, lớp 50k → 1 học viên, lớp 30k → 2 học viên
(trước khi gửi tự tính lại N cho đúng giá lớp buyer — không đọc số mẫu mù).

> 49k nghe to nhưng tính theo lớp bạn ([GIÁ]k/hv): chỉ cần thêm [N]
> học viên trong 14 ngày là hoàn vốn — còn 13 ngày còn lại là lãi.
> Ghim lẻ 2 lần tốn 58k; Đôi gộp 49k tiết kiệm 9k + không rơi khỏi top
> giữa chừng. Không duyệt hoàn đủ như Ghim lẻ. Rep "DOI" mình giữ suất nhé!

Chốt đơn giữ nguyên mục 4, số tiền 49k + mã đơn ghi rõ trong mail gửi admin.
