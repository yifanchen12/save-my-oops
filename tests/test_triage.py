import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "triage.py"
SPEC = importlib.util.spec_from_file_location("triage", SCRIPT)
triage_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(triage_module)


class TriageTests(unittest.TestCase):
    def test_message_sent(self):
        self.assertIn("暂停连发", triage_module.triage({"incident": "message_sent"})["first_step"])

    def test_deleted_file_preserves_state(self):
        self.assertIn("停止", triage_module.triage({"incident": "file_deleted"})["first_step"])

    def test_overwritten_file_mentions_copy(self):
        self.assertIn("副本", triage_module.triage({"incident": "file_overwritten"})["first_step"])

    def test_deadline_recommends_contact(self):
        self.assertIn("联系", triage_module.triage({"incident": "deadline_missed"})["first_step"])

    def test_order_error_prevents_duplicate_payment(self):
        self.assertIn("不要重复付款", triage_module.triage({"incident": "order_error"})["first_step"])

    def test_appointment_verifies_official_channel(self):
        self.assertIn("官方渠道", triage_module.triage({"incident": "appointment_error"})["first_step"])

    def test_missing_flags_remain_unknown(self):
        result = triage_module.triage({"incident": "unknown"})
        self.assertEqual(result["risk_level"], "待确认")
        self.assertIsNone(result["time_sensitive"])

    def test_explicit_no_risk_flags_are_low(self):
        result = triage_module.triage({"incident": "unknown", "time_sensitive": False, "irreversible": False})
        self.assertEqual(result["risk_level"], "低")

    def test_time_sensitive_only_is_medium(self):
        self.assertEqual(triage_module.triage({"incident": "deadline_missed", "time_sensitive": True, "irreversible": False})["risk_level"], "中")

    def test_irreversible_only_is_medium(self):
        self.assertEqual(triage_module.triage({"incident": "file_deleted", "time_sensitive": False, "irreversible": True})["risk_level"], "中")

    def test_both_risks_are_high_and_preserve_evidence(self):
        result = triage_module.triage({"incident": "order_error", "time_sensitive": True, "irreversible": True})
        self.assertEqual(result["risk_level"], "高")
        self.assertIn("截图", result["first_step"])

    def test_unknown_version_avoids_button_path(self):
        result = triage_module.triage({"incident": "file_deleted", "time_sensitive": False, "irreversible": False, "platform_or_version_unknown": True})
        self.assertTrue(result["platform_verification_required"])
        self.assertIn("不提供具体按钮路径", result["first_step"])

    def test_invalid_incident_rejected(self):
        with self.assertRaises(triage_module.InputError):
            triage_module.triage({"incident": "hack account"})

    def test_non_boolean_flag_rejected(self):
        with self.assertRaises(triage_module.InputError):
            triage_module.triage({"incident": "message_sent", "irreversible": "yes"})

    def test_no_action_is_executed(self):
        self.assertIn("没有执行", triage_module.triage({"incident": "message_sent"})["execution"])


if __name__ == "__main__":
    unittest.main()
