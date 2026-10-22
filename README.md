# 补锅侠 · SaveMyOops

遇到消息发错、文件误删/覆盖、错过截止时间、订单或预约出错时，先判断风险，再找到一个低风险、可撤回的第一步。

Skill 会把已知事实、推断与未知项分开；涉及平台版本、设备或规则时会要求核实，不会假定某个按钮一定存在。它只给建议和可选草稿，不会代替你发送消息、删文件、恢复版本、付款、取消或提交表单。

## 适用场景

- 发错消息、错群，或需要为不当措辞道歉。
- 误删、覆盖文件，想判断接下来如何保护恢复机会。
- 错过作业、申请、付款或工作截止时间。
- 订单重复、金额异常、取消/退款状态不清。
- 预约的时间、地点或服务状态有误。

## 安装

将整个 `save-my-oops` 文件夹复制到 Codex skills 目录，然后重新打开 Codex：

- Windows：`%USERPROFILE%\.codex\skills\save-my-oops`
- macOS / Linux：`~/.codex/skills/save-my-oops`

调用示例：

```text
使用 $save-my-oops。我把文件覆盖了，电脑是 Windows，但不知道软件版本。先帮我判断风险和现在最安全的一步，不要建议会覆盖现有文件的操作。
```

## 示例

`examples/input.json` 与 `examples/output.json` 展示了订单窗口临近、结果难以撤回、平台版本未知的高风险分流。脚本只打风险标签和建议，不会操作订单或设备。

本地分流：

```bash
python scripts/triage.py < examples/input.json
```

PowerShell 可用：

```powershell
Get-Content -Raw examples/input.json | python scripts/triage.py
```

合法 `incident` 类型为 `message_sent`、`file_deleted`、`file_overwritten`、`deadline_missed`、`order_error`、`appointment_error` 和 `unknown`。其余布尔字段见示例与脚本。

## 验证

```bash
python -m unittest discover -s tests -v
python tests/validate_skill.py
```

`tests/cases.json` 有 12 个正常、信息不足、边界和安全案例。

## 局限与隐私

- 不访问设备、邮箱、聊天应用或商家账户，不联网查询平台规则，也不能确认消息已读、文件可恢复、退款到账或申诉获批。
- 具体版本、地区和账户规则会变化；先核实官方页面/支持渠道，不依据旧版按钮路径操作。
- 不要发送密码、验证码、支付卡完整信息或身份证完整号码；必要时用遮挡后的截图。
- 随附脚本在本地运行，不联网、不保存输入。高价值文件、账户接管、人身安全或大额资金问题，应尽快联系可信支持或官方/专业渠道。

## 发布到 GitHub

可以把此目录作为独立仓库根目录发布。创建公开仓库 `save-my-oops` 后，将目录内容推送到仓库根目录；请勿提交真实聊天、凭证或个人文件。

## 许可

本 Skill 采用 MIT License，详见 `LICENSE`。
