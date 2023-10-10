'''
Display a gaze marker on the camera/scene video. Demonstrates how to receive frames from the camera, map gaze data onto
a camera frame, and draw a gaze marker.
'''

import adhawkapi
import adhawkapi.frontend
from adhawkapi import MarkerSequenceMode, PacketType

import time

from PIL import Image, ImageStat

import requests

def brightness(im):
    stat = ImageStat.Stat(im)
    return stat.mean[0]


MARKER_SIZE = 20  # Diameter in pixels of the gaze marker
MARKER_COLOR = (0, 250, 50)  # Colour of the gaze marker


class Frontend:
    ''' Frontend communicating with the backend '''

    def __init__(self, handle_pupil, video_receiver_address, gaze_handler):
        # Instantiate an API object
        self._api = adhawkapi.frontend.FrontendApi()

        # Tell the api that we wish to tap into the GAZE_IN_IMAGE data stream with the given callback as the handler
        self._api.register_stream_handler(PacketType.PUPIL_DIAMETER, handle_pupil)
        self._api.register_stream_handler(PacketType.GAZE_IN_IMAGE, gaze_handler)

        # Start the api and set its connection callback to self._handle_connect. When the api detects a connection to a
        # tracker, this function will be run.
        self._api.start(connect_cb=self._handle_connect_response)

        # Stores the video receiver's address
        self._video_receiver_address = video_receiver_address

        # Flags the frontend as not connected yet
        self.connected = False

    def shutdown(self):
        ''' Shuts down the backend connection '''

        # Stops the video stream
        self._api.stop_video_stream(*self._video_receiver_address, lambda *_args: None)

        # Stops api camera capture
        self._api.stop_camera_capture(lambda *_args: None)

        # Stop the log session
        self._api.stop_log_session(lambda *_args: None)

        # Shuts down the api
        self._api.shutdown()

    def quickstart(self):
        ''' Runs a Quick Start using AdHawk Backend's GUI '''

        # The tracker's camera will need to be running to detect the marker that the Quick Start procedure will display
        self._api.quick_start_gui(mode=MarkerSequenceMode.FIXED_GAZE, marker_size_mm=35,
                                  callback=(lambda *_args: None))

    def calibrate(self):
        ''' Runs a Calibration using AdHawk Backend's GUI '''

        # Two calibration modes are supported: FIXED_HEAD and FIXED_GAZE
        # With fixed head mode you look at calibration markers without moving your head
        # With fixed gaze mode you keep looking at a central point and move your head as instructed during calibration.
        self._api.start_calibration_gui(mode=MarkerSequenceMode.FIXED_HEAD, n_points=9, marker_size_mm=35,
                                        randomize=False, callback=(lambda *_args: None))

    def _handle_connect_response(self, error):

        # Starts the camera and sets the stream rate
        if not error:

            # Sets the GAZE_IN_IMAGE data stream rate to 125Hz
            self._api.set_stream_control(PacketType.PUPIL_DIAMETER, 125, callback=(lambda *args: None))
            self._api.set_stream_control(PacketType.GAZE_IN_IMAGE, 125, callback=(lambda *args: None))

            # Starts the tracker's camera so that video can be captured and sets self._handle_camera_start_response as
            # the callback. This function will be called once the api has finished starting the camera.
            self._api.start_camera_capture(camera_index=2, resolution_index=adhawkapi.CameraResolution.HIGH,
                                           correct_distortion=False, callback=self._handle_camera_start_response)

            # Starts a logging session which saves eye tracking signals. This can be very useful for troubleshooting
            self._api.start_log_session(log_mode=adhawkapi.LogMode.BASIC, callback=lambda *args: None)

            # Flags the frontend as connected
            self.connected = True

    def _handle_camera_start_response(self, error):

        self._api.start_video_stream(*self._video_receiver_address, lambda *_args: None)

        # return
        # # Handles the response after starting the tracker's camera
        # if error:
        #     # End the program if there is a camera error
        #     print(f'Camera start error: {error}')
        #     self.shutdown()
        #     sys.exit()
        # else:
        #     # Otherwise, starts the video stream, streaming to the address of the video receiver
        #     self._api.start_video_stream(*self._video_receiver_address, lambda *_args: None)
COV_TRESHOLD = 10_000

start = True
x_data = 0
y_data = 0
fixation_start_timestamp = 0
fixated = False
fixated_x = 0
fixated_y = 0
fixated_time = 0

g_left = 0
g_right = 0


def _handle_pupil(_timestamp, right_pupil, left_pupil):
    global g_left
    global g_right
    g_right = right_pupil
    g_left = left_pupil

def _handle_video_stream(_gaze_timestamp, _frame_index, image_buf, _frame_timestamp):
    global fixated
    if fixated:
        fixated = False
        requests.post('http://20.25.130.61/test_photo', data=image_buf, params={
            'time': time.time(),
            'gaze_x': fixated_x,
            'gaze_y': fixated_y,
            'fixating_time': fixated_time,
        })


def _handle_gaze(timestamp, xpos, ypos, xdegtopix, ydegtopix):
    global x_data, y_data, fixation_start_timestamp, start, fixated, fixated_x, fixated_y, fixated_time
    if start:
        start = False
        x_data = xpos
        y_data = ypos
        fixation_start_timestamp = timestamp
        return
    x_diff = x_data - xpos
    y_diff = y_data - ypos
    move_euclid = x_diff * x_diff + y_diff * y_diff
    if move_euclid > 1000:
        if timestamp - fixation_start_timestamp > 1:
            print("fixated for ", timestamp - fixation_start_timestamp)
            fixated = True
            fixated_x = x_data
            fixated_y = y_data
            fixated_time = timestamp - fixation_start_timestamp
        fixation_start_timestamp = timestamp
        x_data = xpos
        y_data = ypos


def main():
    _video_receiver = adhawkapi.frontend.VideoReceiver()
    _video_receiver.frame_received_event.add_callback(_handle_video_stream)
    _video_receiver.start()
    frontend = Frontend(_handle_pupil, _video_receiver.address, _handle_gaze)
    frontend.quickstart()
    frontend.calibrate()
    try:
        while True:
            time.sleep(1)
    except:
        frontend.shutdown()

if __name__ == '__main__':
    main()
