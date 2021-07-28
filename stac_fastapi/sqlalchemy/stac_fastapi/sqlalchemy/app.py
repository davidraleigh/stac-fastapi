"""FastAPI application."""
import os
import sqlalchemy
from alembic import command, config, script
from alembic.runtime import migration

from stac_fastapi.api.app import StacApi
from stac_fastapi.extensions.core import (
    FieldsExtension,
    QueryExtension,
    SortExtension,
    TransactionExtension,
)
from stac_fastapi.extensions.third_party import BulkTransactionExtension
from stac_fastapi.sqlalchemy.config import SqlalchemySettings
from stac_fastapi.sqlalchemy.core import CoreCrudClient
from stac_fastapi.sqlalchemy.session import Session
from stac_fastapi.sqlalchemy.transactions import (
    BulkTransactionsClient,
    TransactionsClient,
)
from stac_fastapi.sqlalchemy.types.search import SQLAlchemySTACSearch

settings = SqlalchemySettings()
session = Session.create_from_settings(settings)
api = StacApi(
    settings=settings,
    extensions=[
        TransactionExtension(
            client=TransactionsClient(session=session), settings=settings
        ),
        BulkTransactionExtension(client=BulkTransactionsClient(session=session)),
        FieldsExtension(),
        QueryExtension(),
        SortExtension(),
    ],
    client=CoreCrudClient(session=session),
    search_request_model=SQLAlchemySTACSearch,
)
app = api.app


@app.on_event("startup")
def check_migrations():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    script_path = f"{current_dir}/../../alembic"
    alembic_config = config.Config()
    alembic_config.config_file_name = f"{script_path}/../alembic.ini"
    alembic_config.set_main_option("script_location", script_path)
    command.upgrade(alembic_config, "407037cb1636")

    desired_migration = script.ScriptDirectory(dir=script_path).get_current_head()
    # desired_migration = "407037cb1636"
    postgres_user = settings.postgres_user
    postgres_pass = settings.postgres_pass
    postgres_host = settings.postgres_host_writer
    postgres_port = settings.postgres_port
    postgres_dbname = settings.postgres_dbname
    connection = f"postgresql://{postgres_user}:{postgres_pass}@{postgres_host}:{postgres_port}/{postgres_dbname}"

    engine = sqlalchemy.create_engine(connection)
    with engine.begin() as conn:
        context = migration.MigrationContext.configure(conn)
        current_revision = context.get_current_revision()
        if current_revision != desired_migration:
            raise ValueError(
                f"upgrade the database. "
                f"Current migrations revision {current_revision} does not match desired migration {desired_migration}"
            )


def run():
    """Run app from command line using uvicorn if available."""
    try:
        import uvicorn

        uvicorn.run(
            "stac_fastapi.sqlalchemy.app:app",
            host=settings.app_host,
            port=settings.app_port,
            log_level="info",
            reload=settings.reload,
        )
    except ImportError:
        raise RuntimeError("Uvicorn must be installed in order to use command")


if __name__ == "__main__":
    run()


def create_handler(app):
    """Create a handler to use with AWS Lambda if mangum available."""
    try:
        from mangum import Mangum

        return Mangum(app)
    except ImportError:
        return None


handler = create_handler(app)
