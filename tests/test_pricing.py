import copy
import json
import re
from pathlib import Path

import pytest

MIGRATION = Path(__file__).resolve().parents[1] / "supabase" / "migrations" / "003_pricing.sql"


def seed_document():
    """The seed embedded in the migration — also a realistic fixture."""
    sql = MIGRATION.read_text()
    return json.loads(re.search(r"\$pricing\$(.*)\$pricing\$", sql, re.S).group(1))


@pytest.fixture
def seeded(supabase):
    supabase.table("pricing").rows.append({"id": 1, "data": seed_document(), "updated_at": "2026-10-01T10:00:00+00:00"})
    return supabase


def test_migration_seed_is_valid_pricing():
    from app.models.pricing import PricingData

    doc = seed_document()
    assert PricingData.model_validate(doc).to_document() == doc
    assert [c["id"] for c in doc["categories"]] == ["male", "srednie", "duze"]


def test_public_pricing(client, seeded):
    res = client.get("/pricing/")
    assert res.status_code == 200
    body = res.json()
    assert body["updatedAt"] == "2026-10-01T10:00:00+00:00"
    assert body["data"]["categories"][0]["items"][0]["price"] == "150 zł"


def test_public_pricing_404_when_not_configured(client):
    assert client.get("/pricing/").status_code == 404


def test_admin_requires_token(client, seeded):
    assert client.get("/admin/pricing/").status_code == 401
    assert client.put("/admin/pricing/", json={"data": seed_document()}).status_code == 401


def test_update_saves_revision_and_bumps_updated_at(client, seeded, admin_headers):
    doc = seed_document()
    doc["categories"][0]["items"][0]["price"] = " 160 zł "
    res = client.put(
        "/admin/pricing/",
        json={"data": doc, "expectedUpdatedAt": "2026-10-01T10:00:00+00:00"},
        headers=admin_headers,
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["data"]["categories"][0]["items"][0]["price"] == "160 zł"
    assert body["updatedAt"] != "2026-10-01T10:00:00+00:00"

    revisions = seeded.table("pricing_revisions").rows
    assert len(revisions) == 1
    assert revisions[0]["data"]["categories"][0]["items"][0]["price"] == "150 zł"


def test_update_conflict_returns_409(client, seeded, admin_headers):
    res = client.put(
        "/admin/pricing/",
        json={"data": seed_document(), "expectedUpdatedAt": "2026-09-01T00:00:00+00:00"},
        headers=admin_headers,
    )
    assert res.status_code == 409
    assert seeded.table("pricing_revisions").rows == []


def test_update_creates_row_when_missing(client, supabase, admin_headers):
    res = client.put("/admin/pricing/", json={"data": seed_document()}, headers=admin_headers)
    assert res.status_code == 200
    assert supabase.table("pricing").rows[0]["id"] == 1


@pytest.mark.parametrize(
    "mutate",
    [
        lambda d: d["categories"][0]["items"][0].update(name="  "),
        lambda d: d["categories"][0]["items"][0].update(price=""),
        lambda d: d["categories"][1].update(id="male"),
        lambda d: d["categories"][0].update(id="Małe psy"),
        lambda d: d.update(categories=[]),
        lambda d: d["notes"].append(" "),
        lambda d: d.update(unknown=True),
    ],
    ids=["empty-name", "empty-price", "duplicate-id", "bad-id", "no-categories", "empty-note", "extra-field"],
)
def test_invalid_documents_are_rejected(client, seeded, admin_headers, mutate):
    doc = copy.deepcopy(seed_document())
    mutate(doc)
    res = client.put("/admin/pricing/", json={"data": doc}, headers=admin_headers)
    assert res.status_code == 422


def test_empty_examples_are_dropped(client, seeded, admin_headers):
    doc = seed_document()
    doc["categories"][0]["items"][0]["examples"] = "  "
    res = client.put("/admin/pricing/", json={"data": doc}, headers=admin_headers)
    assert "examples" not in res.json()["data"]["categories"][0]["items"][0]
