from dataclasses import dataclass

@dataclass(frozen=True)
class OrderData:
    first_name: str
    last_name: str
    address: str
    metro_station: str
    phone: str
    delivery_date: str
    rent_period: str
    scooter_color: str 
    comment: str = ""

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}, {self.address}"
