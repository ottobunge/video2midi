from typing import Tuple
from matplotlib.image import AxesImage
import cv2
import math

Position = Tuple[int, int]


def match_similar_color(sample, hue, threshold):
    sample_hue = sample[0]
    sample_saturation = sample[1]
    sample_brightness = sample[2]
    lower_bound = hue - threshold
    upper_bound = hue + threshold
    return sample_hue >= lower_bound and sample_hue <= upper_bound and sample_saturation > 60 and sample_brightness > 60


class PianoReader:
    def __init__(
        self,
        right_hand_color: int,
        left_hand_color: int,
        white_keys_n: int,
        black_keys_n: int,
        lowest_degree: int,
        threshold: int = 4
    ):
        self.right_hand_color = right_hand_color
        self.left_hand_color = left_hand_color
        self.white_keys_n = white_keys_n
        self.black_keys_n = black_keys_n
        self.lowest_degree = lowest_degree
        self.threshold = threshold

    def find_white_keys(self, frame: AxesImage):
        height = len(frame)
        width = len(frame[0])
        white_key_width = width / self.white_keys_n
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        first_white_key_pos = [math.floor(height * 0.82), white_key_width // 2]
        i = 5
        degree = self.lowest_degree - 2
        for white_key in range(self.white_keys_n):
            center_pixel_x = math.floor(first_white_key_pos[1] + (white_key * white_key_width))
            center_pixel_y = first_white_key_pos[0]
            spy_pixel = hsv_frame[center_pixel_y][center_pixel_x]
            if i == 0:
                degree += 1
            if i == 1:
                degree += 2
            if i == 2:
                degree += 2
            if i == 3:
                degree += 1
            if i == 4:
                degree += 2
            if i == 5:
                degree += 2
            if i == 6:
                degree += 2
            if i == 6:
                i = 0
            else:
                i += 1
            if match_similar_color(spy_pixel, self.right_hand_color, self.threshold):
                yield degree, "RIGHT", "WHITE", (center_pixel_y, center_pixel_x)
            if match_similar_color(spy_pixel, self.left_hand_color, self.threshold):
                yield degree, "LEFT", "WHITE", (center_pixel_y, center_pixel_x)

    def find_black_keys(self, frame:  AxesImage):
        height = len(frame)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        y = math.floor(height*0.5)
        i = 4
        x = 1
        degree = self.lowest_degree - 1
        for key in range(self.black_keys_n):
            if i == 0:
                x += 21
                degree += 3
            if i == 1:
                x += 15
                degree += 2
            if i == 2:
                x += 21
                degree += 3
            if i == 3:
                degree += 2
                x += 15
            if i == 4:
                x += 14
                degree += 2
            spy_pixel = hsv_frame[y][x]
            if i == 4:
                i = 0
            else:
                i += 1
            if match_similar_color(spy_pixel, self.right_hand_color, self.threshold):
                yield degree, "RIGHT", "BLACK", (y, x)
            if match_similar_color(spy_pixel, self.left_hand_color, self.threshold):
                yield degree, "LEFT", "BLACK", (y, x)

    def read(self, frame: AxesImage):
        for found in self.find_white_keys(frame):
            yield found
        for found in self.find_black_keys(frame):
            yield found
