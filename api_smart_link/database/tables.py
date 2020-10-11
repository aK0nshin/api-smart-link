from sqlalchemy import MetaData, Table, Column, BigInteger, DateTime, String, ForeignKey, JSON, text, func

db_meta = MetaData()

users = Table(
    "users",
    db_meta,
    Column("id", BigInteger, primary_key=True),
    Column("created_at", DateTime, default=func.now(), nullable=True),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now(), nullable=True),
    Column("name", String(length=128)),
    Column("email", String(length=128), unique=True),
    Column("password", String(length=256)),
)

pages = Table(
    "pages",
    db_meta,
    Column("id", BigInteger, primary_key=True),
    Column("created_at", DateTime, default=func.now(), nullable=True),
    Column("updated_at", DateTime, default=func.now(), onupdate=func.now(), nullable=True),
    Column('user_id', BigInteger, ForeignKey("users.id"), nullable=False),
    Column("content", JSON, default=text("'{}'")),
    Column("endpoint", String(length=128), unique=True)
)
