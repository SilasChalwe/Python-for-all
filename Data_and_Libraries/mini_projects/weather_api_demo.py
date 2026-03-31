"""
Mini Project — Weather API Demo
=================================
Demonstrates using the `requests` library to fetch and display weather data
from a public API. Uses Open-Meteo (free, no API key required).

Skills: requests, JSON parsing, error handling, data formatting

Open-Meteo API: https://open-meteo.com/
"""

import requests
import json
from datetime import datetime

# ==============================================================================
# WEATHER CLIENT
# ==============================================================================

class WeatherClient:
    """
    Fetches weather data from Open-Meteo API.
    No API key required — completely free.
    """

    BASE_URL     = "https://api.open-meteo.com/v1"
    GEOCODE_URL  = "https://geocoding-api.open-meteo.com/v1"

    # WMO weather interpretation codes
    WMO_CODES = {
        0:  ("Clear sky",             "☀️"),
        1:  ("Mainly clear",          "🌤️"),
        2:  ("Partly cloudy",         "⛅"),
        3:  ("Overcast",              "☁️"),
        45: ("Foggy",                 "🌫️"),
        48: ("Icy fog",               "🌫️"),
        51: ("Light drizzle",         "🌦️"),
        53: ("Moderate drizzle",      "🌦️"),
        55: ("Dense drizzle",         "🌧️"),
        61: ("Slight rain",           "🌧️"),
        63: ("Moderate rain",         "🌧️"),
        65: ("Heavy rain",            "🌧️"),
        71: ("Slight snow",           "🌨️"),
        73: ("Moderate snow",         "❄️"),
        75: ("Heavy snow",            "❄️"),
        77: ("Snow grains",           "❄️"),
        80: ("Slight showers",        "🌦️"),
        81: ("Moderate showers",      "🌧️"),
        82: ("Violent showers",       "⛈️"),
        85: ("Slight snow showers",   "🌨️"),
        86: ("Heavy snow showers",    "❄️"),
        95: ("Thunderstorm",          "⛈️"),
        96: ("Thunderstorm w/ hail",  "⛈️🌨️"),
        99: ("Thunderstorm w/ heavy hail", "⛈️🌨️"),
    }

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "PythonForAll-WeatherDemo/1.0"
        })

    def _get(self, url: str, params: dict) -> dict:
        """Make a GET request and return parsed JSON."""
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Cannot connect. Check your internet connection.")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"HTTP {e.response.status_code}: {e.response.reason}")

    def get_coordinates(self, city: str) -> dict:
        """Look up latitude/longitude for a city name."""
        data = self._get(
            f"{self.GEOCODE_URL}/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"}
        )
        results = data.get("results")
        if not results:
            raise ValueError(f"City not found: '{city}'")
        r = results[0]
        return {
            "name":      r.get("name"),
            "country":   r.get("country"),
            "latitude":  r.get("latitude"),
            "longitude": r.get("longitude"),
            "timezone":  r.get("timezone"),
        }

    def get_current_weather(self, latitude: float, longitude: float,
                             timezone: str = "auto") -> dict:
        """Fetch current weather conditions."""
        data = self._get(
            f"{self.BASE_URL}/forecast",
            params={
                "latitude":         latitude,
                "longitude":        longitude,
                "timezone":         timezone,
                "current_weather":  True,
                "current":          (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,precipitation,"
                    "wind_speed_10m,wind_direction_10m,weather_code"
                ),
            }
        )
        return data.get("current", {})

    def get_forecast(self, latitude: float, longitude: float,
                     days: int = 7, timezone: str = "auto") -> dict:
        """Fetch daily weather forecast."""
        data = self._get(
            f"{self.BASE_URL}/forecast",
            params={
                "latitude":             latitude,
                "longitude":            longitude,
                "timezone":             timezone,
                "forecast_days":        days,
                "daily": (
                    "temperature_2m_max,temperature_2m_min,"
                    "precipitation_sum,weather_code,wind_speed_10m_max"
                ),
            }
        )
        return data.get("daily", {})

    def describe_weather(self, code: int) -> tuple:
        """Return (description, emoji) for a WMO weather code."""
        return self.WMO_CODES.get(code, ("Unknown", "❓"))


class WeatherApp:
    """Display weather information in a user-friendly format."""

    def __init__(self):
        self.client = WeatherClient()

    def display_current(self, city: str):
        """Print current weather for a city."""
        print(f"\n  Fetching weather for: {city}...")
        try:
            location = self.client.get_coordinates(city)
            current  = self.client.get_current_weather(
                location["latitude"],
                location["longitude"],
                timezone=location.get("timezone", "auto")
            )

            wmo_code = current.get("weather_code", 0)
            desc, emoji = self.client.describe_weather(wmo_code)

            print("\n" + "=" * 50)
            print(f"  {emoji}  WEATHER IN {location['name'].upper()}, {location['country'].upper()}")
            print("=" * 50)
            print(f"  Condition:    {desc} {emoji}")
            print(f"  Temperature:  {current.get('temperature_2m', 'N/A')}°C")
            print(f"  Feels like:   {current.get('apparent_temperature', 'N/A')}°C")
            print(f"  Humidity:     {current.get('relative_humidity_2m', 'N/A')}%")
            print(f"  Precipitation:{current.get('precipitation', 0)} mm")
            print(f"  Wind speed:   {current.get('wind_speed_10m', 'N/A')} km/h")
            print(f"  Wind dir:     {current.get('wind_direction_10m', 'N/A')}°")
            print(f"  Updated:      {current.get('time', 'N/A')}")

        except (ConnectionError, ValueError) as e:
            print(f"  ❌ Error: {e}")

    def display_forecast(self, city: str, days: int = 5):
        """Print a multi-day forecast for a city."""
        print(f"\n  Fetching {days}-day forecast for: {city}...")
        try:
            location = self.client.get_coordinates(city)
            forecast = self.client.get_forecast(
                location["latitude"],
                location["longitude"],
                days=days,
                timezone=location.get("timezone", "auto")
            )

            dates      = forecast.get("time", [])
            temp_max   = forecast.get("temperature_2m_max", [])
            temp_min   = forecast.get("temperature_2m_min", [])
            precip     = forecast.get("precipitation_sum", [])
            wmo_codes  = forecast.get("weather_code", [])
            wind_speed = forecast.get("wind_speed_10m_max", [])

            print(f"\n  📅 {days}-Day Forecast for {location['name']}, {location['country']}")
            print("  " + "-" * 60)
            print(f"  {'Date':<12} {'Cond':<20} {'High':>5} {'Low':>5} {'Rain':>6} {'Wind':>8}")
            print("  " + "-" * 60)

            for i, date in enumerate(dates[:days]):
                _, emoji = self.client.describe_weather(wmo_codes[i] if wmo_codes else 0)
                desc, _  = self.client.describe_weather(wmo_codes[i] if wmo_codes else 0)
                hi   = f"{temp_max[i]:.0f}°C"  if temp_max  else "N/A"
                lo   = f"{temp_min[i]:.0f}°C"  if temp_min  else "N/A"
                rain = f"{precip[i]:.1f}mm"     if precip    else "N/A"
                wind = f"{wind_speed[i]:.0f}k/h" if wind_speed else "N/A"
                cond = f"{emoji} {desc[:15]}"
                print(f"  {date:<12} {cond:<20} {hi:>5} {lo:>5} {rain:>6} {wind:>8}")

        except (ConnectionError, ValueError) as e:
            print(f"  ❌ Error: {e}")


def main():
    """Run the weather demo."""
    print("=" * 50)
    print("  🌍  WEATHER APP DEMO")
    print("=" * 50)

    app = WeatherApp()

    # Demo with a few cities
    demo_cities = ["Lusaka", "London", "Tokyo"]

    for city in demo_cities:
        app.display_current(city)
        print()

    # Show forecast for first city
    app.display_forecast(demo_cities[0], days=5)


if __name__ == "__main__":
    main()
