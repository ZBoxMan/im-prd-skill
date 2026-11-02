# Cross-module concept ownership table

> Split out of README (2026-10-31). A concept's tier, options, recommendation and magnitude are given only in the owner entry; other entries write only "See owner ID". Change rules only in the owner entry; `scripts/lint_skill.py` validates this table row by row.

A concept's tier, options, recommendation and magnitude are given only in the owner entry; related entries in other modules write only "See owner ID" and no longer give options, recommendation or magnitude (for how to write pointer entries see "How to use" item 3). When changing rules, change only the owner entry. A third column reading "— (no referencing entries yet)" means no other module has an entry touching that concept yet; when one is added, add "See owner ID" and backfill this table.

| Concept | Sole owner | Entries in other modules (write only "See owner ID") |
|---|---|---|
| Chat sorting (including whether drafts affect sorting) | LIST-20 | UI-10 |
| Whether a group chat summary carries the sender name prefix | LIST-28 | UI-05 |
| Offline sending: queueing, auto-resume, lifetime, turning into failure | SEND-10 | UX-15, SEND-05 |
| Accidental-tap protection for deleting a chat (confirmation or timed undo) | LIST-26 | UX-11 |
| Timed undo after "delete for me only" on a message | ACT-26 | UX-11 |
| Feedback to a blocked sender after sending | REL-22 | SEND-12, REL-07, SEND-20 |
| Reciprocity rule of the read receipt toggle | SEND-16 | REL-29, REL-13 |
| Form of the read receipt and typing indicator toggles (how many toggles, whether per-chat override) | SEND-22 | REL-29 |
| Whether @mention-me passes through mute, and its default | NOTI-20 | GRP-13, LIST-02, NOTI-05 |
| Whether @all passes through mute | NOTI-21 | GRP-21, LIST-07 |
| Incoming calls from muted chats, group-level muted calls | NOTI-30 | NOTI-08, LIST-02, LIST-22 |
| Pinned chat cap and overflow handling | LIST-01 | UI-09 |
| Pinned message cap and full-quota policy | ACT-21 | ACT-12, UI-17 |
| New messages in an archived chat | LIST-23 | UI-D6, UI-13 |
| Whether muted chats count toward the total badge count | NOTI-26 | UX-D6, UX-23, NOTI-07, LIST-02 |
| Draft saving, restoring, clearing and overwrite confirmation | UI-31 | MISC-15, LIST-05 |
| Draft indicator in the chat list | LIST-05 | UI-31 |
| Cap on multi-select and forward message count | ACT-02 | ACT-10, UX-07 |
| Cap on target chats per forward | ACT-19 | UX-07 |
| Unread count truncation cap | UX-D5 | LIST-10, UI-08 |
| De-emphasized presentation of unread in muted chats | UX-23 | LIST-10, UI-08 |
| Invitee restricting direct adds through privacy settings | REL-11 | GRP-17 |
| Stranger contact model (whether they can message directly, whether they go to message requests first) | REL-21 | SEND-13, LIST-24, DISC-10, INV-20, AGE-19 |
| Last seen shown to the blocked party | REL-08 | SEND-19 |
| Silence and unread accumulation during mute | NOTI-04 | LIST-02 |
| Approver, request state chain and validity period of group join approval | GRP-08 | GRP-19 |
| Default audience of feed posts and stories (including tightening for minor accounts) | FEED-20 | REL-26 (must define "default visibility scope"), AGE-17 |
| Age-judging basis and defaults for accounts that have not completed age confirmation | AGE-07 | FEED-20, PAY-23, ACC-28, WAL-12, ADS-17, PRIV-27, PTS-12 |
| Prompt when the original content disappears while a feed interaction is in flight | FEED-08 | FEED-03 |
| Unread, @ and mute basis of topics and reply threads | FEED-39 | module 03 Must-ask states row "topic or reply thread" |
| Forward, favorite, quote and edit restrictions on payment-type messages (transfer, red packet, collect payment cards), and whether the unsend entry shows | PAY-07 | ACT-03, ACT-28, ACT-04; module 10 Must-ask states row "messages with specific content" |
| Whether unsending a payment card affects the funds (whether the initiator can unilaterally undo after payment succeeds) | PAY-01 | PAY-07 |
| Blocking on unsettled funds before removing a contact, deleting a chat, or leaving a group | PAY-26 | REL-23, LIST-08, GRP-10; module 02 Must-ask states row "remove contact" |
| Whether official accounts, service accounts, bots and system chats can be blocked | BOT-28 | module 02 Must-ask states row "special objects" |
| Labeling of AI-generated content (including AI-generated replies sent by bots) | AI-03 | BOT-03, SUP-07 |
| Whether encrypted chats can use content-outbound capabilities such as translation and AI | AI-14 | SAFE-22, BOT-22 |
| Prompt and "Go to Settings" entry after a system permission is denied | DISC-02 | MISC-38, MISC-10, UX-18, INV-08, PRIV-23 |
| Expiry mechanism of invite links and QR codes (including group QR codes) | GRP-07 | DISC-09, INV-06, INV-01 |
| Validity period and use count of invite links and group QR codes | GRP-18 | DISC-09, INV-06 |
| Who fetches and generates the link preview (sender's device or server) | RICH-57 | MISC-31, SAFE-22 |
| Whether link previews are generated by default (including encrypted chats) | MISC-31 | SAFE-22, RICH-34, RICH-57 |
| Scope of the shared person's info in a contact card and the shared person's control | RICH-44 | REL-25, DISC-15 |
| Whether to introduce channel, community and topic forms | GRP-15 | FEED-29 |
| Channel publishing identity and subscriber count | FEED-10 | GRP-15 |
| Visibility of channel subscriber and community member lists | FEED-30 | GRP-15 |
| Channel comment section | FEED-31 | GRP-15 |
| Channel content retention and what new subscribers can see | FEED-32 | GRP-15 |
| Cap on the number of groups and total members in a community | FEED-14 | GRP-15 |
| Semantics of leaving a community (including whether the announcement group can be left separately) | FEED-37 | GRP-15 |
| Scope of group messages readable by a bot (including AI) that joins a group as a member | BOT-22 | AI-16, AI-02 |
| Background updates for real-time location and the required location authorization (including authorization scope) | RICH-39 | DISC-05 |
| What real-time location sharing recipients can see during sharing, after it ends, and after leaving the group | RICH-40 | RICH-41 |
| In-place risk prompts (including payment recipient, risky links, impersonating accounts) | SAFE-14 | PAY-14, RICH-36, BOT-07, BOT-31, WAL-17 |
| How prompts for rate limits and limit hits are written | SAFE-13 | PAY-15, PAY-05, PAY-28, AI-09, INV-09, INV-14, WAL-16, ENF-21, SUP-03 |
| Layering of notification toggles for feed post and story interaction alerts | NOTI-01 | FEED-28 |
| Asset handling at account deletion (wallet balance and unfinished payments, points, remaining membership period, combined into one question) | WAL-18 | module 01 Must-ask states row "account deletion"; module 14 Must-ask states row "regulated fund flow · counterparty" (pending receipts when the other party deletes their account); AGE-11, PRIV-24, ACC-21, PTS-15, PTS-22; module 24 Must-ask states row "account" |
| What the payer sees when the wallet is restricted or frozen | WAL-22 | PAY-08, ENF-20; module 14 Must-ask states row "regulated fund flow · counterparty" |
| Whether fund capabilities are usable before identity verification is complete (block, or give an unverified quota) | WAL-01 | PAY-22 |
| Prompt and toggle after a contacts-matched contact registers | REL-04 | DISC-12, INV-05 |
| Validity period and reset of the personal QR code | DISC-14 | INV-07 |
| Contacts upload method (including whether plaintext numbers are stored) | DISC-18 | INV-08 |
| Sending invitations to unregistered contacts (SMS or share) and handling of their numbers | INV-22 | INV-03 |
| What the web landing page shows when an external link is opened in an environment without the app installed or signed in | INV-26 | INV-04 (landing pages for group invite links and feed/channel external links follow this entry too) |
| Ad labeling and advertiser visibility (including each ad slot) | ADS-01 | — (no referencing entries yet) |
| Distinguishing chat list ad entries from normal chats (unread, badge count, push, search, chat operations) | ADS-07 | LIST-20, NOTI-07, MISC-01 |
| Default for personalized ads and personalized content recommendations | ADS-14 | PRIV-26 |
| Data scope usable for ad and recommendation targeting (whether chat content is used) | ADS-15 | PRIV-26 |
| Ads and personalized recommendations for minor accounts | ADS-17 | AGE-20; AGE-07 (the "ads and personalized recommendations" clause of the tightening dimension) |
| Details of account restriction and ban (enforcement ladder, restriction prompts and release time, appeal flow, disclosure of reasons) | ENF-01 | ACC-11 |
| Generic ticket state machine for feedback, appeals and disputes (state set, needs more info, closure and reopen after resolved, user withdrawal) | SUP-10 | SAFE-12, ENF-10, ENF-11, ENF-12, ENF-13, WAL-07; module 22 Must-ask states row "stacked and changed enforcement actions" |
| Basis of ticket processing-time commitments (start point, working days, pause timing while needs more info, timeout presentation; whether a penalty appeal commits belongs to ENF-12, same basis as this entry) | SUP-13 | WAL-07, ENF-12 |
| Distinguishing auto-reply from human support (the form of the label and the "transfer to human" entry itself) | BOT-29 | SUP-07, SUP-15 |
| Trigger, continuation and conversion to a message ticket for bot support handoff to a human (does not define the entry form) | SUP-15 | BOT-29 |
| Account deletion method (immediate deletion, cooling-off period, or tiered by risk) | ACC-21 | DISC-11, WAL-08, INV-14, PRIV-24, WAL-18 |
| Data already uploaded after contacts sync is turned off | DISC-21 | PRIV-13, PRIV-16, PRIV-01 |
| Deletion of conversations with AI and the associated memory | AI-10 | PRIV-16 |
| Security cooldown and all-device reminder for data export | MISC-30 | PRIV-07 |
| Where chat content is processed when handed to translation and AI services | AI-12 | PRIV-25 |
| Whether content submitted to AI is used for training | AI-13 | PRIV-25 |
| Retention and visibility of age confirmation data | AGE-10 | PRIV-27 |
| Consent form after terms and privacy policy updates | PRIV-10 | — (no referencing entries yet) |
| Account handling after re-consent is refused | PRIV-11 | — (no referencing entries yet) |
| Handling of already collected data after consent is withdrawn (contacts excepted, belongs to DISC-21) | PRIV-13 | DISC-21, ADS-16 |
| Export scope of "Download My Data" (whether it includes chat history) | PRIV-14 | — (no referencing entries yet) |
| Category deletion without account deletion (deletion scope) | PRIV-16 | — (no referencing entries yet) |
| Handling of the user's own sent content on others' side after account deletion | PRIV-17 | module 01 Must-ask states row "account deletion" |
| Handling of failed points reward grants (invites, tasks, check-in and others on the same basis; the body already covers all three) | INV-17 | PTS-10 |
| Clawback scope after a points reward is judged as cheating (invites, tasks, check-in and others; handled separately with and without a lock period) | INV-18 | PTS-10 |
| Whether points are tied to cash (fund actions awarding points, buying points with cash, points offsetting cash, redeeming cash-type benefits) and its feasibility (including invite and task rewards paying cash or wallet balance directly) | PTS-13 | INV-10, INV-11 |
| Points and remaining membership period during permanent ban and restriction (account deletion belongs to WAL-18) | PTS-22 | ENF-14, PTS-15; module 24 Must-ask states row "account" |
| Existing content exceeding the free cap after membership expires | PTS-25 | MEDIA-15, MISC-16, LIST-01, GRP-16, RICH-52 |
| Time zone basis of rule-type times (day rollover, count reset, expiry date, release time, processing deadline cutoff) | UX-36 | PTS-05, PTS-16, PTS-17, ENF-07, ADS-09, WAL-06, SUP-13 |
| Withdrawing consent item by item inside the app (entry form) | PRIV-28 | PRIV-01 |
