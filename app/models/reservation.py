from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


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
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)