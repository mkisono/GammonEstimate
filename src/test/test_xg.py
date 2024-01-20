import sys
sys.path.append('src')
from xg import get_position

def test_get_position():
    # Test case 1: Valid xgid
    xgid = "XGID=-a---bEBBB--cB---aBcab-b--:1:0:1:00:0:0:3:0:10"
    assert get_position(xgid) == [0, -1, 0, 0, 0, -2, 5, 2, 2, 2, 0, 0, -3, 2, 0, 0, 0, -1, 2, -3, -1, -2, 0, -2, 0, 0]

    # Test case 2: Invalid xgid (contains number in position)
    xgid = "XGID=-a---bE9BB--cB---aBcab-b--:1:0:1:00:0:0:3:0:10"
    assert get_position(xgid) == None

    # Test case 3: Invalid xgid (does not start with 'XGID=')
    xgid = "-a--BCCB---dE---c-e----B-:0:0:1:11:0:0:3:0:10"
    assert get_position(xgid) == None

    # Test case 4: Invalid xgid (incorrect number of parts)
    xgid = "XGID=-a--BCCB---dE---c-e----B-:0:0:1:11:0:0:3:0"
    assert get_position(xgid) == None
