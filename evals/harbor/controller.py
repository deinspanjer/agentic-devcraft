import asyncio
import re
import time
from collections.abc import Awaitable, Callable
from typing import Any


class ControllerError(ValueError):
    pass


def build_request(
    policy: str | dict[str, Any],
    transcript: list[dict[str, str]],
    turn: int,
    max_turns: int,
    *,
    stage: str | None = None,
    observation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    request = {
        "policy": policy,
        "transcript": [dict(item) for item in transcript],
        "interaction_turn": turn,
        "max_interaction_turns": max_turns,
    }
    if isinstance(policy, dict):
        request.update(stage=stage, observation=observation or {})
    return request


def _available_policy(policy: dict[str, Any], stage: str | None) -> dict[str, Any]:
    return {
        "version": policy.get("version"),
        "progress": policy.get("progress"),
        "answers": [
            answer
            for answer in policy.get("answers", [])
            if stage in answer.get("stages", [])
        ],
        "stop_reasons": policy.get("stop_reasons", []),
    }


def validate_decision(
    value: Any,
    *,
    policy: dict[str, Any] | None = None,
    stage: str | None = None,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ControllerError("decision must be an object")

    if policy is not None:
        available = _available_policy(policy, stage)
        action = value.get("action")
        basis_ids = value.get("basis_ids")
        if not isinstance(basis_ids, list) or not all(
            isinstance(item, str) and item for item in basis_ids
        ):
            raise ControllerError("scenario decision requires basis_ids")
        if action == "message" and set(value) == {
            "action",
            "category",
            "basis_ids",
            "message",
        }:
            category = value.get("category")
            message = value.get("message")
            if category == "material_answer" and len(basis_ids) == 1:
                answer = next(
                    (item for item in available["answers"] if item["id"] == basis_ids[0]),
                    None,
                )
                if answer is not None and message == answer["message"]:
                    return value
            if category == "progress" and len(basis_ids) == 1:
                progress = available.get("progress") or {}
                if basis_ids == [progress.get("id")] and message == progress.get("message"):
                    return value
            raise ControllerError("scenario message is not supported by available policy")
        if action == "complete" and set(value) == {"action", "basis_ids", "reason"}:
            if not basis_ids and isinstance(value.get("reason"), str) and value["reason"].strip():
                return value
        if action == "stop" and set(value) == {"action", "basis_ids", "reason"}:
            if not basis_ids and value.get("reason") in available["stop_reasons"]:
                return value
        raise ControllerError("invalid scenario decision")

    action = value.get("action")
    if action == "message" and set(value) == {"action", "message"}:
        message = value.get("message")
        if isinstance(message, str) and message.strip():
            return {"action": action, "message": message}
    elif action == "stop" and set(value) == {"action", "reason"}:
        reason = value.get("reason")
        if isinstance(reason, str) and reason.strip():
            return {"action": action, "reason": reason}

    raise ControllerError("decision must be a non-empty message or stop object")


def _question_key(response: str) -> str | None:
    questions = [
        re.sub(r"\s+", " ", line.strip().lower())
        for line in response.splitlines()
        if "?" in line
    ]
    return "\n".join(questions) if questions else None


async def drive_conversation(
    *,
    policy: str | dict[str, Any],
    transcript: list[dict[str, str]],
    decide: Callable[[dict[str, Any]], Awaitable[Any]],
    send: Callable[[str], Awaitable[str]],
    max_turns: int,
    timeout_sec: float,
    stage: str | None = None,
    observe: Callable[[], Awaitable[dict[str, Any]]] | None = None,
    max_reported_tokens: int | None = None,
    max_repeated_questions: int = 3,
    transcript_start: int = 0,
) -> dict[str, Any]:
    if (
        max_turns < 1
        or timeout_sec <= 0
        or max_repeated_questions < 1
        or transcript_start < 0
        or transcript_start > len(transcript)
    ):
        raise ValueError("max_turns and timeout_sec must be positive")

    started = time.monotonic()
    interaction_turns = sum(
        item["role"] == "agent" for item in transcript[transcript_start:]
    )
    result: dict[str, Any] = {
        "interaction_turns": interaction_turns,
        "termination": None,
        "reason": None,
        "tester_requests": [],
        "decisions": [],
        "observations": [],
    }
    question_counts: dict[str, int] = {}

    while interaction_turns < max_turns:
        observation = await observe() if observe is not None else None
        if observation is not None:
            result["observations"].append(observation)
            if observation.get("contamination"):
                result.update(
                    termination="setup_contamination",
                    reason="undeclared subject-visible state",
                )
                return result
            if observation.get("unsafe_authority"):
                result.update(
                    termination="unsafe_authority",
                    reason=str(observation["unsafe_authority"]),
                )
                return result
            reported = observation.get("reported_output_tokens")
            if (
                max_reported_tokens is not None
                and isinstance(reported, int)
                and reported > max_reported_tokens
            ):
                result.update(termination="token_limit", reason="reported token limit reached")
                return result
        available = _available_policy(policy, stage) if isinstance(policy, dict) else policy
        request = build_request(
            available,
            transcript,
            interaction_turns,
            max_turns,
            stage=stage,
            observation=observation,
        )
        result["tester_requests"].append(request)
        remaining = timeout_sec - (time.monotonic() - started)
        if remaining <= 0:
            result.update(
                termination="time_limit" if isinstance(policy, dict) else "timeout",
                reason="conversation timeout",
            )
            return result

        raw_decision = None
        try:
            raw_decision = await asyncio.wait_for(decide(request), timeout=remaining)
            decision = validate_decision(
                raw_decision,
                policy=policy if isinstance(policy, dict) else None,
                stage=stage,
            )
        except TimeoutError:
            result.update(
                termination="time_limit" if isinstance(policy, dict) else "timeout",
                reason="testing agent timeout",
            )
            return result
        except Exception as exc:
            if isinstance(exc, ControllerError):
                result["decisions"].append(
                    {"rejected": raw_decision, "error": str(exc)}
                )
            result.update(
                termination="controller_error",
                reason=type(exc).__name__,
            )
            return result

        result["decisions"].append(decision)
        if decision["action"] == "complete":
            result.update(termination="completed", reason=decision["reason"])
            return result
        if decision["action"] == "stop":
            termination = (
                decision["reason"]
                if isinstance(policy, dict)
                else "stopped"
            )
            result.update(termination=termination, reason=decision["reason"])
            return result

        transcript.append({"role": "user", "content": decision["message"]})
        remaining = timeout_sec - (time.monotonic() - started)
        if remaining <= 0:
            result.update(
                termination="time_limit" if isinstance(policy, dict) else "timeout",
                reason="conversation timeout",
            )
            return result

        try:
            response = await asyncio.wait_for(send(decision["message"]), remaining)
        except TimeoutError:
            result.update(
                termination="time_limit" if isinstance(policy, dict) else "timeout",
                reason="agent timeout",
            )
            return result
        except Exception as exc:
            result.update(termination="controller_error", reason=type(exc).__name__)
            return result

        transcript.append({"role": "agent", "content": response})
        interaction_turns += 1
        result["interaction_turns"] = interaction_turns
        if question := _question_key(response):
            question_counts[question] = question_counts.get(question, 0) + 1
            if question_counts[question] >= max_repeated_questions:
                result.update(
                    termination="repeated_question",
                    reason="same question repeated",
                )
                return result

    result.update(
        termination="turn_limit", reason="maximum interaction turns reached"
    )
    return result
