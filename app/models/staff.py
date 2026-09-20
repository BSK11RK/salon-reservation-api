from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.reservation import Reservation
    from app.models.salon import Salon


class Staff(Base):
    __tablename__ = "staffs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id"),
        nullable=False
    )
    salon: Mapped["Salon"] = relationship(back_populates="staffs")
    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="staff"
    )