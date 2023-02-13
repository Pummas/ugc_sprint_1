### Спринт 8

Над проектом работали:  
* Михаил Лукин (Тимлид) https://github.com/Pummas
* Валерия Малышева https://github.com/valerycode
* Роман Боровский https://github.com/RomanBorovskiy
* Сергей Моричев https://github.com/s-morichev

### Состав проекта

/ugc - cервис UGC на FastAPI  
/etl - ETL сервис
/docs - Диаграммы по проекту 
/research - Исследование по 2 бд: Clickhouse, Vertica

Команды
- `make format` отформатировать код
- `make lint` запустить линтер (flake8)
- `make run` запустить сервисы
- `make stop` остановить сервисы
- `make etl-logs` посмотреть логи etl


Запустить проект: 

- создать .env.local(достаточно скопировать из ugc/.env.local.example) в /ugc 
- создать .env в ./ (достаточно скопировать из ./.env.example)
- `make run`


Тесты:

- Тесты API `pytest ugc/tests` (предварительно установить зависимости из ugc/requirements.txt, ugc/requirements.dev.txt)
- Тесты ETL `pytest etl/tests` (предварительно установить зависимости из etl/requirements.txt, etl/requirements.dev.txt)



### Ссылка на проект - https://github.com/Pummas/ugc_sprint_1
