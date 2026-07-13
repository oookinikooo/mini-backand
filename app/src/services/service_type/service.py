from .schema import ServiceType

ITEMS = {
    1: "Встреча гостей",
    2: "Доставка документов",
    3: "Мойка автомобиля",
    4: "Перегон автомобиля в автосервис(ТО, ремонт, шиномонтаж)",
    5: "Сопровождение руководителя",
    6: "Фактура",
    7: "Прочее",
}


class Service:
    async def get(self, row_id: int | str) -> ServiceType | None:
        if isinstance(row_id, str) and not row_id.isdigit():
            return None

        row_id = int(row_id)
        if resp := ITEMS.get(row_id):
            return ServiceType(id=row_id, name=resp)
        return None

    async def get_all(self) -> list[ServiceType]:
        rows = [ServiceType(id=i, name=ITEMS[i]) for i in ITEMS]
        return sorted(rows, key=lambda x: x.id)
