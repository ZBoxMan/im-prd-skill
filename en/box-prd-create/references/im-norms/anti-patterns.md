# IM Cross-Module Anti-Pattern Table

> For the closing self-check: after finishing a draft, compare against each row and fix any hit. Module-specific anti-patterns are at the end of each module file; this table holds only cross-module problems that keep recurring.

## Contents
- States and terminal states
- Multi-device, offline and timing
- Relations, permissions and privacy
- Groups and one-on-one chats
- Feedback and copy
- Funds, location, content leaving the app and third-party reads
- Using the norms library

## States and terminal states

| Vague/wrong | Correct | Reason |
|---|---|---|
| Draws only icons and defines no state machine, e.g. "send status: single check, double check" | Give each state a one-line meaning first, then its entry condition, exit condition and terminal state; say whether failure is terminal or retryable | Icons are presentation; the state machine is what engineering implements |
| Writes only the success path | Cover at least five exits: waiting on the server, recoverable failure, blocked, timeout, unknown result | Most copy in mainstream products is spent on failures and edge cases |
| One line "Operation failed, please retry" covers every failure | Give separate copy and destination for network failure, insufficient permission, object no longer valid, and rate limit | Different causes call for different remedies |
| Can open but not close, can send but not unsend, can enter but not leave | Pair every "create" with a path to undo, view or exit; if none is offered, state "not provided" | A broken loop is a one-vote veto |
| Async action has no intermediate state | Specify how the waiting state looks, whether it can be canceled, and the state after canceling | On weak networks the intermediate state lasts seconds to minutes |
| Report, appeal, wallet dispute and feedback each define their own state names and flow, and some notify on result while others do not | Map all of them to the common support-ticket state machine; define supplement, reopen, withdraw and result notification once; each type only adds entry point, eligibility, count and time limit (see SUP-10, SUP-04) | Users see different names at different entry points, engineering implements twice, and states and notifications contradict each other |

## Multi-device, offline and timing

| Vague/wrong | Correct | Reason |
|---|---|---|
| Considers only the current device | State the behavior on the account's other devices: whether read, unsent, deleted and setting changes sync, and how fast | Multi-device is a default capability of mainstream products |
| Assumes the recipient is online | State what an offline recipient sees on coming online, and whether the push already showed the original content | Unsend, edit and delete break most easily at an offline recipient |
| Orders messages by local time | State the ordering basis and the send order of messages queued offline once the network returns | Local time is untrustworthy; out-of-order delivery changes meaning |
| "Messages before the block are still delivered" or "cannot unsend after the timeout" state only the result | State the cutoff basis: server receive time or client send time, and which device prevails across devices | If the cutoff basis is not written, each side implements its own and boundary messages behave inconsistently |
| "Real-time updates" | Write four phases: trigger, refresh, stop, reopen (the four-phase form for signaling rules) | "Real-time" cannot be implemented uniquely |
| Ignores the object being changed by someone else during the user's operation | Write mid-operation changes: the other party unsends, is removed from the group, has permission revoked, or the chat is cleared | Concurrency is the norm in IM |

## Relations, permissions and privacy

| Vague/wrong | Correct | Reason |
|---|---|---|
| Does not define behavior for blocked, deleted-account or non-contact objects | Every feature involving "the other party" states the send result and prompt for these three kinds of object | Relation state changes the capability boundary |
| A privacy switch says only "can be turned off" | State the default value, the range tiers, and the reciprocity rule after turning off (if I turn it off, can I also no longer see others') | The default value decides the experience of most users |
| The blocked party gets an explicit "you have been blocked" feedback | Whether to reveal the block to the blocked party is a divergence for Box to rule on | Revealing or not is a privacy trade-off; mainstream products differ |
| Permission says only "admins can" | State the permission item list, who can grant, whether same-level or higher roles can be acted on, and how in-progress operations are handled when permission is revoked | Permission conflicts are a frequent defect source in group features |
| Withdrawing consent, turning off sync or turning off personalization says only "turned off" | State the feature's state after withdrawal, and whether already-collected data stops being processed, is deleted, or is left to the user to choose (see PRIV-13; for the address book see DISC-21) | Users believe the data is deleted while it remains on the server, which is misleading disclosure |
| Strangers and contacts get the same capabilities | State limits on a stranger's first contact, high-disturbance actions unavailable before acceptance, and the decline and report entry points | Stranger reachability decides the harassment surface |
| An account with unconfirmed age says only "some features restricted" | List item by item what is restricted (stranger contact, default feed audience, payment and account opening, age-restricted content, personalized recommendation), whether the entry is hidden or prompts on tap, and how to lift it (see AGE-07, AGE-02) | Each module reads "restricted" its own way, and users do not know how to lift it |

## Groups and one-on-one chats

| Vague/wrong | Correct | Reason |
|---|---|---|
| Writes one-on-one rules and assumes groups are the same | State item by item the differences between groups and one-on-one chats, or explicitly "same as one-on-one" | Receipts, unsend, notifications and @ commonly differ in groups |
| Group size has only one cap | Write rules by size tier, with all tiers on the same card | Receipts, notifications and invitation rules usually degrade in large groups |
| No handling of history and entry points after leaving, being removed, or group dissolution | State whether history is kept, whether posting is still possible, how the chat list displays it, and whether rejoining is possible | The state after membership ends is the one most easily missed |
| System messages written casually | Give the verbatim text of system messages for group info changes, member changes and permission changes, and state who sees them | System messages are the factual record in a group |

## Feedback and copy

| Vague/wrong | Correct | Reason |
|---|---|---|
| "Prompt the user" | State the carrier (toast / dialog / inline hint / banner / system message) and the verbatim copy | The carrier decides whether it interrupts and whether it can be undone |
| Dangerous action completes in one step | Delete, leave, dissolve, clear and block go through a second confirmation whose copy states the scope and whether it can be restored | Irreversible actions must be predictable |
| Unsend and delete use the same word | Use different words, entry points and confirmations for "delete for me only" and "unsend for everyone" | Users will assume the other party's copy is also deleted |
| Count says only "show the number" | State the counting basis, how the cap is displayed, conditions under which it is not cleared, and whether muted chats are counted | The counting basis is a frequent dispute for badge counts and unread |
| Penalty or restriction prompt says only "account restricted", with no appeal entry or deadline | State the restricted scope, features still usable, the lift time or "permanent", the appeal entry and the appeal deadline (see ENF-01, ENF-02, ENF-07; for wallet restriction see WAL-21) | Users cannot tell when it will be restored or how to seek remedy, and only probe repeatedly and contact support |
| Ad or recommendation items inserted into the chat list or feed are treated as ordinary items | State that they carry an ad label, do not count toward unread or badge count, do not trigger push, do not appear in search, and do not respond to chat actions (see ADS-01, ADS-07) | Unread, badge and search bases get polluted, and users cannot tell "someone is looking for me" |

## Funds, location, content leaving the app and third-party reads

| Vague/wrong | Correct | Reason |
|---|---|---|
| Payment and split states are mixed into one "paid/unpaid" set | Label each state first as "regulated fund flow" or "bookkeeping": fund flow follows licensed-institution confirmation and the card only maps it; bookkeeping is editable and deletable and moves no money | The two kinds differ in authoritative source, rewritability and regulatory responsibility; mixing them muddles reconciliation |
| Feed posts and stories are visible to everyone by default, regardless of account age | State the default audience and show the current audience explicitly on the publish page; accounts of minors or without completed age confirmation get tighter tiers (age basis: see AGE-07) | The default value decides the exposure of most content, and launch regions usually have compliance requirements for minor accounts |
| Chat content is handed to translation, AI or a bot without notice | State the first-use notice, the content scope submitted at each entry point, where it is processed, whether it is used for training, and availability in encrypted chats | When others' messages are sent out, the original sender cannot know, and the encryption promise may be defeated |
| Real-time location says only "start sharing" | State the limited-duration tiers, automatic end on expiry, manual stop and "stop all", and what the other party sees after it ends | Without expiry or a single stop entry, users forget they are still sharing their whereabouts |
| Account or wallet deletion says only "data is deleted after deletion" and does not handle balances | State whether balance, in-progress withdrawals, pending collections and unresolved disputes block or are routed, whether points and remaining membership period are voided, and provide withdrawal and statement-download entries before deletion (see WAL-18, WAL-20) | Funds do not vanish with the account; "where does the money go after deletion" is a frequent complaint |
| "Bots can read group messages" defines no scope | State the default read scope (only what concerns it, or everything), who can widen it, and where members can see the read scope | The read scope in a group concerns the privacy of all members, not only the person who added the bot |
| Sending images or links states only the content itself | State whether metadata such as the capture location of images is stripped, who fetches link previews, and whether they are generated by default | Embedded metadata and preview fetching leak location and URLs without the user's knowledge |
| Writes "recharge to get points", "buy points with cash", "points offset cash", "redeem for phone credit or balance" without marking feasibility | When tied to cash, the corresponding money action is handled as a regulated fund flow; write feasibility as {TBC} merged with the licensed-institution item, and for the refund path of the cash part see PAY-21; the points themselves remain bookkeeping (see PTS-13) | Points may be deemed a stored-value or payment instrument, bypassing fund compliance and refund rules |
| Invitation reward says only "enter an invite code, both sides get points" | State the grant condition and timing, lock period, usage cap, self-invite detection, grant failure and revocation (see INV-11, INV-14 to INV-18) | If the reward rules are not complete, it is farmed as soon as it launches |

## Using the norms library

| Vague/wrong | Correct | Reason |
|---|---|---|
| Writes a `Level: Must-ask` divergence into the card per recommendation, or puts it under "Defaulted to recommendation" | Handle by the level at the end of the entry: `Must-ask` goes to Box first and the card carries `{TBD: topic, recommended: approach}`; `Default-OK` is written into the card per recommendation and listed under "Defaulted to recommendation" | Must-ask items involve privacy, irreversible handling or main-flow direction; the recommendation is only a suggestion |
| Leaves `{TBD}` on a `Default-OK` divergence or convention | Write the recommended value or a value within the magnitude directly, and list one line under "Defaulted to recommendation" | Too many placeholders block the write gate and waste Box's attention |
| Copies the numbers in the norms library magnitudes | Values are set by ZYMIX business; the magnitude is only used to judge whether a value is off the charts | 2026-09-15 ruling: do not copy competitor numbers |
| Writes "same as mainstream products" on the card instead of the rule | Write the rule itself in full; if needed add one line under `Note:` such as "same as mainstream instant-messaging products" (a rewording Box approved) | Developers cannot see the norms library; the card must be self-contained |
| Writes norms-library IDs on the annotation card | IDs are used only inside the skill, reviews and evals | Rule IDs on the canvas have been retired |
| Writes values that only a licensed institution, regulator or engineering can answer (limits, fees, settlement time, open regions, whether funds can be frozen in transit) as `{TBD}` and asks Box | Write `{TBC: what is missing}` into open items, merging multiple items for the same answering party into one group; leave only product trade-offs to Box | Box cannot rule on these, it uses up the question budget, and the card has to be changed again after the answer |
| For an entry whose recommendation is "follow existing ZYMIX rules", leaves `{TBD}` and asks even though the source of truth already has the answer | Check the source of truth first; if found, write it as body text per the source of truth, and the card may note "per current terms" | Wastes Box's attention, and the same fact may appear in two forms across requirements |
