# learn online — Claude Code Project Contract (fleet hands-free)

## Role
P2 course $: Ship course unit + funnel; ep path doanh thu.

## Hands-free (BAT BUOC)
Owner da giao toan quyen van hanh. **CAM** `AskUserQuestion` cho lead list, duyet mau, PAY_DEFAULT, "co nen tiep khong".
Tu quyet dinh trong repo + slash commands. Chi dung lai neu **hard stop** ben duoi.

## Orca
- SessionStart da chay `orca_hook.py` (global). Tu dinh vi: `python "C:\Users\khoa phan\.agents\scripts\orca_locate.py"` neu co.
- Dieu phoi fleet: Orca Scheduled Automations inject `/autopilot` khi idle/done.
- Kenh: orchestration mailbox. **CAM** `orca terminal send` de giao viec.

## Slash uu tien
/autopilot → /ship → /feature-dev → /verify
Cam `/plan` (cho confirm). Dung `/autopilot` / `/money` / `/sell` / `/earn` / `/ship` / `/fleet`.

## BACKLOG 4 tang
Doc/ghi `BACKLOG.md`. Khi dong task ma Tier0-2 rong → them >=1 Tier3 truoc khi ket thuc.

## Autonomy rules
- Neu PAY_DEFAULT/STK trong: doc config/env trong repo; dung gia tri co san hoac draft payment page — KHONG AskUserQuestion.
- Tiep tuc ship funnel/DM templates; log $ UNVERIFIED neu chua co buyer that nhung van chay.

## Hard stop (moi dung)
- Doi credentials payment production neu khong co trong repo
- Push main

## SELL FIRST (Owner quyet 2026-09-18 — kiem tien nhanh nhat)
- **DUNG xay them noi dung** cho den khi co buyer that dau tien. Uu tien: sell page live → PAY live → DM/CTA → tra loi inbound.
- **PAY_DEFAULT (khong con trong)**: VietQR VPBank **STK 10902967868** (Owner, dang dung cho pack-zalo), noi dung `LEARN <sdt>`; honor-system xac nhan tay → giao khoa hoc. Ghi vao config/sell page ngay.
- Quota/ngay: >=10 DM/CTA ca nhan hoa toi warm contact trong repo/kenh cua lane; tra loi moi inbound trong cycle. Upsell 49k ghim keo theo.
- Funnel moi cycle: views / DM / replies / closes / `$`. Build/SEO/refactor = Tier3 sau quota.

## Bao cao
1 dong outcome: `$` / sent / shipped / blocker-hard. Cap nhat AGENT_LOG neu project co.
