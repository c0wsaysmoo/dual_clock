from datetime import datetime, timedelta
from utilities.animator import Animator
from setup import colours, fonts, frames, screen
from utilities.temperature import grab_forecast, grab_rain

from rgbmatrix import graphics

import logging

# Configure logging
#logging.basicConfig(filename='rain.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Setup
TEXT_FONT = fonts.extrasmall
DISTANCE_FROM_TOP = 10
RAIN_REFRESH = 600


class RainScene(object):
    def __init__(self):
        super().__init__()
        self._last_refresh_time = None
        self._cached_forecast = None
        self._last_rain = None
        self._last_rain_str = None
        self._redraw_forecast = True
        self._seconds_since_update = 0  # Initialize the counter
        self._cached_rain = None
        self._last_hour = None

    def colour_gradient(self, colour_A, colour_B, ratio):
        return graphics.Color(
            colour_A.red + ((colour_B.red - colour_A.red) * ratio),
            colour_A.green + ((colour_B.green - colour_A.green) * ratio),
            colour_A.blue + ((colour_B.blue - colour_A.blue) * ratio),
        )

    @Animator.KeyFrame.add(frames.PER_SECOND)
    def rain(self, elapsed_time):
        # Increment the counter
        self._seconds_since_update += 1
        current_hour = datetime.now().hour

        # Check for regular time-based refresh every RAIN_REFRESH seconds
        if self._seconds_since_update >= RAIN_REFRESH or self._redraw_forecast:
            #logging.debug("Refreshing rain data and forecast...")
            self._seconds_since_update = 0

            # Reset _redraw_forecast to True after regular refresh
            self._redraw_forecast = True

            # Grab forecast and rain data every RAIN_REFRESH seconds
            #logging.debug("Making API call for new forecast and rain data...")
            forecast = grab_forecast()
            rain_chance = grab_rain()

            if forecast is not None:
                self._cached_forecast = forecast
                self._redraw_forecast = False
                #logging.debug(f"Forecast Data: {forecast}")

            if rain_chance is not None:
                self._cached_rain = rain_chance
                #logging.debug(f"Rain Data: {rain_chance}")

            current_day_data = rain_chance[0]
            #logging.debug(f"Current Day Data: {current_day_data}")

            # Undraw old precipitation probability
            if self._last_rain_str is not None:
                self.draw_square(40, 5, 64, 9, colours.BLACK)

            # Extract forecast
            current_hour_data = forecast[0]
            precipitation_probability = current_hour_data['values']['precipitationProbability']

            # Store last precipitation probability
            self._last_rain = precipitation_probability

            # Format the string
            self._last_rain_str = f"{precipitation_probability * 0.01:.0%}"

            rain_ratio = current_day_data["values"]["precipitationProbability"] / 100.0
            rain_colour = self.colour_gradient(colours.WHITE, colours.BLUE, rain_ratio)

            # Calculate the offset to center the text
            space_width = 4
            rain_width = len(self._last_rain_str) * space_width
            offset = (40 + 64) // 2 - rain_width // 2

            # Draw precipitation probability for the current hour
            _ = graphics.DrawText(
                self.canvas,
                TEXT_FONT,
                offset,
                DISTANCE_FROM_TOP,
                rain_colour,
                self._last_rain_str
            )

        # Forced redraw conditions
        if self._redraw_forecast:
            logging.debug("Forcing redraw of forecast...")
            self._redraw_forecast = False