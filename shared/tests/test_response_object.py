from shared import response_object


def test_response_success_is_true():
    assert bool(response_object.ResponseSuccess()) is True