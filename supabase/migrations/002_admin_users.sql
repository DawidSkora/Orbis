-- Admin users for /edit panel (passwords stored as bcrypt hashes only)
-- Run in Supabase SQL Editor after 001_gallery_photos.sql

create table if not exists public.admin_users (
  id uuid primary key default gen_random_uuid(),
  username text not null unique,
  password_hash text not null,
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

alter table public.admin_users enable row level security;

-- No public policies: access only via Orbis service role
