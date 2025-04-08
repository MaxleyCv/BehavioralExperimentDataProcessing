import pickle
from typing import List

import numpy as np
import pandas as pd

from network_tools.net_stat import NetworkStatistics
from network_tools.tcp_conn import OpenTCPConnections
from routines.constants import Context
from routines.routine import Routine
from utils.timing import UET


class CreateNetworkFeaturesRoutine(Routine):
    def __init__(self):
        self.__context = Context()

    def __read_time_grid(self) -> List[UET]:
        with open(self.__context.UET_GRID_FILE, 'rb') as f:
            uet_space = pickle.load(f)
        return uet_space

    def execute(self) -> bool:
        uet_space: List[int] = list(map(lambda x: x(), self.__read_time_grid()))
        connections = OpenTCPConnections(
            self.__context.TCP_CONNECTIONS_FILE_PATH
        )
        network_statistics_dataframe = pd.read_csv(self.__context.ROUTER_FILE_PATH)
        for host in self.__context.ip_to_trackable_mapping:
            tag = self.__context.ip_to_trackable_mapping[host]

            network_stats = NetworkStatistics(
                context=self.__context,
                host_ip=host,
                network_stat_dataframe=network_statistics_dataframe
            )

            traffic_in = network_stats.read_outcoming_traffic_from_host_uet(uet_space)
            traffic_out = network_stats.read_outcoming_traffic_from_host_uet(uet_space)
            tcp_in = list(
                map(
                    connections.num_inc_connections_at_time_per_host,
                    [host] * len(uet_space),
                    uet_space
                )
            )
            tcp_out = list(
                map(
                    connections.num_out_connections_at_time_per_host,
                    [host] * len(uet_space),
                    uet_space
                )
            )
            host_stats = np.array([traffic_in, traffic_out, tcp_in, tcp_out]).T
            with open(self.__context.NETWORK_EMBEDDINGS + f"{tag}.emb", 'wb') as f:
                pickle.dump(host_stats.tolist(), f)

        return True
