import json
import os

class Context:
    """
    Configuration file to manage the program
    """
    # Where to place your dataset
    RESULT_FILENAME = 'result/dataset.csv'
    # Place for raw experimental data
    DATA_ROOT_FOLDER = 'data/'
    TEMPORARY_ROOT_FOLDER = 'tmp/'
    # Place for video recordings
    # Please abide the naming convention: videos are placed under names {0-based index_number}.mp4 in the following
    VISUAL_ROOT_FOLDER = DATA_ROOT_FOLDER + 'recordings/'
    # Place to store videos specifically
    VIDEO_ROOT_FOLDER = VISUAL_ROOT_FOLDER + 'videos/'
    # Make sure that timestamps are generated as csv file, and have the same naming convention as the videos.
    # Timestamps should make pairs. If you choose to make your own timestamps they will override existing.
    # You can use visual tools to generate timestamps by running python3 setup.py --gen-timestamps
    TIMESTAMP_ROOT_FOLDER = "tmp/extra_timestamps/" \
        if len(os.listdir('tmp/extra_timestamps/'))\
        else VISUAL_ROOT_FOLDER + 'timestamps/'

    UET_ROOT_FOLDER = TEMPORARY_ROOT_FOLDER + "uets_by_video/"

    # Considering any timestamps, sometimes they are reliable, sometimes they are not.
    # Therefore this measure will stop some of the early frames from loading to the memory.
    # Basically a first skip in time
    # Needs to be exactly the size of num_videos
    TIMESTAMP_CUTOFF_FRAMES = [93,92,103,36]

    # Router-based criteria.
    # The router is the gateway for all of your experimental data, to which everyone is connected.
    # You will be able to choose the address list when running setup (it will produce a file in TMP)
    # If you have multiple .pcap.gz files then first run mergecap -aw in the file directory and export the file as csv
    # Make sure you use absolute timestamps with just the time of the day that is the basis of UET
    ROUTER_ROOT_FOLDER = DATA_ROOT_FOLDER + 'router/'
    ROUTER_FILE_PATH = ROUTER_ROOT_FOLDER + 'captures.csv'
    TCP_CONNECTIONS_FILE_PATH = ROUTER_ROOT_FOLDER + 'tcp_conn.csv'

    # Homographies for cartesian coordinate warps per video
    HOMOGRAPHY_ROOT_FOLDER = TEMPORARY_ROOT_FOLDER + "homographies/"

    # Poses will need to be yielded at some point
    POSE_ROOT_FOLDER = TEMPORARY_ROOT_FOLDER + "poses/"

    # Number of used videos
    NUMBER_OF_VIDEOS = 4

    # A place to decompose the videos by frame as this is useful for identity assignment
    VIDEO_DECOMPOSITION_ROOT_FOLDER = TEMPORARY_ROOT_FOLDER + "videos_by_frame/"

    # You need to plant some groud truth for the initial assignment.
    # You will be able to mix up different devices further in identity assignment.
    # You need to fill out your manifest.json for proper assignments across various fields.
    GROUND_TRUTH_MANIFEST_FILE = DATA_ROOT_FOLDER + "manifest.json"

    # These are primarily used in data aggregation and will be mostly within the inner workings
    PRIMARY_FEATURE_VECTORS_PER_VIDEO_PATH = TEMPORARY_ROOT_FOLDER + "embeddings-per-video/"
    VISUAL_EMBEDDINGS_COMBINED_PATH = TEMPORARY_ROOT_FOLDER + "visual-embeddings/"
    EXTRA_TIMESTAMPS_FOLDER = TEMPORARY_ROOT_FOLDER + "extra_timestamps/"
    NETWORK_EMBEDDINGS = TEMPORARY_ROOT_FOLDER + "network-embeddings/"

    UET_GRID_FILE = TEMPORARY_ROOT_FOLDER + "timegrid.uets"


    # Now observation windows
    MOVEMENT_OBSERVATION_WINDOW_SECONDS = 4
    NETWORK_OBSERVATION_WINDOW_SECONDS = 4

    # VERY IMPORTANT: FINAL FILE TIME INTERVAL:
    TIME_STEP_INTERVAL_USECONDS = int(1 / 15 * 10 ** 6)

    def __init__(self):
        with open(self.GROUND_TRUTH_MANIFEST_FILE, 'r') as f:
            self.trackables = json.load(f)["trackable_identities"]
            self.ip_to_trackable_mapping = {trackable["ip"]: trackable["tag"] for trackable in self.trackables}
            self.keys = set(self.ip_to_trackable_mapping.values())
            # necessary config conditions for evaluation
            assert len(self.TIMESTAMP_CUTOFF_FRAMES) == self.NUMBER_OF_VIDEOS
