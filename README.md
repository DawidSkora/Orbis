# Orbis

FastAPI backend for Wyczesana Łapka (Supabase).

## Gallery setup

1. In Supabase SQL Editor, run [`supabase/migrations/001_gallery_photos.sql`](supabase/migrations/001_gallery_photos.sql).
2. Ensure `.env` has `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` (or `SUPABASE_ANON_KEY` with write access).
3. Seed storage + rows:

```bash
python scripts/seed_gallery.py
```

Images are read from `../wyczesanalapka/public/images` by default.

## API

- `GET /gallery/` — published photos (`?featured=true`, `?category=...`, `?limit=N`)
- `GET /gallery/{id}` — single published photo
