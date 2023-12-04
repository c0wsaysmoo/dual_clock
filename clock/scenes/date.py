from datetime import datetime

from utilities.animator import Animator
from setup import colours, fonts, frames

from rgbmatrix import graphics

# Setup
DAY_COLOUR = colours.MIDDLE_PURPLE
DATE_COLOUR = colours.ROYAL_PURPLE
DATE_FONT = fonts.extrasmall

class DateScene(object):
    def __init__(self):
        super().__init__()
        self._last_date = None

    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def date(self, count):
        if len(self._data):
            # Ensure redraw when there's new data
            self._last_date = None
        else:
            # If there's no data to display
            # then draw the date
            now = datetime.now()
            current_day = now.strftime("%A")  # Updated day format
            current_date = now.strftime("%b %-d, %Y")  # Updated date format

            # Only draw if date needs to be updated
            if self._last_date != (current_day, current_date):
                if not self._last_date is None:
                    last_day, last_date = self._last_date
                    self.draw_square(0, 10, 64, 21, colours.BLACK)

                self._last_date = (current_day, current_date)

                # Calculate middle_x for centering
                middle_x = (0 + 64) // 2

                # Draw day centered
                font_character_width = 4
                day_string_width = len(current_day) * font_character_width
                start_x = middle_x - day_string_width // 2
                DAY_POSITION = (start_x, 15)
                _ = graphics.DrawText(
                    self.canvas,
                    DATE_FONT,
                    DAY_POSITION[0],
                    DAY_POSITION[1],
                    DAY_COLOUR,
                    current_day,
                )

                # Draw date centered
                date_string_width = len(current_date) * font_character_width
                start_x = middle_x - date_string_width // 2
                DATE_POSITION = (start_x, 21)
                _ = graphics.DrawText(
                    self.canvas,
                    DATE_FONT,
                    DATE_POSITION[0],
                    DATE_POSITION[1],
                    DATE_COLOUR,
                    current_date,
                )