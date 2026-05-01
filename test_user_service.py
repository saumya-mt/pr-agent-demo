"""Tests for user_service."""

from user_service import search_users, export_users_to_csv, get_admin_users


def test_search_returns_list():
    # doesn't actually test correctness, just that it doesn't crash
    result = search_users("admin")
    assert isinstance(result, list)


def test_export_creates_file():
    export_users_to_csv("/tmp/users_export.csv")
    # no assertion — just checking it doesn't throw
