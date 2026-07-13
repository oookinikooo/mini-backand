from .schema import Requester

ITEMS = {
    1: "Александр Владимирович Полонский",
    2: "Александр Евгеньевич Герчиков",
    3: "Александр Сергеевич Кабышев",
    4: "Алексей Николаевич Максов",
    5: "Андрей Васильевич Мазурик",
    6: "Ателье Фактура",
    7: "Вадим Васильевич Войтюшенко",
    8: "Дмитрий Владимирович Пантюхов",
    9: "Дмитрий Петрович Короленок",
    10: "Игорь Александрович Старовойтов",
    11: "Константин Аркадьевич Силюков",
    12: "Леонид Владимирович Румберг",
    13: "Леонид Георгиевич Дарадан",
    14: "Марекас Кошелевас",
    15: "Наталья Анатольевна Пашкевич",
    16: "Наталья Маратовна Смелькинсон",
    17: "Наталья Петровна Мороз",
    18: "Петр Дмитриевич Волынец",
    19: "Сергей Александрович Гладченко",
    20: "Сергей Александрович Левченя", 
    21: "Сергей Викторович Макаренко",
    22: "Сергей Владимирович Ринг",
    23: "Сергей Сергеевич Асвадуров",
    24: "Татьяна Валерьевна Сливкина",
    25: "Тимофей Тимофеевич Солонович",
    26: "Юрий Александрович Петров",
    27: "Юрий Евгеньевич Моисеенко",
}


class Service:
    async def get(self, row_id: int | str) -> Requester | None:
        if isinstance(row_id, str) and not row_id.isdigit():
            return None

        row_id = int(row_id)
        if value := ITEMS.get(row_id):
            return Requester(id=row_id, name=value)
        return None

    async def get_all(self) -> list[Requester]:
        rows = [Requester(id=i, name=ITEMS[i]) for i in ITEMS]
        return sorted(rows, key=lambda x: x.id)

    # async def has( self, full_name: str) -> tuple[int, str] | None:
    #     for i, name in ITEMS.items():
    #         if name == full_name:
    #             return (i, name)
    #     return None
