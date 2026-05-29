-- Gallery photos table + RLS + public storage bucket policies
-- Run in Supabase SQL Editor (Dashboard -> SQL -> New query)

-- Table
create table if not exists public.gallery_photos (
  id uuid primary key default gen_random_uuid(),
  pet_name text not null,
  breed text not null,
  service text not null,
  category text not null check (
    category in ('Strzyżenie', 'Trymowanie', 'Czesanie', 'Przed & Po')
  ),
  aspect_ratio text not null check (
    aspect_ratio in ('square', 'portrait', 'tall')
  ),
  gradient_from text not null,
  gradient_to text not null,
  storage_path text not null,
  sort_order int not null default 0,
  is_featured boolean not null default false,
  is_published boolean not null default true,
  created_at timestamptz not null default now()
);

create index if not exists gallery_photos_published_sort_idx
  on public.gallery_photos (is_published, sort_order, created_at);

-- RLS
alter table public.gallery_photos enable row level security;

drop policy if exists "Public read published gallery photos" on public.gallery_photos;
create policy "Public read published gallery photos"
  on public.gallery_photos
  for select
  to anon, authenticated
  using (is_published = true);

-- Storage bucket (public read for website images)
insert into storage.buckets (id, name, public)
values ('gallery', 'gallery', true)
on conflict (id) do update set public = true;

-- Allow public read of gallery bucket objects
drop policy if exists "Public read gallery images" on storage.objects;
create policy "Public read gallery images"
  on storage.objects
  for select
  to anon, authenticated
  using (bucket_id = 'gallery');
