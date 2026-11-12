import pytest

from plummet_worker.lock import AlreadyRunning, RunLock


def test_second_lock_fails_while_first_is_held(tmp_path):
    path = tmp_path / "worker.lock"

    with RunLock(path), pytest.raises(AlreadyRunning), RunLock(path):
        pass


def test_lock_can_be_taken_again_after_release(tmp_path):
    path = tmp_path / "data" / "worker.lock"

    with RunLock(path):
        pass
    with RunLock(path):
        pass

    assert path.exists()
