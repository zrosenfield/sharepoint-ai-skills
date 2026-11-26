---
name: publish-approved
description: Publishes approved Content Intake files to the Content Library with dates and status, and keeps the hub fresh. Use when someone says "publish approved content", "publish this", or after the Publish to library quick step moved a file.
---

# Publish approved content

1. Find Content Intake files whose approval status is **Approved** (or the file the user selected). Never publish
   anything that is not approved.
2. Move each file to the **Content Library** root (the "Publish to library" quick step does this in one click; if you
   move it yourself, keep the same file name). Metadata columns with the same internal name carry over.
3. On the moved file set: Published on = today; Expires on = Proposed expiry if given, otherwise today + 6 months;
   Shareability = the approved shareability; Featured = No; Popularity = 0. Keep Content owner.
4. If the file replaces an older asset (same title or the submitter said so), move the older file to **Archive** with
   Archived on = today, Reason = Replaced, Replaced by = link to the new file, and update any **Customer Shares** rows
   whose Source asset is the old file to Status = **Source updated**.
5. Report what was published, with links, and anything you could not publish and why.
