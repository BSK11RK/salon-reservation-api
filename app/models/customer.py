from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.reservation import Reservation
    from app.models.user import User


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user: Mapped[str] = relationship("User", back_populates="customer")
    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="customer"
    )