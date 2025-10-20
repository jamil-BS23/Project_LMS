# alembic/env.py
import sys
import os
import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

DATABASE_URL = os.getenv("DATABASE_URL")

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import models and Base
from app.database import Base
from app.models.book import Book  # import all models here
from app.models.donation_book import DonationBook  # import all models here
target_metadata = Base.metadata

# Logging config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_online() -> None:
    connectable = create_async_engine(DATABASE_URL, future=True, poolclass=pool.NullPool)

    def do_migrations(sync_conn):
        context.configure(
            connection=sync_conn,
            target_metadata=target_metadata,
            compare_type=True
        )
        context.run_migrations()

    async def async_run():
        async with connectable.begin() as conn:
            await conn.run_sync(do_migrations)

    asyncio.run(async_run())



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
