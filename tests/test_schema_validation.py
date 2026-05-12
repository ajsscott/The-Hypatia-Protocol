#!/usr/bin/env python3
"""Tests for scripts/validate-schemas.py — schema-conformance gate per Q-05.

Covers the three Intelligence store schemas (patterns / knowledge / reasoning),
plus a smoke test on the empty stores that ship in the repo to verify they
pass cleanly.
"""
from __future__ import annotations

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
validate_mod = importlib.import_module("validate-schemas")


def valid_pattern():
    return {
        "id": "pat-test-001",
        "category": "preference",
        "content": "Prefer named kwargs past two arguments for readability.",
        "confidence": 0.9,
        "tags": ["python", "style"],
        "context": "Hypatia code review",
        "created": "2026-05-12",
        "lastAccessed": "2026-05-12",
        "accessCount": 3,
    }


def valid_knowledge():
    return {
        "id": "know-test-001",
        "category": "technical",
        "content": "Roo Code's tool-use protocol mirrors Cline's — fs_read becomes read_file.",
        "confidence": 0.95,
        "tags": ["roo", "tools"],
        "source": "https://docs.roocode.com/",
        "created": "2026-05-12",
        "lastAccessed": "2026-05-12",
        "accessCount": 1,
    }


def valid_reasoning():
    return {
        "id": "reason-test-001",
        "type": "deduction",
        "content": "If Hypatia must run on Ollama for vendor-lock resilience, then prompt-cache-dependent designs are off the table.",
        "intent": "constraint propagation",
        "reuse_signal": "high",
        "confidence": 0.85,
        "tags": ["llm-agnostic"],
        "derived_from": ["know-001"],
        "provenance": "synthesized",
        "created": "2026-05-12",
        "lastAccessed": "2026-05-12",
        "accessCount": 0,
    }


class TestPatternSchema(unittest.TestCase):
    def _validate(self, entry):
        return validate_mod.validate_entry(
            entry, validate_mod.PATTERN_REQUIRED, validate_mod.PATTERN_OPTIONAL,
            "category", validate_mod.PATTERN_CATEGORIES,
            validate_mod.PATTERN_CONTENT_LIMIT, "patterns",
        )

    def test_valid_entry_clean(self):
        issues = self._validate(valid_pattern())
        errors = [m for sev, m in issues if sev == "ERROR"]
        self.assertEqual(errors, [])

    def test_missing_required_field(self):
        entry = valid_pattern()
        del entry["confidence"]
        issues = self._validate(entry)
        self.assertTrue(any(sev == "ERROR" and "confidence" in m for sev, m in issues))

    def test_wrong_type(self):
        entry = valid_pattern()
        entry["tags"] = "not-a-list"
        issues = self._validate(entry)
        self.assertTrue(any(sev == "ERROR" and "tags" in m for sev, m in issues))

    def test_bad_category_enum(self):
        entry = valid_pattern()
        entry["category"] = "not-a-real-category"
        issues = self._validate(entry)
        self.assertTrue(any(sev == "WARN" and "not in enum" in m for sev, m in issues))

    def test_legacy_category_is_warn_not_error(self):
        entry = valid_pattern()
        entry["category"] = "communication"   # PATTERN_LEGACY_CATEGORIES member
        issues = self._validate(entry)
        self.assertTrue(any(sev == "WARN" and "legacy category" in m for sev, m in issues))
        self.assertFalse(any(sev == "ERROR" for sev, m in issues))

    def test_content_over_limit_is_info(self):
        entry = valid_pattern()
        entry["content"] = "x" * (validate_mod.PATTERN_CONTENT_LIMIT + 50)
        issues = self._validate(entry)
        self.assertTrue(any(sev == "INFO" and "exceeds" in m for sev, m in issues))


class TestKnowledgeSchema(unittest.TestCase):
    def _validate(self, entry):
        return validate_mod.validate_entry(
            entry, validate_mod.KNOWLEDGE_REQUIRED, validate_mod.KNOWLEDGE_OPTIONAL,
            "category", validate_mod.KNOWLEDGE_CATEGORIES,
            validate_mod.KNOWLEDGE_CONTENT_LIMIT, "knowledge",
        )

    def test_valid_entry_clean(self):
        errors = [m for sev, m in self._validate(valid_knowledge()) if sev == "ERROR"]
        self.assertEqual(errors, [])

    def test_legacy_field_is_error(self):
        entry = valid_knowledge()
        entry["last_accessed"] = "2026-05-12"   # legacy snake_case dup of lastAccessed
        issues = self._validate(entry)
        self.assertTrue(any(sev == "ERROR" and "legacy field" in m for sev, m in issues))

    def test_unknown_field_is_info(self):
        entry = valid_knowledge()
        entry["completely_new_field"] = "x"
        issues = self._validate(entry)
        self.assertTrue(any(sev == "INFO" and "unknown field" in m for sev, m in issues))


class TestReasoningSchema(unittest.TestCase):
    def _validate(self, entry):
        return validate_mod.validate_entry(
            entry, validate_mod.REASONING_REQUIRED, validate_mod.REASONING_OPTIONAL,
            "type", validate_mod.REASONING_TYPES,
            validate_mod.REASONING_CONTENT_LIMIT, "reasoning",
        )

    def test_valid_entry_clean(self):
        errors = [m for sev, m in self._validate(valid_reasoning()) if sev == "ERROR"]
        self.assertEqual(errors, [])

    def test_bad_type_enum(self):
        entry = valid_reasoning()
        entry["type"] = "not-a-real-type"
        issues = self._validate(entry)
        self.assertTrue(any(sev == "WARN" and "not in enum" in m for sev, m in issues))

    def test_bad_provenance_enum(self):
        entry = valid_reasoning()
        entry["provenance"] = "not-a-real-provenance"
        issues = self._validate(entry)
        self.assertTrue(any(sev == "WARN" and "provenance" in m for sev, m in issues))

    def test_derived_from_must_be_list(self):
        entry = valid_reasoning()
        entry["derived_from"] = "know-001"   # wrong type — should be list
        issues = self._validate(entry)
        self.assertTrue(any(sev == "ERROR" and "derived_from" in m for sev, m in issues))


class TestEmptyShippingStores(unittest.TestCase):
    """The empty JSON stores that ship in hypatia-kb/Intelligence/ must validate clean."""

    def test_patterns_empty_clean(self):
        path = REPO_ROOT / "hypatia-kb" / "Intelligence" / "patterns.json"
        issues = validate_mod.validate_store(
            str(path), validate_mod.PATTERN_REQUIRED, validate_mod.PATTERN_OPTIONAL,
            "category", validate_mod.PATTERN_CATEGORIES,
            validate_mod.PATTERN_CONTENT_LIMIT, "patterns",
        )
        self.assertEqual([m for sev, m in issues if sev == "ERROR"], [])

    def test_knowledge_empty_clean(self):
        path = REPO_ROOT / "hypatia-kb" / "Intelligence" / "knowledge.json"
        issues = validate_mod.validate_store(
            str(path), validate_mod.KNOWLEDGE_REQUIRED, validate_mod.KNOWLEDGE_OPTIONAL,
            "category", validate_mod.KNOWLEDGE_CATEGORIES,
            validate_mod.KNOWLEDGE_CONTENT_LIMIT, "knowledge",
        )
        self.assertEqual([m for sev, m in issues if sev == "ERROR"], [])

    def test_reasoning_empty_clean(self):
        path = REPO_ROOT / "hypatia-kb" / "Intelligence" / "reasoning.json"
        issues = validate_mod.validate_store(
            str(path), validate_mod.REASONING_REQUIRED, validate_mod.REASONING_OPTIONAL,
            "type", validate_mod.REASONING_TYPES,
            validate_mod.REASONING_CONTENT_LIMIT, "reasoning",
        )
        self.assertEqual([m for sev, m in issues if sev == "ERROR"], [])


class TestSynonymMap(unittest.TestCase):
    """Synonym map JSON is structurally simple but has invariants worth pinning."""

    def setUp(self):
        path = REPO_ROOT / "hypatia-kb" / "Intelligence" / "synonym-map.json"
        self.data = json.loads(path.read_text())

    def test_has_meta_and_synonyms_keys(self):
        self.assertIn("_meta", self.data)
        self.assertIn("synonyms", self.data)

    def test_synonyms_values_are_lists(self):
        for canonical, aliases in self.data["synonyms"].items():
            self.assertIsInstance(aliases, list, f"{canonical} aliases must be a list")
            for a in aliases:
                self.assertIsInstance(a, str, f"{canonical} alias {a!r} must be str")

    def test_canonical_terms_are_unique(self):
        # JSON parsing already deduplicates keys; this assertion is documentation.
        keys = list(self.data["synonyms"].keys())
        self.assertEqual(len(keys), len(set(keys)))

    def test_no_canonical_appears_as_its_own_alias(self):
        for canonical, aliases in self.data["synonyms"].items():
            self.assertNotIn(canonical, aliases,
                             f"{canonical} listed as its own alias (redundant)")


if __name__ == "__main__":
    unittest.main()
