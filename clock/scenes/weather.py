from datetime import datetime
from rgbmatrix import graphics
from utilities.animator import Animator
from setup import colours, fonts, frames, screen
from utilities.temperature import grab_weather_data
from config import TEMPERATURE_UNITS
import colorsys

import logging

# Configure logging
#logging.basicConfig(filename='weather.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

REFRESH_SECONDS = 600
WEATHER_FONT = fonts.extrasmall
TEMPERATURE_FONT = fonts.extrasmall
WEATHER_FONT_HEIGHT = 5

class WeatherScene(object):
    def __init__(self):
        super().__init__()
        self._last_temperature = None
        self._last_temperature_str = None
        self._last_wind_speed = None
        self._last_wind_gust = None
        self._last_wind_direction = None
        self._last_current_humidity = None
        self._last_updated = None
        self._cached_data = None
        self._redraw = True

    def colour_gradient(self, colour_A, colour_B, ratio):
        return graphics.Color(
            colour_A.red + ((colour_B.red - colour_A.red) * ratio),
            colour_A.green + ((colour_B.green - colour_A.green) * ratio),
            colour_A.blue + ((colour_B.blue - colour_A.blue) * ratio),
        )

    def degrees_to_cardinal(self, d):
        dirs = ["N", "NE",  "E",  "SE", "S",  "SW",  "W",  "NW"]
        ix = int((d + 22.5) / 45)
        return dirs[ix % 8]

    def draw_square(self, x, y, width, height, color):
        # Assuming you have a draw_square method
        pass

    def determine_color(self, wind_gust, wind_speed):
        difference = wind_gust - wind_speed
        if 0 <= difference <= 5:
            return colours.GREEN
        elif 5 < difference <= 10:
            return colours.YELLOW
        else:
            return colours.RED

    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def weather_and_temperature(self, count):
        # Ensure redraw when there's new data
        if len(self._data):
            self._redraw = True
            return

        seconds_since_update = (datetime.now() - self._last_updated).seconds if self._last_updated is not None else 0
        if not (seconds_since_update % REFRESH_SECONDS) or self._redraw:
            if self._cached_data is not None and self._redraw:
                (
                    current_temperature, current_humidity,
                    wind_speed, wind_direction, wind_gust
                ) = self._cached_data
            else:
                self._cached_data = grab_weather_data()
                (
                    current_temperature, current_humidity,
                    wind_speed, wind_direction, wind_gust
                ) = self._cached_data
                self._last_updated = datetime.now()

                # Undraw old temperature and weather
                if self._last_temperature_str is not None:
                    self.draw_square(40, 0, 64, 4, colours.BLACK)
                self.draw_square(40, 32, 64, 21, colours.BLACK)

            # Temperature update logic
            if current_temperature is not None:
                self._last_temperature_str = f"{round(current_temperature)}\u00b0"
                self._last_temperature = current_temperature

                humidity_ratio = current_humidity / 100.0
                temp_colour = self.colour_gradient(colours.WHITE, colours.BLUE, humidity_ratio)

                font_character_width = 4
                temperature_string_width = len(self._last_temperature_str) * font_character_width
                middle_x = (40 + 64) // 2
                start_x = middle_x - temperature_string_width // 2
                TEMPERATURE_POSITION = (start_x, 5)

                # Draw temperature
                _ = graphics.DrawText(
                    self.canvas,
                    TEMPERATURE_FONT,
                    TEMPERATURE_POSITION[0],
                    TEMPERATURE_POSITION[1],
                    temp_colour,
                    self._last_temperature_str,
                )

            # Wind update logic
            if wind_speed is not None and wind_gust is not None:
                wind_speed_color = self.determine_color(wind_gust, wind_speed)

                if TEMPERATURE_UNITS == "imperial":
                    wind_speed_str = f"{round(wind_speed)}mph"
                elif TEMPERATURE_UNITS == "metric":
                    wind_speed_str = f"{round(wind_speed)}m/s"

                self._last_wind_info_str = wind_speed_str
                self._last_wind_info = wind_speed

                font_character_width = 4
                wind_info_width = len(self._last_wind_info_str) * font_character_width
                middle_x = (40 + 64) // 2
                start_x_speed = middle_x - wind_info_width // 2
                WIND_SPEED_POSITION = (start_x_speed, 26)

                # Draw wind speed
                _ = graphics.DrawText(
                    self.canvas,
                    WEATHER_FONT,
                    WIND_SPEED_POSITION[0],
                    WIND_SPEED_POSITION[1],
                    wind_speed_color,
                    self._last_wind_info_str,
                )

                # Draw wind direction separately
                if wind_direction is not None:
                    self._last_wind_direction_info_str = self.degrees_to_cardinal(wind_direction)
                    self._last_wind_direction_info = wind_direction
                    wind_direction_width = len(self._last_wind_direction_info_str) * font_character_width
                    start_x_direction = middle_x - wind_direction_width // 2
                    WIND_DIRECTION_POSITION = (start_x_direction, 32)  

                    # Draw wind direction
                    _ = graphics.DrawText(
                        self.canvas,
                        WEATHER_FONT,
                        WIND_DIRECTION_POSITION[0],
                        WIND_DIRECTION_POSITION[1],
                        colours.GREY,  
                        self._last_wind_direction_info_str,
                    )

                    self._redraw = False
