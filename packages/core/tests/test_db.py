from plummet_core.db import make_engine, session_scope
from plummet_core.models import Product


def test_creates_sqlite_folder(tmp_path):
    db_file = tmp_path / "data" / "test.db"

    make_engine(f"sqlite:///{db_file}")

    assert db_file.parent.is_dir()


def test_session_scope_saves_changes(engine):
    with session_scope(engine) as session:
        session.add(Product(url="https://shop.test/a", store="shop.test"))

    with session_scope(engine) as session:
        assert session.query(Product).count() == 1


def test_session_scope_undoes_changes_on_error(engine):
    try:
        with session_scope(engine) as session:
            session.add(Product(url="https://shop.test/a", store="shop.test"))
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    with session_scope(engine) as session:
        assert session.query(Product).count() == 0
