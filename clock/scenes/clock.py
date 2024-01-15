from datetime import datetime
import pytz  # Add this import for time zone support
from utilities.animator import Animator
from setup import colours, fonts, frames
from rgbmatrix import graphics
from config import LOCAL_TIME
from config import SECOND_TIME
from config import CLOCK_FORMAT

# Setup
CLOCK_FONT = fonts.large_bold
CLOCK_COLOUR_1 = colours.SEA_GREEN
CLOCK_COLOUR_2 = colours.FOREST_GREEN

class ClockScene(object):
    def __init__(self):
        super().__init__()
        self._last_time_second = None
        self._last_time_first = None

    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def clock(self, count):
        # Get the current time for second
        second_time = datetime.now(pytz.timezone(SECOND_TIME))
        current_time_second = second_time.strftime("%l:%M" if CLOCK_FORMAT == "12hr" else "%H:%M")

        # Get the current time for first
        first_time = datetime.now(pytz.timezone(LOCAL_TIME))
        current_time_first = first_time.strftime("%l:%M" if CLOCK_FORMAT == "12hr" else "%H:%M")

        # Draw second time
        if self._last_time_second != current_time_second:
            if not self._last_time_second is None:
                _ = graphics.DrawText(
                    self.canvas,
                    CLOCK_FONT,
                    0,
                    32,
                    colours.BLACK,
                    self._last_time_second,
                )
            self._last_time_second = current_time_second

            _ = graphics.DrawText(
                self.canvas,
                CLOCK_FONT,
                0,
                32,
                CLOCK_COLOUR_2,
                current_time_second,
            )

        # Draw first time
        if self._last_time_first != current_time_first:
            if not self._last_time_first is None:
                _ = graphics.DrawText(
                    self.canvas,
                    CLOCK_FONT,
                    0,
                    10,
                    colours.BLACK,
                    self._last_time_first,
                )
            self._last_time_first = current_time_first

            _ = graphics.DrawText(
                self.canvas,
                CLOCK_FONT,
                0,
                10,
                CLOCK_COLOUR_1,
                current_time_first,
            )