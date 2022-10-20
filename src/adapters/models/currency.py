from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Table

from src.adapters.databases import mapper_registry

currency_table = Table(
    "currencies",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("code", String(8)),
    Column("name", String(100)),
    Column("created_at", DateTime, default=datetime.now),
    Column("updated_at", DateTime, default=datetime.now, onupdate=datetime.now),
)
