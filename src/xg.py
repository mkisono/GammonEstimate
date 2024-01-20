def get_position_str(position):
    index = abs(position)
    conv_table = "-ABCDEFGHIJKLMNOP"
    checker = conv_table[index]
    if position < 0:
        checker = checker.lower()
    return checker


def get_xgid(row):
    position_str = ''.join(map(get_position_str, row['Position']))
    cube = row['Doubled_Cube']
    cube_pos = row['Doubled_CubePos']
    xgid = f"XGID={position_str}:{cube}:{cube_pos}:1:00:0:0:3:0:10"
    return xgid
