# Orbis

FastAPI backend for Wyczesana Łapka (Supabase).

## Gallery setup

1. In Supabase SQL Editor, run:
   - [`supabase/migrations/001_gallery_photos.sql`](supabase/migrations/001_gallery_photos.sql)
   - [`supabase/migrations/002_admin_users.sql`](supabase/migrations/002_admin_users.sql)
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

## Admin API (Bearer JWT from `POST /auth/login`)

- `POST /auth/login` — `{ username, password }` → `{ token, username }`
- `GET /auth/me` — current admin
- `GET /admin/gallery/` — all rows (including unpublished)
- `POST /admin/gallery/` — create
- `PUT /admin/gallery/{id}` — update
- `DELETE /admin/gallery/{id}` — delete
- `POST /admin/gallery/upload` — multipart image upload

Gallery mutations are **not** available on public `/gallery/` routes.

## Website admin UI

Next.js app exposes `/edit` and proxies admin calls via `/api/admin/*` with an httpOnly session cookie.
