import os

class Context:
    """
    Configuration file to manage the program
    """
    # Place for raw experimental data
    DATA_ROOT_FOLDER = 'data/'
    # Place for video recordings
    # Please abide the naming convention: videos are placed under names {0-based index_number}.mp4 in the following
    VISUAL_ROOT_FOLDER = DATA_ROOT_FOLDER + 'recordings/'
    # Place to store videos specifically
    VIDEO_ROOT_FOLDER = VISUAL_ROOT_FOLDER + 'videos/'
    # Make sure that timestamps are generated as csv file, and have the same naming convention as the videos.
    # Timestamps should make pairs. If you choose to make your own timestamps they will override existing.
    # You can use visual tools to generate timestamps by running python3 setup.py --gen-timestamps
    TIMESTAMP_ROOT_FOLDER = "tmp/extra_timestamps" \
        if len(os.listdir('tmp/extra_timestamps'))\
        else VISUAL_ROOT_FOLDER + 'timestamps/'

    # Router-based criteria.
    # The router is the gateway for all of your experimental data, to which everyone is connected.
    # You will be able to choose the address list when running setup (it will produce a file in TMP)
    # If you have multiple .pcap.gz files then first run mergecap -a in the file directory and export the file as csv
    # Make sure you use absolute timestamps with just the time of the day that is the basis of UET
    ROUTER_ROOT_FOLDER = DATA_ROOT_FOLDER + '/router'
    ROUTER_FILE_PATH = ROUTER_ROOT_FOLDER + '/captures.pcap'

    #
