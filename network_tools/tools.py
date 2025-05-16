import copy


def leave_only(column_list, data_initial):
    data = copy.deepcopy(data_initial)
    original_column_list = data.columns
    extra = list(set(original_column_list) - set(column_list))
    data = data.drop(columns=extra)
    return data

def search_minimal(start_index, time_current, dataframe, difference_useconds):
    left_index = 0
    right_index = start_index

    target_time = time_current - difference_useconds

    while abs(left_index - right_index) > 1:
        index_mid = int(0.5 * (left_index + right_index))
        time_mid = dataframe.loc[index_mid]["time"]

        if time_mid < target_time:
            left_index = index_mid
        elif time_mid > target_time:
            right_index = index_mid
        else:
            return index_mid

    return right_index
