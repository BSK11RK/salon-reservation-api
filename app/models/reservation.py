from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.menu import Menu
    from app.models.staff import Staff


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False
    )
    staff_id: Mapped[int] = mapped_column(
        ForeignKey("staffs.id"),
        nullable=False
    )
    menu_id: Mapped[int] = mapped_column(
        ForeignKey("menus.id"), 
        nullable=False
    )
    start_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    end_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    customer: Mapped["Customer"] = relationship(
        back_populates="reservations"
    )
    staff: Mapped["Staff"] = relationship(
        back_populates="reservations"
    )
    menu: Mapped["Menu"] = relationship(
        back_populates="reservations"
    )