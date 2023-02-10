from uuid import UUID

from core.core_model import CoreModel


class DTOViewEvent(CoreModel):
    """Модель для события просмотр фильма"""

    user_id: UUID
    film_id: UUID
    pos_start: int  # начало просмотра фильма, время в секундах от начала фильма
    pos_end: int  # конец просмотра фильма, время в секундах от начала фильма
