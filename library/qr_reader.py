import time
import datetime
from pyzbar import pyzbar
from imutils.video import VideoStream

class QRReader:
    def __init__(self):
        self.video_stream = VideoStream(src=0).start()
        time.sleep(1.0)
        self.previous_order = 'A 0'
        self.time_of_first_blanc = datetime.datetime.now()
        self.time_of_last_oder = datetime.datetime.now()

    def read(self):
        frame = self.video_stream.read()
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)
        if barcodes:
            data = barcodes[0].data.decode("utf-8")
        else:
            data = ''
        new_order = 'A 0'
        if data:
            if data != self.previous_order:
                new_order = data
                self.previous_order = new_order
            self.time_of_last_oder = datetime.datetime.now()
        if data == "":
            self.time_of_first_blanc = datetime.datetime.now()
            if (self.time_of_first_blanc - self.time_of_last_oder) > datetime.timedelta(seconds=3):
                self.previous_order = 'A 0'
        return new_order

    def stop(self):
        self.video_stream.stop()
