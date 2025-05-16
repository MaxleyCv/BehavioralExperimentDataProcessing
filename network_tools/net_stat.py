import copy

import pandas as pd

from network_tools.tools import leave_only, search_minimal
from routines.constants import Context
from utils.timing import UET


class NetworkStatistics:
    """
    A class that will combine feature vectors that are needed from the network space
    Will use the cumulative traffic sum over the observation window.
    """
    def __init__(
        self,
        context: Context,
        host_ip: str,
        network_stat_dataframe: pd.DataFrame
    ):
        self.__context = context
        self.__host = host_ip
        self.__dataframe = network_stat_dataframe

    def read_incoming_traffic_from_host_uet(self, uet_space):

        host: str = self.__host
        dataframe: pd.DataFrame = copy.deepcopy(self.__dataframe)

        df_given_dest = dataframe[dataframe.Destination.isin([host])]

        df_filtered = leave_only(["Time", "Destination", "Length"], df_given_dest)
        times = df_filtered["Time"]
        times_usec = list(map(UET, times))
        new_times = pd.DataFrame({"time": times_usec, "length": df_filtered["Length"]})
        new_times["CumulativeLength"] = new_times["length"].cumsum()

        DIFF_USEC = self.__context.NETWORK_OBSERVATION_WINDOW_SECONDS * 10 ** 6
        T = new_times.reset_index()
        timestamps_new, lengths = [], []
        for timestamp in uet_space:
            frame_left_id = search_minimal(T.shape[0] - 1, timestamp, T, DIFF_USEC)
            frame_right_id = search_minimal(T.shape[0] - 1, timestamp, T, 0)
            timestamps_new.append(timestamp)
            difference = T.loc[frame_right_id]["CumulativeLength"] - T.loc[frame_left_id]["CumulativeLength"]
            lengths.append(difference)
        return timestamps_new, lengths

    def read_outcoming_traffic_from_host_uet(self, uet_space):

        host: str = self.__host
        dataframe: pd.DataFrame = copy.deepcopy(self.__dataframe)

        df_given_dest = dataframe[dataframe.Source.isin([host])]
        print(df_given_dest.shape)
        df_filtered = leave_only(["Time", "Source", "Length"], df_given_dest)
        times = df_filtered["Time"]
        times_usec = list(map(UET, times))
        new_times = pd.DataFrame({"time": times_usec, "length": df_filtered["Length"]})
        new_times["CumulativeLength"] = new_times["length"].cumsum()
        DIFF_USEC = self.__context.NETWORK_OBSERVATION_WINDOW_SECONDS * 10 ** 6
        T = new_times.reset_index()

        if T.shape[0] == 0:
            print(f"Shut out host {host}")
            return uet_space, [0 for _ in range(len(uet_space))]

        timestamps_new, lengths = [], []
        for timestamp in uet_space:
            frame_left_id = search_minimal(T.shape[0] - 1, timestamp, T, DIFF_USEC)
            frame_right_id = search_minimal(T.shape[0] - 1, timestamp, T, 0)
            timestamps_new.append(timestamp)
            difference = T.loc[frame_right_id]["CumulativeLength"] - T.loc[frame_left_id]["CumulativeLength"]
            lengths.append(difference)
        return timestamps_new, lengths
