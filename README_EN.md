<p align="center"><strong>Independent student project by a BUPT AI student</strong> · Follow for updates and collaboration</p>
<p align="center"><a href="README.md">简体中文</a> · <a href="README_EN.md">English</a></p>

<h1 align="center">SaveMyOops · 补锅侠</h1>

<p align="center"><strong>Pause, protect what can still be protected, and choose a low-risk next step.</strong></p>
<p align="center">An AI assistant skill for mis-sent messages, deleted or overwritten files, missed deadlines, and order or appointment mistakes. Use it with any assistant that supports Agent Skills, or provide the files as ordinary context.</p>
<p align="center"><img alt="Validate Skill: passing" src="https://img.shields.io/badge/Validate%20Skill-passing-brightgreen"> <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow"></p>

If it helps you avoid a second mistake or preserve a recovery option, consider giving the project a ⭐ Star or following for updates. No star count is displayed here.

## What it helps with

| Situation | How SaveMyOops helps |
| --- | --- |
| You sent a message to the wrong person or group | Checks whether a reversible correction is available, then helps draft a clear factual follow-up. |
| You deleted or overwrote a file | Prioritizes preserving the device and checking existing trash, version history, or backups before risky recovery attempts. |
| You missed a deadline | Separates the published deadline, your timeline, and unknown exceptions; drafts a concise request for clarification. |
| An order or appointment went wrong | Verifies the order/booking status and the service’s current official process before suggesting another action. |

## Install

Give this instruction to your AI assistant:

```text
Install the public repository https://github.com/yifanchen12/save-my-oops as an Agent Skill. Keep its SKILL.md and references together.
```

If your assistant does not support skill installation, download the repository and provide `SKILL.md` plus the relevant reference page as context.

Try:

```text
Use SaveMyOops. I overwrote a document about ten minutes ago. Help me protect the current state and check the lowest-risk recovery options. Do not change files automatically.
```

## A typical answer

1. **Time-sensitive or irreversible risk** — what could disappear or become harder to reverse.
2. **Evidence** — the message, alert, order confirmation, file history, or deadline text you provided.
3. **Unknowns** — platform version, account type, recipient state, backup status, and policy details that need checking.
4. **Low-risk next step** — preserve the current state and verify the official process.
5. **Optional draft** — a short correction or request that you review and send yourself.

The included triage script labels risk from explicit inputs only. It does not access your device, contact anyone, restore files, cancel orders, or submit appeals.

## Reference library

The knowledge base contains **100 references** across file recovery, platform messaging, account security, incident response, consumer processes, and communication research. Platform help pages and recovery windows change; verify the current instructions for your account, device, and version before acting.

- [Knowledge base guide](references/knowledge/README.md)
- [Core 100-item source index](references/knowledge/来源索引.md)
- [File protection and recovery](references/knowledge/误删覆盖后的文件保护与恢复.md)
- [Message correction and repair](references/knowledge/消息更正与关系补救.md)
- [Deadlines, orders, and appointments](references/knowledge/截止时间订单预约核验.md)

## Limits and privacy

- It cannot guarantee file recovery, an extension, a refund, a booking change, or forgiveness.
- Software menus and platform rules differ by version, region, account, and plan. Check the official source before acting.
- It does not automatically delete, overwrite, recall, cancel, pay, send, or submit anything.
- Share only the excerpt needed. Remove names, contact details, addresses, account identifiers, and private content first.
- If an incident involves account takeover, financial loss, threats, or immediate safety concerns, contact the relevant official provider or local support channel promptly.

## Development and license

Run the validator and triage tests with Python 3:

```bash
python tests/validate_skill.py
python -m unittest discover -s tests -p "test_*.py" -v
```

MIT License. See [LICENSE](LICENSE).
