import pytest

from revolut_api.app import make_nested_json
from tests.test_json_nested.data_for_testing import sample_input, sample_output, sample_output_2, sample_output_3


@pytest.mark.parametrize(
    "test_sample_input, keys_priority, test_sample_output",
    [
        (sample_input, ["currency", "country", "city"], sample_output),
        (sample_input, ["city"], sample_output_2),
        (sample_input, ["amount", "currency"], sample_output_3),
    ],
)
def test_make_nested_json(test_sample_input, keys_priority, test_sample_output):
    assert make_nested_json(test_sample_input, *keys_priority) == test_sample_output
