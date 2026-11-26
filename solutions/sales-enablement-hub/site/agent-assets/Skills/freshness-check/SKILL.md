---
name: freshness-check
description: Finds Content Library assets that are expired or expiring within 30 days, flags the customer shares that point at them, and proposes archive moves. Use when someone says "what's expiring", "run the freshness check", "clean up old content".
---

# Freshness check

1. In **Content Library**, list assets where Expires on is before today (Expired) or within the next 30 days
   (Expiring), with owner and popularity.
2. For each, list **Customer Shares** rows whose Source asset points at it; set Status = **Source expired** for expired
   assets (ask before writing more than 10 rows).
3. List **Decks** (customer decks Copilot built) whose Source slides name a slide that came from an expired asset,
   so the seller can rebuild them.
4. Propose, do not perform, moves to **Archive** for expired assets; on the user's yes, move them with Archived on =
   today and Reason = Expired, and add a **Content Requests** row asking the owner for a renewal when the asset is
   still in use.
5. Reply with a short table: asset, expires, owner, open shares, affected decks, proposed action.
