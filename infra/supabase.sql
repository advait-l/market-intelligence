create extension if not exists "pgcrypto";
create extension if not exists vector;

create table if not exists stocks (
    id uuid primary key default gen_random_uuid(),
    ticker text unique not null,
    name text,
    sector text,
    exchange text,
    created_at timestamp default now()
);

create table if not exists ohlc_daily (
    id uuid primary key default gen_random_uuid(),
    stock_id uuid references stocks(id),
    date date not null,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume bigint,
    source_file_hash text,
    created_at timestamp default now(),
    unique (stock_id, date)
);

create table if not exists analyses (
    id uuid primary key default gen_random_uuid(),
    stock_id uuid references stocks(id),
    date_range_start date,
    date_range_end date,
    rsi numeric,
    macd numeric,
    signal text,
    summary text,
    created_at timestamp default now()
);

create table if not exists analysis_embeddings (
    id uuid primary key default gen_random_uuid(),
    analysis_id uuid references analyses(id),
    embedding vector(3072),
    model text,
    created_at timestamp default now()
);

create index if not exists idx_ohlc_stock_date on ohlc_daily (stock_id, date);
create index if not exists idx_analysis_stock on analyses (stock_id);
