import sys
import types
from unittest.mock import patch

if "requests" not in sys.modules:
    requests_stub = types.ModuleType("requests")
    requests_stub.Session = object
    requests_stub.get = lambda *args, **kwargs: None
    requests_stub.post = lambda *args, **kwargs: None
    sys.modules["requests"] = requests_stub

if "loguru" not in sys.modules:
    loguru_stub = types.ModuleType("loguru")

    class _FakeLogger:
        def add(self, *args, **kwargs):
            return None

        def info(self, *args, **kwargs):
            return None

        def debug(self, *args, **kwargs):
            return None

        def warning(self, *args, **kwargs):
            return None

        def error(self, *args, **kwargs):
            return None

        def exception(self, *args, **kwargs):
            return None

    loguru_stub.logger = _FakeLogger()
    sys.modules["loguru"] = loguru_stub

if "toml" not in sys.modules:
    toml_stub = types.ModuleType("toml")
    toml_stub.loads = lambda *args, **kwargs: {}
    sys.modules["toml"] = toml_stub

if "chardet" not in sys.modules:
    chardet_stub = types.ModuleType("chardet")
    chardet_stub.detect = lambda *args, **kwargs: {"encoding": "utf-8"}
    sys.modules["chardet"] = chardet_stub

from shmtu_auth.src.core.core import ShmtuNetAuthCore


def test_login_legacy_success_skips_h3c_fallback():
    core = ShmtuNetAuthCore()

    with (
        patch("shmtu_auth.src.core.core.check_is_connected_retry", return_value=False),
        patch("shmtu_auth.src.core.core.get_query_string", return_value="legacy_query"),
        patch.object(
            ShmtuNetAuthCore,
            "_login_legacy",
            return_value=(True, "Login Success (Legacy)"),
        ) as legacy_mock,
        patch.object(
            ShmtuNetAuthCore,
            "_login_h3c",
            return_value=(True, "Login Success (H3C)"),
        ) as h3c_mock,
    ):
        ok, msg = core.login("202540510004", "pwd")

    assert ok is True
    assert msg == "Login Success (Legacy)"
    legacy_mock.assert_called_once_with("legacy_query")
    h3c_mock.assert_not_called()


def test_login_legacy_failed_then_h3c_fallback_success():
    core = ShmtuNetAuthCore()

    with (
        patch("shmtu_auth.src.core.core.check_is_connected_retry", return_value=False),
        patch(
            "shmtu_auth.src.core.core.get_query_string",
            return_value="http://1.1.1.1|legacy_query",
        ),
        patch.object(
            ShmtuNetAuthCore,
            "_login_legacy",
            return_value=(False, "legacy failed"),
        ) as legacy_mock,
        patch.object(
            ShmtuNetAuthCore,
            "_login_h3c",
            return_value=(True, "Login Success (H3C)"),
        ) as h3c_mock,
    ):
        ok, msg = core.login("202540510004", "pwd")

    assert ok is True
    assert msg == "Login Success (H3C)"
    legacy_mock.assert_called_once_with("legacy_query")
    h3c_mock.assert_called_once_with("202540510004", "pwd", "http://1.1.1.1")


def test_login_h3c_response_unexpected_but_network_confirmed_success():
    core = ShmtuNetAuthCore()

    with (
        patch("shmtu_auth.src.core.core.check_is_connected_retry", side_effect=[False, True]),
        patch(
            "shmtu_auth.src.core.core.get_query_string",
            return_value="http://hwifi.shmtu.edu.cn/auth.html?userip=1.1.1.1|legacy_query",
        ),
        patch.object(
            ShmtuNetAuthCore,
            "_login_legacy",
            return_value=(False, "legacy failed"),
        ),
        patch.object(
            ShmtuNetAuthCore,
            "_login_h3c",
            wraps=core._login_h3c,
        ),
        patch("shmtu_auth.src.core.core.requests.Session") as session_cls,
    ):
        session = session_cls.return_value
        session.cookies.get.return_value = None
        session.get.return_value = types.SimpleNamespace(
            url="http://hwifi.shmtu.edu.cn/auth.html?userip=1.1.1.1",
        )
        session.post.return_value = types.SimpleNamespace(
            status_code=200,
            text='{"code":0}',
            json=lambda: {"code": 0},
        )

        ok, msg = core.login("202540510004", "pwd")

    assert ok is True
    assert msg == "Login Success (H3C Confirmed)"
