

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
from app.models import user, book, category, borrow, settings, donation_book, user_rating, book_review  # noqa: F401

import os
from dotenv import load_dotenv


load_dotenv()

config = context.config


database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("❌ DATABASE_URL not found in .env file.")

if database_url.startswith("postgresql+asyncpg"):
    sync_database_url = database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
else:
    sync_database_url = database_url

config.set_main_option("sqlalchemy.url", sync_database_url)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


