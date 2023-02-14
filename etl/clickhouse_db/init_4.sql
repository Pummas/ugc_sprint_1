CREATE DATABASE IF NOT EXISTS shard2;

CREATE TABLE IF NOT EXISTS
shard2.viewed_films (user_id UUID, film_id UUID,  pos_start Int64, pos_end Int64, created_at DateTime DEFAULT now())
Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/viewed_films', 'replica_2')
PARTITION BY toYYYYMMDD(created_at) ORDER BY film_id;

CREATE TABLE IF NOT EXISTS
viewed_films
(user_id UUID, film_id UUID,  pos_start Int64, pos_end Int64, created_at DateTime DEFAULT now())
ENGINE = Distributed('company_cluster', '', viewed_films, rand());