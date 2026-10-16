# Orbis

FastAPI backend for Wyczesana Łapka (Supabase).

## Gallery setup

1. In Supabase SQL Editor, run:
   - [`supabase/migrations/001_gallery_photos.sql`](supabase/migrations/001_gallery_photos.sql)
   - [`supabase/migrations/002_admin_users.sql`](supabase/migrations/002_admin_users.sql)
   - [`supabase/migrations/003_pricing.sql`](supabase/migrations/003_pricing.sql) — price list table + seed (current prices)
2. Ensure `.env` has `SUPABASE_URL`, `SUPABASE_KEY` (service role), and `AUTH_SECRET`.
3. Seed storage + gallery rows:

```bash
python scripts/seed_gallery.py
```

4. Create admin account(s):

```bash
python scripts/seed_admin.py --username admin --password 'your-secure-password'
```

## Public API

- `GET /gallery/` — published photos (`?featured=true`, `?category=...`, `?limit=N`)
- `GET /gallery/{id}` — single published photo
- `GET /pricing/` — price list `{ data, updatedAt }` (404 until `003_pricing.sql` is run)

## Admin API (Bearer JWT from `POST /auth/login`)

- `POST /auth/login` — `{ username, password }` → `{ token, username }`
- `GET /auth/me` — current admin
- `GET /admin/gallery/` — all rows (including unpublished)
- `POST /admin/gallery/` — create
- `PUT /admin/gallery/{id}` — update
- `DELETE /admin/gallery/{id}` — delete
- `POST /admin/gallery/upload` — multipart image upload
- `GET /admin/pricing/` — price list `{ data, updatedAt }`
- `PUT /admin/pricing/` — replace price list `{ data, expectedUpdatedAt }`; validates the document,
  stores the previous version in `pricing_revisions`, `409` if `expectedUpdatedAt` is outdated
- `GET /admin/qa/` — all FAQ pairs (ordered by `created_at`)
- `POST /admin/qa/` — create `{ question, answer }` (trimmed, non-empty)
- `PUT /admin/qa/{id}` — update `question` and/or `answer`
- `DELETE /admin/qa/{id}` — delete

> ⚠️ Public `POST/PUT/DELETE /qa/` are still unauthenticated (used by OrbisApp). Plan: add login to
> OrbisApp, switch it to `/admin/qa/` and remove the public mutations.

## Tests

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Tests use an in-memory fake of Supabase (`tests/conftest.py`) — they never touch the real database.

Gallery mutations are **not** available on public `/gallery/` routes.

## Website admin UI

Next.js app exposes `/edit` and proxies admin calls via `/api/admin/*` with an httpOnly session cookie.
