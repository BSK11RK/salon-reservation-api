from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Staff(Base):
    __tablename__ = "staffs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    salon_id: Mapped[int] = mapped_column(
        ForeignKey("salons.id"), 
        nullable=False
    )