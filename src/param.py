def get_id(query_params, num_positions):
    value = query_params.get('id')
    if value is None:
        return None
    try:
        position_id = int(value[0])
        if position_id < 0 or position_id >= num_positions:
            return None
        return position_id
    except (ValueError, IndexError):
        return None
