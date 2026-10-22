#!/usr/bin/env python3
"""Deterministic, non-destructive first-response triage for everyday mistakes."""

from __future__ import annotations

import json
import sys
from typing import Any


class InputError(ValueError):
    """Raised when the triage request is malformed."""


BASE_ACTIONS = {
    "message_sent": "先暂停连发；确认收件人、已发送内容和对方是否已读，再决定是否发一条简短更正。",
    "file_deleted": "先停止在受影响位置写入新内容；检查回收站、云端版本记录或备份。确认设备和软件前，不运行清理或恢复写回操作。",
    "file_overwritten": "保留当前文件副本并记录覆盖时间；先查看版本历史/备份，再选择可撤回的恢复方式。不要直接覆盖现有副本。",
    "deadline_missed": "先确认截止规则和当前状态；尽早联系负责方说明事实、询问补交或延期途径，并保留沟通记录。",
    "order_error": "先核对订单状态、金额和商家规则；若涉及重复扣款或取消时限，联系官方客服并保存订单凭证。不要重复付款。",
    "appointment_error": "先核对预约编号、时间、地点和取消/改期规则；联系官方渠道确认更改是否成功，并保留确认信息。",
    "unknown": "先描述已经发生的事、涉及的对象/账户，以及接下来最早的截止时间；在查明前避免删除、重试付款或重复发送。",
}


def _flag(data: dict[str, Any], key: str) -> bool | None:
    value = data.get(key)
    if value is not None and not isinstance(value, bool):
        raise InputError(f"{key} 必须是 true、false 或省略表示未知")
    return value


def triage(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise InputError("输入必须是 JSON 对象")
    incident = data.get("incident")
    if incident not in BASE_ACTIONS:
        raise InputError(f"incident 必须是以下之一：{', '.join(BASE_ACTIONS)}")

    time_sensitive = _flag(data, "time_sensitive")
    irreversible = _flag(data, "irreversible")
    platform_unknown = _flag(data, "platform_or_version_unknown")
    if time_sensitive is None or irreversible is None:
        level = "待确认"
        rationale = "时间窗口或可撤回性尚未确认；先保留现状，不执行难以撤回的操作。"
    elif time_sensitive and irreversible:
        level = "高"
        rationale = "同时存在时间敏感与难以撤回的风险，先保护现状并尽快联系有权处理的一方。"
    elif time_sensitive or irreversible:
        level = "中"
        rationale = "存在一项需要优先确认的风险；采取可逆动作并尽快核实关键事实。"
    else:
        level = "低"
        rationale = "当前提供的信息未显示紧迫或不可逆风险；先核实情况，再采取小步可撤回的处理。"

    next_step = BASE_ACTIONS[incident]
    if level == "高":
        next_step += " 现在先保存截图、编号、时间等凭证；如有截止窗口，优先联系官方负责方。"
    if platform_unknown:
        next_step += " 平台或版本尚未确认，因此不提供具体按钮路径；先核实应用名称、版本和设备。"

    return {
        "incident": incident,
        "risk_level": level,
        "time_sensitive": time_sensitive,
        "hard_to_reverse": irreversible,
        "reason": rationale,
        "first_step": next_step,
        "platform_verification_required": platform_unknown,
        "execution": "仅提供建议；没有执行任何发送、删除、恢复、取消、付款或预约操作。",
        "need_to_confirm": ["实际状态与关键时间", "操作是否已经生效"] + (["是否存在临近截止时间"] if time_sensitive is None else []) + (["操作是否可撤回"] if irreversible is None else []) + (["应用/平台名称、版本与设备"] if platform_unknown else []),
    }


def main() -> int:
    try:
        result = triage(json.load(sys.stdin))
    except (InputError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
