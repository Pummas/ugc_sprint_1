### UGC Сервис
env.local.example переименовать в env.local - это для локального запуска  
для запуска нужна Kafka  
Jaeger - опционально (`ENABLE_TRACER=False` - значит трассировка выключена)  
Эндпойнт `POST /ugc/v1/events/movies_view/<film_id:UUID>`
Требует JWT-токен, из него берет user_id (проверку для отладки можно отключить MOCK_AUTH_TOKEN=False)
