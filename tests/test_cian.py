from cian import compute_yield


def test_compute_yield():
    assert compute_yield(1000000, 10000) == 0.12
    assert compute_yield(0, 10000) == 0.0
    assert compute_yield(1000000, 0) == 0.0
