from datetime import datetime
import pytz  # Add this import for time zone support

from utilities.animator import Animator
from setup import colours, fonts, frames

from rgbmatrix import graphics

# Setup
CLOCK_FONT = fonts.large_bold
CLOCK_COLOUR_ORD = colours.SEA_GREEN
CLOCK_COLOUR_PDX = colours.FOREST_GREEN

class ClockScene(object):
    def __init__(self):
        super().__init__()
        self._last_time_portland = None
        self._last_time_chicago = None

    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def clock(self, count):
        # Get the current time for Portland, Oregon
        portland_time = datetime.now(pytz.timezone('America/Los_Angeles'))
        current_time_portland = portland_time.strftime("%l:%M")

        # Get the current time for Chicago
        chicago_time = datetime.now(pytz.timezone('America/Chicago'))
        current_time_chicago = chicago_time.strftime("%l:%M")

        # Draw Portland time
        if self._last_time_portland != current_time_portland:
            if not self._last_time_portland is None:
                _ = graphics.DrawText(
                    self.canvas,
                    CLOCK_FONT,
                    0,
                    32,
                    colours.BLACK,
                    self._last_time_portland,
                )
            self._last_time_portland = current_time_portland

            _ = graphics.DrawText(
                self.canvas,
                CLOCK_FONT,
                0,
                32,
                CLOCK_COLOUR_PDX,
                current_time_portland,
            )

        # Draw Chicago time
        if self._last_time_chicago != current_time_chicago:
            if not self._last_time_chicago is None:
                _ = graphics.DrawText(
                    self.canvas,
                    CLOCK_FONT,
                    0,
                    10,
                    colours.BLACK,
                    self._last_time_chicago,
                )
            self._last_time_chicago = current_time_chicago

            _ = graphics.DrawText(
                self.canvas,
                CLOCK_FONT,
                0,
                10,
                CLOCK_COLOUR_ORD,
                current_time_chicago,
            )