# Результаты тестирования хранилищ Clickhouse и Vertica

Для тестирования мы выбрали два хранилища: Clickhouse и Vertica. Обе были развернуты на одной ноде в докер контейнере. Перед началом тестирования в обе БД было загружено 10 млн. тестовых записей.
В результате тестирования была измерена средняя скорость выполнения запросов на чтение уже существующих данных из БД, а также добавление новых данных в БД.

###1. Средняя скорость чтение данных из БД при выполнении следующих запросов:

-`select_count` - получить количество записей в БД
```sql
SELECT count() FROM test.views
```
Clickhouse - 0.0034317708015441893
Vertica - 0.07541932106018066

- `select_max_timestamp_by_user_movie` - получить последнюю временную отметку(timestamp), на которой остановился пользователь при просмотре фильма
```sql
SELECT MAX (timestamp) 
FROM test.views 
WHERE movie_id = %(movie_id)s 
AND user_id = %(user_id)s
```
Clickhouse - 0.14352055072784423
Vertica - 0.20426430344581603

- `select_max_timestamps_by_user` - получить timestamp-ы, на которых остановился пользователь для всех фильмов
```sql
SELECT movie_id, max(timestamp) 
FROM test.views 
WHERE user_id = %(user_id)s 
GROUP BY movie_id
```
Clickhouse - 0.14173938751220702
Vertica - 0.21342064261436464

- `select_movies_by_user` - получить id всех фильмов, которые смотрел определенный пользователь
```sql
SELECT DISTINCT (movie_id) 
FROM test.views 
WHERE user_id = %(user_id)s
```
Clickhouse - 0.11394890069961548
Vertica - 0.22883625507354735

- `select_users_by_movie` - получить id всех пользователей, которые смотрели определенный фильм
```sql
SELECT DISTINCT (user_id) FROM test.stats WHERE movie_id = %(movie_id)s
```
Clickhouse - 0.09843321681022645
Vertica - 0.2199421000480652


###2. Средняя скорость записи данных в БД разного количества:

Вставка 1 записи
Clickhouse - 0.005311518907546997
Vertica - 0.008367453813552856

Вставка 10 записей
Clickhouse - 0.004150627851486206
Vertica - 0.08395615935325623

Вставка 200 записей
Clickhouse - 0.005924476385116577
Vertica - 1.6160258209705354

Вставка 500 записей
Clickhouse - 0.008380765914916993
Vertica - 3.9117399179935455

Вставка 1000 записей
Clickhouse - 0.012998361587524414
Vertica - 8.6335749065876


Тестирование показало, что чтение и запись данных по всем запросам в Clickhouse происходит значительно быстрее, чем в Vertica, поэтому для дальнейшей работы нами был выбран Clickhouse.
