from src.param import get_id

def test_get_id():
    # Test case 1: Empty query parameters
    query_params = {}
    assert get_id(query_params, 100) == None

    query_params = {'id': ['0']}
    assert get_id(query_params, 100) == 0

    query_params = {'id': ['10']}
    assert get_id(query_params, 100) == 10

    query_params = {'id': ['1000']}
    assert get_id(query_params, 100) == None

    query_params = {'id': ['-1']}
    assert get_id(query_params, 100) == None

    query_params = {'id': ['0', '1']}
    assert get_id(query_params, 100) == 0

    query_params = {'foo': ['0']}
    assert get_id(query_params, 100) == None

    query_params = {'id': ['a']}
    assert get_id(query_params, 100) == None

    query_params = {'id': []}
    assert get_id(query_params, 100) == None

