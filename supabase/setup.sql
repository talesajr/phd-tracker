-- Backend do PhD Tracker no Supabase.
-- Como usar: no painel do projeto (supabase.com) abra o SQL Editor,
-- cole este arquivo inteiro e clique em Run.

-- Tabela única: uma linha por usuário com todo o estado do app em JSON.
create table if not exists public.app_state (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  data       jsonb not null,
  updated_at timestamptz not null default now()
);

-- Row Level Security: cada usuário só lê e escreve a própria linha.
alter table public.app_state enable row level security;

drop policy if exists "own state" on public.app_state;
create policy "own state" on public.app_state
  for all to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
