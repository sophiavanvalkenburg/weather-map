"""
weather_parser.py

lat, long, weather_code, high_temp, low_temp
"""

import sys
from xml.etree import ElementTree


def parse_zips_to_city_codes(city_code_to_zip_fname):
    zip_to_city_codes = {}
    with open(city_code_to_zip_fname) as f:
        for line in f:
            rows = line.split("|")
            city_code = rows[2].strip()
            zip_code = rows[0].strip()
            zip_to_city_codes[zip_code] = city_code
    return zip_to_city_codes


def parse_zip_to_lat_longs(zip_to_lat_long_fname, zip_to_city_codes):
    city_code_to_lat_longs = {}
    with open(zip_to_lat_long_fname) as f:
        past_header = False
        for line in f:
            if not past_header:
                past_header = True
                continue
            rows = line.split(",")
            zip_code = rows[0].strip()
            lat = rows[1].strip()
            lon = rows[2].strip()
            city_code = zip_to_city_codes.get(zip_code)
            if city_code:
                city_code_to_lat_longs[city_code] = (lat, lon)
    return city_code_to_lat_longs


def get_weather_data(weather_fname, city_code_to_lat_longs):
    weather_data = []
    root = ElementTree.parse(weather_fname)
    forecasts = root.findall("forecast")
    for forecast in forecasts:
        city_code = forecast.find("citycode").text.strip()
        today = forecast.find("day")
        weather_code = today.find("icon").text.strip()
        high_temp = today.find("high").text.strip()
        low_temp = today.find("low").text.strip()
        latlong = city_code_to_lat_longs.get(city_code)
        if latlong:
            lat, lon = latlong
            weather_data.append([lat, lon, weather_code, high_temp, low_temp])
        else:
            print city_code
    return weather_data


def output_weather_data(output_fname, weather_data):
    with open(output_fname, "w") as f:
        for row in weather_data:
            f.write(",".join(row))
            f.write("\n")


def main(args):
    weather_fname = args[0]
    city_code_to_zip_fname = args[1]
    zip_to_lat_long_fname = args[2]
    output_fname = args[3]
    print "Getting zips to city codes"
    zip_to_city_codes = parse_zips_to_city_codes(city_code_to_zip_fname)
    print "Getting zip to lat longs"
    city_code_to_lat_longs = parse_zip_to_lat_longs(zip_to_lat_long_fname, zip_to_city_codes)
    print "Getting weather data"
    weather_data = get_weather_data(weather_fname, city_code_to_lat_longs)
    output_weather_data(output_fname, weather_data)


if __name__ == "__main__":
    main(sys.argv[1:])
