import pytest

from tasks.models import (
    Epic,
)


class TestEpic:
    @pytest.mark.parametrize("title", ("Nice title", None))
    def test_epic_str_representation(self, title):
        """Verify epic string representation"""
        epic = Epic(title=title)

        assert str(epic) == str(title)
