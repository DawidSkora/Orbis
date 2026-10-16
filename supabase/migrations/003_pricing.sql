-- Price list (cennik) for the website, edited in the /edit admin panel.
-- Run in Supabase SQL Editor after 002_admin_users.sql. Safe to re-run: the seed is
-- inserted only when no price list exists yet.

-- Single-row document (id is always 1). `data` shape (camelCase, validated by Orbis):
--   { categories: [{ id, title, subtitle, items: [{ name, description, price, examples? }] }],
--     additionalServices: [{ name, price }], soloServices: [{ name, price }], notes: [text] }
create table if not exists public.pricing (
  id smallint primary key default 1 check (id = 1),
  data jsonb not null,
  updated_at timestamptz not null default now()
);

-- Previous versions, written by Orbis on every save (restore by copying `data` back).
create table if not exists public.pricing_revisions (
  id bigint generated always as identity primary key,
  data jsonb not null,
  valid_until timestamptz not null default now()
);

alter table public.pricing enable row level security;
alter table public.pricing_revisions enable row level security;
-- No public policies: access only via Orbis service role

insert into public.pricing (id, data)
values (1, $pricing${
  "categories": [
    {
      "id": "male",
      "title": "Małe psy",
      "subtitle": "do 10 kg",
      "items": [
        {
          "name": "Pakiet Klasyczny",
          "description": "krótka fryzura maszynką na jedną długość, kąpiel, pazurki",
          "price": "150 zł",
          "examples": "Maltańczyk, Shih Tzu, York, Maltipoo, Cavapoo, Pudel Toy"
        },
        {
          "name": "Pakiet Stylowy",
          "description": "dłuższa fryzura, praca nożyczkami, kąpiel, pazurki",
          "price": "170 zł",
          "examples": "Maltańczyk, Shih Tzu, York, Maltipoo, Cavapoo, Pudel Toy"
        },
        {
          "name": "Pakiet Pielęgnacyjny",
          "description": "krótkowłose – kąpiel, wyczesanie, pazurki",
          "price": "120 zł",
          "examples": "Mops, Buldog Francuski, kundelek do 10 kg"
        },
        {
          "name": "Pakiet Pielęgnacyjny",
          "description": "długowłose – kąpiel, wyczesanie, pazurki",
          "price": "140 zł",
          "examples": "Pomeranian, Pekińczyk, kundelek do 10 kg"
        },
        {
          "name": "Pakiet Trymowanie",
          "description": "kąpiel, trymowanie, pazurki",
          "price": "80 zł/h",
          "examples": "JRT, kundelek do 10 kg"
        }
      ]
    },
    {
      "id": "srednie",
      "title": "Średnie psy",
      "subtitle": "do 25 kg",
      "items": [
        {
          "name": "Pakiet Pielęgnacyjny",
          "description": "kąpiel, wyczesanie, pazurki",
          "price": "150 zł",
          "examples": "Beagle, Bulterier, Corgi, kundelek do 25 kg"
        },
        {
          "name": "Pakiet Stylowy",
          "description": "długowłose – praca nożyczkami/maszynką, kąpiel, pazurki",
          "price": "200 zł",
          "examples": "Lagotto, Cocker Spaniel, Cockapoo"
        },
        {
          "name": "Pakiet Podszerstek",
          "description": "kąpiel, usunięcie podszerstka, pazurki",
          "price": "100 zł/h",
          "examples": "Samoyed, Husky, Border Collie"
        },
        {
          "name": "Pakiet Trymowanie",
          "description": "kąpiel, trymowanie, pazurki",
          "price": "100 zł/h",
          "examples": "Foksterier, kundelek do 25 kg"
        }
      ]
    },
    {
      "id": "duze",
      "title": "Duże psy",
      "subtitle": "do 40 kg",
      "items": [
        {
          "name": "Pakiet Pielęgnacyjny",
          "description": "krótkowłose – kąpiel, wyczesanie, pazurki",
          "price": "200 zł",
          "examples": "Labrador, Owczarek Belgijski"
        },
        {
          "name": "Pakiet Stylowy",
          "description": "długowłose – praca nożyczkami/maszynką, kąpiel, pazurki",
          "price": "300 zł",
          "examples": "Goldendoodle"
        },
        {
          "name": "Pakiet Podszerstek",
          "description": "kąpiel, usunięcie podszerstka, pazurki",
          "price": "110 zł/h",
          "examples": "Owczarek Niemiecki/Szwajcarski/Szkocki/Podhalański, kundelek do 40 kg"
        }
      ]
    }
  ],
  "additionalServices": [
    {
      "name": "Rozczesywanie kołtunów/filc",
      "price": "+30 zł do usługi"
    },
    {
      "name": "Czyszczenie uszu",
      "price": "20 zł"
    },
    {
      "name": "Usuwanie kleszczy",
      "price": "10 zł/szt"
    }
  ],
  "soloServices": [
    {
      "name": "Obcinanie włosów przy oczach",
      "price": "40 zł"
    },
    {
      "name": "Obcinanie pazurków",
      "price": "30 zł"
    },
    {
      "name": "Wizyta adaptacyjna",
      "price": "bezpłatna"
    },
    {
      "name": "Usuwanie kleszcza",
      "price": "30 zł"
    }
  ],
  "notes": [
    "W przypadku zachowań agresywnych psa podczas wizyty doliczana jest dodatkowa opłata w postaci 50% ceny bazowej.",
    "Cena może się różnić w przypadku złego stanu sierści lub dużej ilości kołtunów.",
    "W przypadku znalezienia pcheł na psie, wizyta kończy się natychmiast, a właściciel pokrywa koszty wizyty + dezynfekcji."
  ]
}$pricing$::jsonb)
on conflict (id) do nothing;
