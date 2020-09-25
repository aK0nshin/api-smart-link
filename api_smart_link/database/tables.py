from sqlalchemy import MetaData, Table, Column, BigInteger, DateTime, String, Boolean

db_meta = MetaData()

notes = Table(
    "users",
    db_meta,
    Column("id", BigInteger, primary_key=True),
    Column("created_at", DateTime, nullable=True),
    Column("updated_at", DateTime, nullable=True),
    Column("name", String(length=128)),
    Column("email", String(length=128)),
    Column("password", String(length=256)),
)
