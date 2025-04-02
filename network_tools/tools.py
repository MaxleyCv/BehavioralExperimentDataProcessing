def leave_only(column_list, data):
    original_column_list = data.columns
    extra = list(set(original_column_list) - set(column_list))
    data = data.drop(columns=extra)
    return data