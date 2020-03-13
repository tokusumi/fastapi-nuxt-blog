import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database
from settings.database import Base


@pytest.fixture(scope="function")
def SessionLocal():
    """
    Create a clean database on every test case.
    For safety, we should abort if a database already exists.

    We use the `sqlalchemy_utils` package here for a few helpers in consistently
    creating and dropping the database.
    """
    # settings of test database
    TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
    # TODO: table is not created when in-memory db is used.
    # TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # in-memory
    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

    assert not database_exists(TEST_SQLALCHEMY_DATABASE_URL), "Test database already exists. Aborting tests."

    # Create test database and the tables
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Run the tests
    yield SessionLocal

    # Drop the test database
    drop_database(TEST_SQLALCHEMY_DATABASE_URL)
