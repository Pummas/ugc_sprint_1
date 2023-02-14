CREATE DATABASE IF NOT EXISTS shard;
CREATE DATABASE IF NOT EXISTS replica;

CREATE TABLE IF NOT EXISTS
shard.viewed_films (user_id UUID, film_id UUID,  pos_start Int64, pos_end Int64, created_at DateTime DEFAULT now())
Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/viewed_films', 'replica_1')
PARTITION BY toYYYYMMDD(created_at) ORDER BY film_id;

CREATE TABLE IF NOT EXISTS
replica.viewed_films (user_id UUID, film_id UUID,  pos_start Int64, pos_end Int64, created_at DateTime DEFAULT now())
Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/viewed_films', 'replica_2')
PARTITION BY toYYYYMMDD(created_at) ORDER BY film_id;

CREATE TABLE IF NOT EXISTS
default.viewed_films
(user_id UUID, film_id UUID,  pos_start Int64, pos_end Int64, created_at DateTime DEFAULT now())
ENGINE = Distributed('company_cluster', '', viewed_films, rand());