import csv
import pickle

from routines.constants import Context
from routines.routine import Routine


class CombineNetworkAndVisualRoutine(Routine):
    """
    Final routine to read both network and visual contents. This just combines the two.
    """
    def __init__(self):
        self.__context = Context()

    def execute(self) -> bool:
        host_names = self.__context.keys
        embeddings = [
            ["UET", "angLA", "angRA", "angSE", "angNB", "bbwh", "area_norm", "traffic_in", "traffic_out", "tcp_in", "tcp_out", "personID"]
        ]
        for host_name in host_names:
            with open(self.__context.NETWORK_EMBEDDINGS + f"{host_name}.emb", 'rb') as f:
                network_component = pickle.load(f)
            with open(self.__context.VISUAL_EMBEDDINGS_COMBINED_PATH + f"{host_name}.emb", 'rb') as f:
                visual_component = pickle.load(f)
            for net_features, visual_features in zip(network_component, visual_component):
                embeddings.append(
                    [
                        *visual_features, *net_features, host_name
                    ]
                )

        with open(self.__context.RESULT_FILENAME, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(embeddings)

        return True
