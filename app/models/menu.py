from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.reservation import Reservation
    from app.models.salon import Salon


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id"),
        nullable=False
    )
    salon: Mapped["Salon"] = relationship(back_populates="menus")
    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="menu"
    )