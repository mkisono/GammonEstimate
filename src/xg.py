from typing import List
conv_table = "-ABCDEFGHIJKLMNOP"


def get_position_str(position: int) -> str:
    index = abs(position)
    checker = conv_table[index]
    if position < 0:
        checker = checker.lower()
    return checker


def get_xgid(row: dict) -> str:
    position_str = ''.join(map(get_position_str, row['Position']))
    cube = row['Doubled_Cube']
    cube_pos = row['Doubled_CubePos']
    xgid = f"XGID={position_str}:{cube}:{cube_pos}:1:00:0:0:3:0:10"
    return xgid


def get_position(xgid: str) -> List[int]:
    if not xgid.startswith('XGID='):
        return None
    parts = xgid.split(':')
    if len(parts) != 10:
        return None
    try:
        return [conv_table.index(checker) if checker.isupper() else -conv_table.index(checker.upper()) for checker in parts[0][5:]]
    except ValueError:
        return None
