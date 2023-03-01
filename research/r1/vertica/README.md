# Тестирование Vertica

Требуемая версия питона: 3.9

1. Создайте и активируйте виртуальное окружение
```commandline
python3.9 -m venv venv
. venv/bin/activate
```
2. Установите зависимости
```commandline
pip install -r requirements.txt
```
3. Запустите Vertica:
```commandline
docker-compose up -d
```
4. Создайте таблицу в БД(при первом запуске):
```commandline
python create_db.py
```
Схема таблицы в БД:
```sql
CREATE TABLE test.views (
    id IDENTITY,
    user_id UUID NOT NULL,
    movie_id UUID NOT NULL,
    timestamp INTEGER NOT NULL,
    event_time DATETIME NOT NULL
)
ORDER BY id;
```

5. Сгенерируйте тестовые данные и загрузите их в БД:
```
python load_data.py
```

5. Запустите тесты на чтение данных из БД:
```commandline
python select_tests.py
```
Результаты тестирования будут записаны в файл select_test_results.txt
6. Запустите тесты на запись данных в БД:
```commandline
python insert_tests.py
```
Тестируется время записи 1, 10, 200, 500, 1000 строк.Тестируется время записи 1, 10, 200, 500, 1000 строк. Результаты тестирования будут записаны в файл insert_test_results.txt
