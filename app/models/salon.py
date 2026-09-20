from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.menu import Menu
    from app.models.staff import Staff


class Salon(Base):
    __tablename__ = "salons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    staffs: Mapped[list["Staff"]] = relationship(back_populates="salon")
    menus: Mapped[list["Menu"]] = relationship(back_populates="salon")