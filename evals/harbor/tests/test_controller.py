import asyncio
import unittest

from evals.harbor.controller import ControllerError, drive_conversation, validate_decision


class ControllerTest(unittest.IsolatedAsyncioTestCase):
    async def test_blinds_request_and_stops(self):
        seen = []

        async def decide(request):
            seen.append(request)
            return {"action": "stop", "reason": "done"}

        result = await drive_conversation(
            policy="inspect the response",
            transcript=[{"role": "agent", "content": "ready"}],
            decide=decide,
            send=lambda _: None,
            max_turns=2,
            timeout_sec=1,
        )

        self.assertEqual(result["termination"], "stopped")
        self.assertEqual(set(seen[0]), {"policy", "transcript", "turn", "max_turns"})
        self.assertNotIn("arm", repr(seen[0]).lower())
        self.assertNotIn("expected", repr(seen[0]).lower())

    async def test_enforces_turn_limit(self):
        async def decide(_):
            return {"action": "message", "message": "continue"}

        async def send(_):
            return "continued"

        result = await drive_conversation(
            policy="continue",
            transcript=[{"role": "agent", "content": "ready"}],
            decide=decide,
            send=send,
            max_turns=2,
            timeout_sec=1,
        )

        self.assertEqual(result["termination"], "turn_limit")
        self.assertEqual(result["turns"], 2)

    async def test_stage_local_turn_count_keeps_prior_transcript_as_context(self):
        async def decide(request):
            self.assertEqual(len(request["transcript"]), 4)
            self.assertEqual(request["turn"], 1)
            return {"action": "stop", "reason": "done"}

        result = await drive_conversation(
            policy="continue",
            transcript=[
                {"role": "user", "content": "old"},
                {"role": "agent", "content": "old answer"},
                {"role": "user", "content": "new"},
                {"role": "agent", "content": "new answer"},
            ],
            transcript_start=2,
            decide=decide,
            send=lambda _: None,
            max_turns=2,
            timeout_sec=1,
        )
        self.assertEqual(result["termination"], "stopped")

    async def test_reports_timeout(self):
        async def decide(_):
            await asyncio.sleep(1)

        result = await drive_conversation(
            policy="wait",
            transcript=[{"role": "agent", "content": "ready"}],
            decide=decide,
            send=lambda _: None,
            max_turns=2,
            timeout_sec=0.01,
        )

        self.assertEqual(result["termination"], "timeout")

    async def test_reports_controller_error(self):
        async def decide(_):
            return {"action": "unexpected"}

        result = await drive_conversation(
            policy="fail",
            transcript=[{"role": "agent", "content": "ready"}],
            decide=decide,
            send=lambda _: None,
            max_turns=2,
            timeout_sec=1,
        )

        self.assertEqual(result["termination"], "controller_error")
        self.assertEqual(
            result["decisions"],
            [
                {
                    "rejected": {"action": "unexpected"},
                    "error": "decision must be a non-empty message or stop object",
                }
            ],
        )

    async def test_scenario_filters_policy_and_accepts_only_cited_answers(self):
        policy = {
            "version": "v1",
            "progress": {"id": "progress", "message": "status"},
            "answers": [
                {"id": "initial-answer", "stages": ["initial"], "message": "visible"},
                {"id": "later-answer", "stages": ["extension"], "message": "future"},
            ],
            "stop_reasons": ["scenario_gap"],
        }
        seen = []

        async def decide(request):
            seen.append(request)
            return {
                "action": "message",
                "category": "material_answer",
                "basis_ids": ["initial-answer"],
                "message": "visible",
            }

        async def send(_):
            return "done"

        result = await drive_conversation(
            policy=policy,
            transcript=[{"role": "agent", "content": "question?"}],
            decide=decide,
            send=send,
            max_turns=2,
            timeout_sec=1,
            stage="initial",
        )
        self.assertEqual(result["termination"], "turn_limit")
        self.assertEqual([item["id"] for item in seen[0]["policy"]["answers"]], ["initial-answer"])
        self.assertNotIn("future", repr(seen[0]))
        with self.assertRaises(ControllerError):
            validate_decision(
                {
                    "action": "message",
                    "category": "material_answer",
                    "basis_ids": ["later-answer"],
                    "message": "future",
                },
                policy=policy,
                stage="initial",
            )

    async def test_scenario_completion_gap_observation_and_repeated_question_boundaries(self):
        policy = {
            "version": "v1",
            "progress": {"id": "progress", "message": "status"},
            "answers": [],
            "stop_reasons": ["scenario_gap"],
        }

        async def complete(_):
            return {"action": "complete", "basis_ids": [], "reason": "verified"}

        result = await drive_conversation(
            policy=policy,
            transcript=[{"role": "agent", "content": "done"}],
            decide=complete,
            send=lambda _: None,
            max_turns=2,
            timeout_sec=1,
            stage="initial",
        )
        self.assertEqual(result["termination"], "completed")

        async def gap(_):
            return {"action": "stop", "basis_ids": [], "reason": "scenario_gap"}

        result = await drive_conversation(
            policy=policy,
            transcript=[{"role": "agent", "content": "need a choice"}],
            decide=gap,
            send=lambda _: None,
            max_turns=2,
            timeout_sec=1,
            stage="initial",
        )
        self.assertEqual(result["termination"], "scenario_gap")

        async def observe():
            return {"contamination": ["AGENTS.md"]}

        result = await drive_conversation(
            policy=policy,
            transcript=[{"role": "agent", "content": "ready"}],
            decide=complete,
            send=lambda _: None,
            observe=observe,
            max_turns=2,
            timeout_sec=1,
            stage="initial",
        )
        self.assertEqual(result["termination"], "setup_contamination")

        async def token_observation():
            return {"reported_output_tokens": 101}

        result = await drive_conversation(
            policy=policy,
            transcript=[{"role": "agent", "content": "ready"}],
            decide=complete,
            send=lambda _: None,
            observe=token_observation,
            max_turns=2,
            timeout_sec=1,
            stage="initial",
            max_reported_tokens=100,
        )
        self.assertEqual(result["termination"], "token_limit")

        async def unsafe_observation():
            return {"unsafe_authority": "hosted push"}

        result = await drive_conversation(
            policy=policy,
            transcript=[{"role": "agent", "content": "ready"}],
            decide=complete,
            send=lambda _: None,
            observe=unsafe_observation,
            max_turns=2,
            timeout_sec=1,
            stage="initial",
        )
        self.assertEqual(result["termination"], "unsafe_authority")

        async def too_slow(_):
            await asyncio.sleep(1)

        result = await drive_conversation(
            policy=policy,
            transcript=[{"role": "agent", "content": "ready"}],
            decide=too_slow,
            send=lambda _: None,
            max_turns=2,
            timeout_sec=0.01,
            stage="initial",
        )
        self.assertEqual(result["termination"], "time_limit")

        async def progress(_):
            return {
                "action": "message",
                "category": "progress",
                "basis_ids": ["progress"],
                "message": "status",
            }

        async def repeat(_):
            return "Which format?"

        result = await drive_conversation(
            policy=policy,
            transcript=[{"role": "agent", "content": "Which format?"}],
            decide=progress,
            send=repeat,
            max_turns=5,
            timeout_sec=1,
            stage="initial",
            max_repeated_questions=2,
        )
        self.assertEqual(result["termination"], "repeated_question")


if __name__ == "__main__":
    unittest.main()
