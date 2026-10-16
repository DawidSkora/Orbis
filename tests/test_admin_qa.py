import pytest


def seed(supabase, *pairs):
    table = supabase.table("qa_pairs")
    for i, (q, a) in enumerate(pairs):
        table.rows.append({"id": f"00000000-0000-0000-0000-00000000000{i}", "question": q, "answer": a, "created_at": f"2026-01-0{i + 1}"})


@pytest.mark.parametrize(
    "method,path",
    [
        ("get", "/admin/qa/"),
        ("post", "/admin/qa/"),
        ("put", "/admin/qa/00000000-0000-0000-0000-000000000000"),
        ("delete", "/admin/qa/00000000-0000-0000-0000-000000000000"),
    ],
)
def test_requires_admin_token(client, method, path):
    res = client.request(method, path, json={"question": "Q", "answer": "A"})
    assert res.status_code == 401
    res = client.request(method, path, json={"question": "Q", "answer": "A"}, headers={"Authorization": "Bearer bad"})
    assert res.status_code == 401


def test_list_is_ordered_by_created_at(client, supabase, admin_headers):
    seed(supabase, ("Pierwsze?", "A1"), ("Drugie?", "A2"))
    supabase.table("qa_pairs").rows.reverse()
    res = client.get("/admin/qa/", headers=admin_headers)
    assert res.status_code == 200
    assert [r["question"] for r in res.json()] == ["Pierwsze?", "Drugie?"]


def test_create_update_delete(client, supabase, admin_headers):
    created = client.post("/admin/qa/", json={"question": "  Ile trwa wizyta? ", "answer": "Ok. 2 h"}, headers=admin_headers)
    assert created.status_code == 200
    pair = created.json()
    assert pair["question"] == "Ile trwa wizyta?"

    updated = client.put(f"/admin/qa/{pair['id']}", json={"answer": "Około 2 godzin"}, headers=admin_headers)
    assert updated.status_code == 200
    assert updated.json() == {**pair, "answer": "Około 2 godzin"}

    deleted = client.delete(f"/admin/qa/{pair['id']}", headers=admin_headers)
    assert deleted.json() == {"deleted": pair["id"]}
    assert supabase.table("qa_pairs").rows == []


def test_rejects_empty_text(client, admin_headers):
    res = client.post("/admin/qa/", json={"question": "   ", "answer": "A"}, headers=admin_headers)
    assert res.status_code == 422


def test_update_and_delete_unknown_id_return_404(client, admin_headers):
    missing = "00000000-0000-0000-0000-000000000099"
    assert client.put(f"/admin/qa/{missing}", json={"answer": "x"}, headers=admin_headers).status_code == 404
    assert client.delete(f"/admin/qa/{missing}", headers=admin_headers).status_code == 404


def test_public_qa_is_ordered_and_limited(client, supabase):
    seed(supabase, ("A?", "1"), ("B?", "2"), ("C?", "3"))
    supabase.table("qa_pairs").rows.reverse()
    res = client.get("/qa/?limit=2")
    assert [r["question"] for r in res.json()] == ["A?", "B?"]
