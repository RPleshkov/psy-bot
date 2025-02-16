from datetime import datetime
from sqlalchemy import BigInteger, DateTime, String, sql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=sql.func.now()
    )


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
