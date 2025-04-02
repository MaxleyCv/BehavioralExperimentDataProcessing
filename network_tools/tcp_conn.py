import pandas as pd

from network_tools.tools import leave_only


class OpenTCPConnections:
    """
    Open TCP connections database for Wireshark statistics TCP flow capture
    """
    def __init__(self, tcp_connections_file: str):
        connection_sheet = pd.read_csv(tcp_connections_file)
        connection_sheet["start"] = list(map(self.__timestamp_to_uet_mapping_for_tcp, connection_sheet["Abs Start"].to_numpy()))
        connection_sheet["end"] = list(map(int, connection_sheet["start"].to_numpy() + 10 ** 6 * connection_sheet['Duration'].to_numpy()))
        self.connection_sheet = leave_only(["start", "end", "Address A", "Address B"], connection_sheet)

    def __timestamp_to_uet_mapping_for_tcp(self, timestamp: str) -> int:
        """
        Since Wireshark gives a different type of Timestamp into TCP connections capture, this is UET of that type.
        :param timestamp: timestamp from Wireshark statistics -> tcp connections -> enable absolute
        :return: UET of the timeframe
        """
        time = timestamp.split("T")[1]
        h, m, s = time.split(":")
        sec, msec = map(int, s.split("."))
        time_usec = msec * 10 ** 3 + 10 ** 6 * sec + 10 ** 6 * 60 * int(m) + int(h) * 3600 * 10 ** 6
        return time_usec

    def num_inc_connections_at_time_per_host(self, host: str, time: int) -> int:
        """
        Query to find number of current connections (incoming) for a given host IP at a given time
        :param host: IP string
        :param time: UET at a given time
        :return: number of current connections
        """
        connections = self.connection_sheet[self.connection_sheet["Address B"] == host]
        num_connections = 0
        for idx, instance in connections.iterrows():
            if instance["start"] < time < instance["end"]:
                num_connections += 1
        return num_connections

    def num_out_connections_at_time_per_host(self, host: str, time: int) -> int:
        """
        Query to find number of current connections (out coming) for a given host IP at a given time
        :param host: IP string
        :param time: UET at a given time
        :return: number of current connections
        """
        connections = self.connection_sheet[self.connection_sheet["Address A"] == host]
        num_connections = 0
        for idx, instance in connections.iterrows():
            if instance["start"] < time < instance["end"]:
                num_connections += 1
        return num_connections
