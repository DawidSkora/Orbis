"""Test setup: replaces app.database with an in-memory fake so tests never touch Supabase."""
import os
import sys
import types
import uuid
from datetime import datetime, timezone

import pytest

os.environ.setdefault("AUTH_SECRET", "test-secret-that-is-at-least-32-bytes-long")


class _Result:
    def __init__(self, data):
        self.data = data


class _Query:
    def __init__(self, table, op, payload=None):
        self.table, self.op, self.payload = table, op, payload
        self.filters, self.order_by, self.max_rows = [], [], None

    def select(self, *_):
        return self

    def eq(self, column, value):
        self.filters.append((column, value))
        return self

    def order(self, column, desc=False):
        self.order_by.append((column, desc))
        return self

    def limit(self, n):
        self.max_rows = n
        return self

    def _matches(self, row):
        return all(str(row.get(c)) == str(v) for c, v in self.filters)

    def execute(self):
        rows = self.table.rows
        if self.op == "insert":
            row = {"id": str(uuid.uuid4()), "created_at": datetime.now(timezone.utc).isoformat(), **self.payload}
            rows.append(row)
            return _Result([row])
        if self.op == "update":
            hit = [r for r in rows if self._matches(r)]
            for r in hit:
                r.update(self.payload)
            return _Result(hit)
        if self.op == "delete":
            hit = [r for r in rows if self._matches(r)]
            self.table.rows = [r for r in rows if r not in hit]
            return _Result(hit)
        out = [dict(r) for r in rows if self._matches(r)]
        for column, desc in reversed(self.order_by):
            out.sort(key=lambda r: r.get(column) or "", reverse=desc)
        return _Result(out[: self.max_rows] if self.max_rows else out)


class _Table:
    def __init__(self):
        self.rows = []

    def select(self, *_):
        return _Query(self, "select")

    def insert(self, payload):
        return _Query(self, "insert", payload)

    def update(self, payload):
        return _Query(self, "update", payload)

    def delete(self):
        return _Query(self, "delete")


class FakeSupabase:
    def __init__(self):
        self.tables = {}

    def table(self, name):
        return self.tables.setdefault(name, _Table())


fake_db = types.ModuleType("app.database")
fake_db.supabase = FakeSupabase()
sys.modules["app.database"] = fake_db


@pytest.fixture
def supabase():
    fake_db.supabase.tables.clear()
    return fake_db.supabase


@pytest.fixture
def client(supabase):
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


@pytest.fixture
def admin_headers():
    from app.deps.auth import create_access_token

    return {"Authorization": f"Bearer {create_access_token('u1', 'admin')}"}
