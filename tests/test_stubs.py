import pytest

from demo.seed import main as seed_main
from jobs.nightly_consolidate import main as consolidate_main


def test_nightly_job_stub_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    assert consolidate_main(["--local"]) == 0
    assert "not implemented" in capsys.readouterr().out


def test_seed_stub_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    assert seed_main(["--reset"]) == 0
    assert "not implemented" in capsys.readouterr().out
