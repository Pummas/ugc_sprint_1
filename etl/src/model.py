from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class CoreModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ViewedFilm(CoreModel):
    user_id: UUID
    film_id: UUID
    pos_start: int  # начало просмотра фильма, время в секундах от начала фильма
    pos_end: int  # конец просмотра фильма, время в секундах от начала фильма
