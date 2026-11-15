"""Tests for Jira constants.

Focused tests for Jira constants, validating correct values and business logic.
"""

from mcp_atlassian.jira.constants import (
    DEFAULT_READ_JIRA_FIELDS,
    DEFAULT_READ_JIRA_FIELDS_CSV,
)


class TestDefaultReadJiraFields:
    """Test suite for DEFAULT_READ_JIRA_FIELDS constant."""

    def test_type_and_structure(self):
        """Test that DEFAULT_READ_JIRA_FIELDS is a set of strings."""
        assert isinstance(DEFAULT_READ_JIRA_FIELDS, set)
        assert all(isinstance(field, str) for field in DEFAULT_READ_JIRA_FIELDS)
        assert len(DEFAULT_READ_JIRA_FIELDS) == 11

    def test_contains_expected_jira_fields(self):
        """Test that DEFAULT_READ_JIRA_FIELDS contains the correct Jira fields."""
        expected_fields = {
            "summary",
            "description",
            "status",
            "assignee",
            "reporter",
            "labels",
            "versions",
            "priority",
            "created",
            "updated",
            "issuetype",
        }
        assert DEFAULT_READ_JIRA_FIELDS == expected_fields

    def test_essential_fields_present(self):
        """Test that essential Jira fields are included."""
        essential_fields = {"summary", "status", "issuetype"}
        assert essential_fields.issubset(DEFAULT_READ_JIRA_FIELDS)

    def test_field_format_validity(self):
        """Test that field names are valid for API usage."""
        for field in DEFAULT_READ_JIRA_FIELDS:
            # Fields should be non-empty, lowercase, no spaces
            assert field and field.islower()
            assert " " not in field
            assert not field.startswith("_")
            assert not field.endswith("_")

    def test_csv_is_sorted_and_complete(self):
        """The published default must not depend on set iteration order."""
        assert DEFAULT_READ_JIRA_FIELDS_CSV == ",".join(
            sorted(DEFAULT_READ_JIRA_FIELDS)
        )
        assert set(DEFAULT_READ_JIRA_FIELDS_CSV.split(",")) == DEFAULT_READ_JIRA_FIELDS


def test_tool_defaults_are_stable_across_processes():
    """Two interpreters with different hash seeds publish the same default."""
    import os
    import subprocess
    import sys

    code = "from mcp_atlassian.jira.constants import DEFAULT_READ_JIRA_FIELDS_CSV as c; print(c)"
    outputs = {
        subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "PYTHONHASHSEED": seed},
        ).stdout
        for seed in ("1", "2", "3")
    }
    assert len(outputs) == 1
