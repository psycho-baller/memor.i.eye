''' Demonstrates how to subscribe to and handle data from gaze and event streams '''

import time
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageStat
from upload import upload_img

import adhawkapi
import adhawkapi.frontend
from adhawkapi import Events, MarkerSequenceMode, PacketType


def brightness(im):
    stat = ImageStat.Stat(im)
    return stat.mean[0]


class Frontend:
    ''' Frontend communicating with the backend '''

    def __init__(self):
        # Instantiate an API object
        self._api = adhawkapi.frontend.FrontendApi()

        self.take_photo = False

        # self.calibrate

        # Tell the api that we wish to tap into the GAZE data stream
        # with self._handle_gaze_data_stream as the handler
        # self._api.register_stream_handler(PacketType.GAZE, self._handle_gaze_data_stream)
 
        # Start the api and set its connection callback to self._handle_connect_response. When the api detects a
        # connection to a MindLink, this function will be run.
        self._api.start(connect_cb=self._handle_connect_response)

        self._api.register_stream_handler(PacketType.GAZE_IN_IMAGE, self._handle_gaze_in_image_stream)
                                      # self._handle_gaze_data_stream)

        self._api.register_stream_handler(PacketType.EVENTS, self._handle_event_stream)

        # setup a video receiver
        self.video_receiver = adhawkapi.frontend.VideoReceiver()
        self.video_receiver.frame_received_event.add_callback(self.frame_handler)
        self.video_receiver.start()


        # Used to limit the rate at which data is displayed in the console
        self._last_console_print = None

        # Flags the frontend as not connected yet
        self.connected = False

        self.mean = np.zeros(2)
        self.cov = np.zeros(2)

        # threshold of (trace) of cov to consider a fixation
        self.cov_threshold = 10_000
        self.mean_threshold = np.array([500, 100])
        self.past_fixation_point = np.array([-10000, -10000])

        self.fixating = False
        self.fixated_image = None
        self.fixating_start_time = 0
        self.fixating_total_time = 0

        self.num_timesteps = 64
        self.current_timestep = 0
        # stores self.num_timesteps many values of the (x,y) gaze position over time
        self.moving_data = []
        self.times = []

        print('Starting frontend...')

    def calibrate(self):
        ''' Runs a Calibration using AdHawk Backend's GUI '''

        # Two calibration modes are supported: FIXED_HEAD and FIXED_GAZE
        # With fixed head mode you look at calibration markers without moving your head
        # With fixed gaze mode you keep looking at a central point and move your head as instructed during calibration.
        self._api.start_calibration_gui(mode=MarkerSequenceMode.FIXED_HEAD, n_points=9, marker_size_mm=35,
                                        randomize=False, callback=(lambda *_args: None))

    def _handle_event_stream(self, event_type, _timestamp, *_args):
        if event_type == Events.SACCADE.value and self.fixating:
            print('############# Saccade! moved away')

            self.fixating_total_time = time.time() - self.fixating_start_time

            image = np.array(cv2.imdecode(np.frombuffer(self.fixated_image, dtype=np.uint8), 1))
            cv2.circle(image, (int(self.past_fixation_point[0]), int(self.past_fixation_point[1])), 100, (255, 255, 255), thickness=10)

            cv2.imwrite(f'fixations/{self.current_timestep}.jpg', image)
            image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
            upload_img(image_bytes, self.past_fixation_point, self.fixating_total_time)

            # reset fixation time
            self.fixating_total_time = 0
            self.fixating_start_time = 0
            self.fixating = False

    def shutdown(self):
        ''' Shuts down the backend connection '''

        # Stops api camera capture
        self._api.stop_video_stream(*self.video_receiver.address, lambda *x: None)
        self._api.stop_camera_capture(lambda *_args: None)

        # Stop the log session
        self._api.stop_log_session(lambda *_args: None)

        # Shuts down the api
        self._api.shutdown()

    def update_moving_values(self, x_pos, y_pos):
        self.moving_data += [np.array([x_pos, y_pos])]
        self.times += [time.time()]

        # remove the first element if max length is exceded
        if self.current_timestep >= self.num_timesteps:
            self.moving_data = self.moving_data[1:]  # remove first element
            self.times = self.times[1:]  # remove first element

        self.current_timestep += 1

    def _handle_gaze_in_image_stream(self, timestamp, x_pos, y_pos, *_args):
        ''' Prints gaze data to the console '''

        # # Only log at most once per second
        # if self._last_console_print and timestamp < self._last_console_print + 1:
        #     return

        self._last_console_print = timestamp

        self.update_moving_values(x_pos, y_pos)

        if self.current_timestep > self.num_timesteps:
            # get cov matrix of data
            self.cov = np.cov(np.array(self.moving_data).T)
            # print('COV', np.trace(self.cov), self.cov_threshold, np.abs(self.past_fixation_point - np.mean(self.moving_data, 0)), self.mean_threshold )

            # CHECK if deemed to be a fixation,
            # also only if it's sufficiently far from previous fixation point.
            if (
                np.trace(self.cov) < self.cov_threshold
                and np.any(np.abs(self.past_fixation_point - np.mean(self.moving_data, 0)) > self.mean_threshold)
                and not self.fixating
            ):
                # set new past fixation point
                self.past_fixation_point = np.array([x_pos, y_pos])

                print('---------')
                print('---> FIXATION FOUND', self.past_fixation_point)
                print('---------')

                # set flag to save image
                self.take_photo = True
                self.fixating = True

    def _handle_connect_response(self, error):
        ''' Handler for backend connections '''

        # Starts the camera and sets the stream rate
        if not error:
            print('Connected to AdHawk Backend Service')

            # Sets the GAZE data stream rate to 125Hz
            self._api.set_stream_control(PacketType.GAZE_IN_IMAGE, 125, callback=(lambda *args: None))

            self._api.set_event_control(adhawkapi.EventControlBit.SACCADE, 1, callback=(lambda *_args: None))

            # Starts the MindLink's camera so that a Quick Start can be performed. Note that we use a camera index of 0
            # here, but your camera index may be different, depending on your setup. On windows, it should be 0.
            self._api.start_camera_capture(camera_index=2, resolution_index=adhawkapi.CameraResolution.HIGH,
                                           correct_distortion=False, callback=self.handle_camera_start_response)

            # Starts a logging session which saves eye tracking signals. This can be very useful for troubleshooting
            self._api.start_log_session(log_mode=adhawkapi.LogMode.BASIC, callback=lambda *args: None)

            # Flags the frontend as connected
            self.connected = True

    def handle_camera_start_response(self, response):
        self.start_video_stream()
        # if response:
        #     print(f'camera start response: {response}')
        # else:
        #     print('starting video stream')
        #     self.start_video_stream()

    def start_video_stream(self):
        ''' Start the video streaming '''
        self._api.start_video_stream(*self.video_receiver.address, lambda *x: None)


    def frame_handler(self, timestamp, frame_index, image_buf, bob):
        # if registered as a fixation, write the photo to disk (for now)
        # TOOD: upload to S3
        if self.take_photo:
            # print(self.past_fixation_point, 'fixation point')

            self.take_photo = False
            self.fixating = True
            self.fixated_image = image_buf
            self.fixating_start_time = time.time()


def main():
    '''Main function'''

    frontend = Frontend()
    try:
        # print('Plug in your MindLink and ensure AdHawk Backend is running.')

        # frontend.calibrate()

        while True:
            # TODO; specify refresh interval
            # Loops while the data streams come in
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):

        # Allows the frontend to be shut down robustly on a keyboard interrupt
        frontend.shutdown()



if __name__ == '__main__':
    main()
