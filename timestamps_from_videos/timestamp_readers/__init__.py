from timestamps_from_videos.timestamp_readers.r1 import FirstVideoTimestampReader
from timestamps_from_videos.timestamp_readers.r2 import SecondVideoTimestampReader
from timestamps_from_videos.timestamp_readers.r3 import ThirdVideoTimestampReader
from timestamps_from_videos.timestamp_readers.r4 import FourthVideoTimestampReader

timestamp_readers = [
    FirstVideoTimestampReader(),
    SecondVideoTimestampReader(),
    ThirdVideoTimestampReader(),
    FourthVideoTimestampReader()

]