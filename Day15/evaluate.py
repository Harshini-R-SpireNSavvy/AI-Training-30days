#!/usr/bin/env python3
"""
Run 10 benchmark questions; print scores and optionally refresh QUALITY_REPORT.md tables.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from rag_core import IDK_MESSAGE, ask

ROOT = Path(__file__).resolve().parent
CHROMA = ROOT / "chroma_db"
REPORT_PATH = ROOT / "QUALITY_REPORT.md"


@dataclass
class TestCase:
    qid: str
    question: str
    expect_idk: bool
    must_mention: list[str]  # lowercase substrings expected in answer when not IDK
    preferred_sources: list[str]  # filename substrings for citation check


TEST_CASES: list[TestCase] = [
    TestCase(
        "Q1",
        "What nominal DC voltage does Widget X require?",
        False,
        ["12"],
        ["02_product_specs"],
    ),
    TestCase(
        "Q2",
        "How many paid vacation days do full-time employees accrue per year?",
        False,
        ["22"],
        ["01_company_handbook"],
    ),
    TestCase(
        "Q3",
        "What is the API rate limit per minute for the public tier?",
        False,
        ["100"],
        ["05_api_reference"],
    ),
    TestCase(
        "Q4",
        "Within how many minutes must lab spills be reported to the supervisor?",
        False,
        ["15"],
        ["03_safety_guidelines"],
    ),
    TestCase(
        "Q5",
        "What time should a new hire arrive at Building C on their first day?",
        False,
        ["09:00|9:00"],
        ["04_onboarding_faq"],
    ),
    TestCase(
        "Q6",
        "According to the glossary, what does RAG stand for and what does it combine?",
        False,
        ["retrieval", "generation"],
        ["06_glossary"],
    ),
    TestCase(
        "Q7",
        "Is VPN required to access internal APIs from outside the office network?",
        False,
        ["vpn"],
        ["01_company_handbook"],
    ),
    TestCase(
        "Q8",
        "Who won the FIFA World Cup in 2022, and what was the final score?",
        True,
        [],
        [],
    ),
    TestCase(
        "Q9",
        "What is the name of the CEO's pet dog?",
        True,
        [],
        [],
    ),
    TestCase(
        "Q10",
        "What is the maximum container size for flammable solvents allowed on the bench?",
        False,
        ["500"],
        ["03_safety_guidelines"],
    ),
]


def _has_citation(answer: str, sources: list[str]) -> bool:
    if not sources:
        return True
    for s in sources:
        if s in answer:
            return True
    return bool(re.search(r"\[[^\]]+\.md\s+—\s+chunk\s+\d+\]", answer))


def _mentions_keywords(answer: str, keywords: list[str]) -> bool:
    low = answer.lower()
    for kw in keywords:
        if "|" in kw:
            alts = [a.strip().lower() for a in kw.split("|")]
            if not any(a in low for a in alts):
                return False
        else:
            if kw.lower() not in low:
                return False
    return True


def score_case(ans_text: str, is_idk: bool, tc: TestCase) -> tuple[int, str]:
    """Return integer quality score 1–5 and a short rationale."""
    if tc.expect_idk:
        if is_idk:
            return 5, "Correctly abstained with IDK-style response."
        if IDK_MESSAGE.split()[0] in ans_text:
            return 5, "Abstained; matched IDK template."
        return 2, "Should abstain but returned grounded-looking text (risk of hallucination)."

    if is_idk:
        return 2, "Incorrect abstention; fact exists in corpus."

    if not _has_citation(ans_text, tc.preferred_sources):
        return 3, "Answered but citation to expected source not clearly present."

    if not _mentions_keywords(ans_text, tc.must_mention):
        return 3, "Citations present but expected keywords missing or partial."

    return 5, "Grounded answer with citations and key facts."


def run_all() -> list[dict]:
    results = []
    for tc in TEST_CASES:
        rag = ask(tc.question, CHROMA)
        sc, why = score_case(rag.text, rag.is_idk, tc)
        results.append(
            {
                "id": tc.qid,
                "question": tc.question,
                "expect_idk": tc.expect_idk,
                "is_idk": rag.is_idk,
                "best_distance": rag.best_distance,
                "quality_1_to_5": sc,
                "rationale": why,
                "answer_preview": rag.text[:400].replace("\n", " "),
            }
        )
    return results


def patch_report_table(results: list[dict]) -> None:
    if not REPORT_PATH.exists():
        return
    lines = REPORT_PATH.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    skip_until_end = False
    for line in lines:
        if line.strip() == "<!-- AUTO_TABLE_START -->":
            out.append(line)
            out.append("")
            out.append("| Q | Expect IDK | Got IDK | Score (1–5) | Best distance | Notes |")
            out.append("|---|------------|---------|---------------|---------------|-------|")
            for r in results:
                bd = "" if r["best_distance"] is None else f"{r['best_distance']:.3f}"
                out.append(
                    f"| {r['id']} | {r['expect_idk']} | {r['is_idk']} | {r['quality_1_to_5']} | {bd} | {r['rationale']} |"
                )
            out.append("")
            out.append(f"_JSON metrics: `evaluation_results.json`_")
            skip_until_end = True
            continue
        if skip_until_end:
            if line.strip() == "<!-- AUTO_TABLE_END -->":
                skip_until_end = False
                out.append(line)
            continue
        if not skip_until_end:
            out.append(line)
    REPORT_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    if not CHROMA.exists():
        print("Run python ingest.py first.")
        return
    results = run_all()
    (ROOT / "evaluation_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    avg = sum(r["quality_1_to_5"] for r in results) / len(results)
    print(json.dumps(results, indent=2))
    print(f"\nMean quality score: {avg:.2f} / 5.0")
    patch_report_table(results)
    print(f"Wrote evaluation_results.json; updated {REPORT_PATH.name} auto table (if markers present).")


if __name__ == "__main__":
    main()
