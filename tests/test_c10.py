
from i106 import C10, Packet
import pytest

from common import SAMPLE_FILE


class TestC10:

    @pytest.fixture
    def c(self):
        return C10(SAMPLE_FILE)

    def test_construct(self, c):
        assert c.handle > -1
        assert c.filename == SAMPLE_FILE

    def test_open_buffer(self):
        with open(SAMPLE_FILE, 'rb') as f:
            buf = f.read(1000)

        c = C10(buffer=buf)
        assert c.filename == '<buffer>'

    def test_iteration(self, c):
        for p in c:
            assert isinstance(p, Packet)

    def test_tell(self, c):
        c.__next__()
        assert c.tell() == 6280

    def test_seek(self, c):
        c.seek(100)
        assert c.tell() == 100
