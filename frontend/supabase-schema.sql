-- Voice AI Agent - Supabase Database Schema
-- Führe dieses SQL in deinem Supabase SQL Editor aus

-- Profiles table
create table profiles (
  user_id uuid references auth.users primary key,
  username text,
  default_callback_number text,
  street text,
  house_number text,
  postal_code text,
  city text,
  country text default 'Germany',
  calendar_connected boolean default false,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Requests table
create table requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users not null,
  title text not null,
  description text not null,
  callback_number text not null,
  number_to_call text,
  preferred_time text not null,
  status text not null default 'queued',
  summary text,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Events table
create table events (
  id uuid primary key default gen_random_uuid(),
  request_id uuid references requests(id) on delete cascade not null,
  type text not null,
  message text not null,
  created_at timestamp with time zone default now()
);

-- Enable Row Level Security
alter table profiles enable row level security;
alter table requests enable row level security;
alter table events enable row level security;

-- Profiles policies
create policy "Users can view own profile"
  on profiles for select
  using (auth.uid() = user_id);

create policy "Users can insert own profile"
  on profiles for insert
  with check (auth.uid() = user_id);

create policy "Users can update own profile"
  on profiles for update
  using (auth.uid() = user_id);

-- Requests policies
create policy "Users can view own requests"
  on requests for select
  using (auth.uid() = user_id);

create policy "Users can create own requests"
  on requests for insert
  with check (auth.uid() = user_id);

create policy "Users can update own requests"
  on requests for update
  using (auth.uid() = user_id);

-- Events policies
create policy "Users can view events for own requests"
  on events for select
  using (
    exists (
      select 1 from requests
      where requests.id = events.request_id
      and requests.user_id = auth.uid()
    )
  );

create policy "Users can create events for own requests"
  on events for insert
  with check (
    exists (
      select 1 from requests
      where requests.id = events.request_id
      and requests.user_id = auth.uid()
    )
  );

-- Indexes für bessere Performance
create index requests_user_id_idx on requests(user_id);
create index requests_status_idx on requests(status);
create index events_request_id_idx on events(request_id);
create index events_created_at_idx on events(created_at desc);

-- Trigger für updated_at
create or replace function update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger update_requests_updated_at
  before update on requests
  for each row
  execute function update_updated_at_column();

create trigger update_profiles_updated_at
  before update on profiles
  for each row
  execute function update_updated_at_column();