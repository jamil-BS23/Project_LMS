
from logging.config import fileConfig
from sqlalchemy import create_engine, pool, inspect
from alembic import context
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import models (avoid importing async engine)
from app.models import (
    user,
    book,
    category,
    borrow,
    settings,
    donation_book,
    user_rating,
    book_review,
)  # noqa: F401
from app.models.user import Base  # Import Base from a model file

# Alembic config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Convert async URL to sync for Alembic
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL not found in .env file.")

if database_url.startswith("postgresql+asyncpg"):
    sync_database_url = database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
else:
    sync_database_url = database_url

config.set_main_option("sqlalchemy.url", sync_database_url)
target_metadata = Base.metadata


def skip_existing_tables(connection):
    """
    Detect and skip tables that already exist in the database
    to prevent 'relation already exists' errors.
    """
    inspector = inspect(connection)
    existing_tables = inspector.get_table_names()

    for table_name in list(target_metadata.tables.keys()):
        if table_name in existing_tables:
            print(f"⚠️  Table '{table_name}' already exists — skipping creation.")
            target_metadata.remove(target_metadata.tables[table_name])


def run_migrations_offline():
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


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(sync_database_url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        # Skip already existing tables
        skip_existing_tables(connection)

        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
    
