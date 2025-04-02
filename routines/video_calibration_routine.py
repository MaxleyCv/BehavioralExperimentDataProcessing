from routines.constants import Context
from routines.routine import Routine
from utils.capture import Capture
from utils.command_line_interface import CommandInterface
import cv2

from video_warps.selector_function import SelectorFunction
from video_warps.video_warp import VideoWarp


class VideoCalibrationRoutine(Routine):
    """
    This routine will start the process of finding homography warps for coordinate calculations based on the floor.
    Needed by visual feature producer.
    """
    def __init__(self, n_videos: int):
        context = Context()
        self.__video_list = [context.VIDEO_ROOT_FOLDER + f"{i}.mp4" for i in range(n_videos)]
        self.__n_videos = n_videos
        self.__detections = []
        self.__context = context
        self.status = False

    def execute(self) -> int:
        self.status = True
        for video_id in range(self.__n_videos):
            self.status = self.status and self.__start_interface_per_video(video_id)
            if self.status:
                # Now, I know this is very weird but is needed to load module
                selector_function: SelectorFunction
                COMMAND = f"from video_warps.children.{video_id} import selector_function"
                try:
                    exec(COMMAND)
                except Exception as e:
                    print(e)
                    print(f"Sorry! Function not found for video id {video_id}")
                    raise e

                # just initialization of this class is enough to compute and save homography
                VideoWarp(
                    self.__context,
                    self.__detections[-1],
                    selector_function,
                    video_id
                )
            else:
                break
        return self.status

    def __start_interface_per_video(self, video_id: int) -> bool:
        """
        A small interactive interface to select the points matching
        :param video_id:
        :return:
        """
        interface = CommandInterface(f"Computing homographies for video {video_id}")
        interface.write_instruction(f"Please make sure that you have created {video_id}.py in video_warps/children")
        interface.write_instruction("Showing on the image is a sample of your video. A - nice frame, D - change.")

        video = cv2.VideoCapture(self.__video_list[video_id])
        _, frame = video.read()
        window_name = f"{video_id} - selection"
        while True:
            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('a') or key == ord('A'):
                # a special case if this is the end of the video
                ret, frame = video.read()
                if not ret:
                    interface.write_instruction("Wow! You finished the video. Goodbye LOL :)")
                    return False
            elif key == ord('d') or key == ord('D'):
                interface.write_instruction("Now we can continue to select the clicks.")
                break

        interface.write_instruction("Now capture your points. Never click!")
        capture = Capture(window_name, frame)
        cv2.imshow(window_name, capture)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        interface.write("Are you satisfied or one more? y/n")
        response = interface.read_symbol()
        if response == 'n':
            return self.__start_interface_per_video(video_id)

        self.__detections.append(capture.detections)
        return True

    def __del__(self):
        cv2.destroyAllWindows()
