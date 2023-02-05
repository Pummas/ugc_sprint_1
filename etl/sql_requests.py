create_shard = "CREATE DATABASE IF NOT EXISTS shard;"
create_replica = "CREATE DATABASE IF NOT EXISTS replica;"
create_shard_table = """
CREATE TABLE 
IF NOT EXISTS 
shard.viewed_films (user_id Int64, film_id Int64,  film_minutes Int64) 
Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/viewed_films', 'replica_1') 
PARTITION BY film_id ORDER BY user_id;
"""
create_replica_table = """
CREATE TABLE IF NOT EXISTS 
replica.viewed_films (user_id Int64, film_id Int64,  film_minutes Int64) 
Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/viewed_films', 'replica_2') 
PARTITION BY film_id ORDER BY user_id;
                       """
create_default_table = """
CREATE TABLE IF NOT EXISTS 
default.viewed_films 
(user_id Int64, film_id Int64,  film_minutes Int64) 
ENGINE = Distributed('company_cluster', '', viewed_films, rand());
                       """
create_shard2_table = """
CREATE TABLE IF NOT EXISTS 
shard.viewed_films (user_id Int64, film_id Int64,  film_minutes Int64) 
Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/viewed_films', 'replica_1') 
PARTITION BY film_id ORDER BY user_id;
"""

create_replica2_table = """
CREATE TABLE IF NOT EXISTS 
replica.viewed_films (user_id Int64, film_id Int64,  film_minutes Int64) 
Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/viewed_films', 'replica_2') 
PARTITION BY film_id ORDER BY user_id;
"""

create_default2_table = """
CREATE TABLE IF NOT EXISTS 
default.viewed_films 
(user_id Int64, film_id Int64,  film_minutes Int64) 
ENGINE = Distributed('company_cluster', '', viewed_films, rand());
"""