"""
Charlotte Action Functions
==========================

This module represents set of actions the Assistant can perform.
The module has 8 functions:
    - age               : Calculates the age
    - locate            : Locates the position of the user
    - find              : Finds the approximate `file name` in a directory
    - play_music        : Plays music from `D:/Music` directory
    - current_weather   : Returns current weather condition
    - forecast_weather  : Returns weather forecast for next 5 hours
    - current_forecast_weather: Returns current weather and forecast
    - wish_user         : Wishes user based on time of the day

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exc_info

from charlotte.utils.paths.directories import local_dir
from charlotte.utils.paths.files import ai_file
from charlotte.utils.profiles.user import title


def age(birthdate: str) -> int:
    """
    Definition
    ----------
        Calculates the age based on the birthdate provided.

    Parameter
    ---------
        birthdate : string, mandatory
            Birthdate in string format. The birthdate needs to be ISO 8601
            format.

    Returns
    -------
        age : integer, default
            Returns age in integer format.

    Notes
    -----
        This age calculation is used while building profile.
    """
    from datetime import date

    try:
        days_in_year = 365.2425
        year = int(birthdate.split('-')[0])
        month = int(birthdate.split('-')[1])
        day = int(birthdate.split('-')[2])
        age = int((date.today() - date(year, month, day)).days / days_in_year)
        return age
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def locate(area: str = None) -> str:
    """
    Definition
    ----------
        Returns current location using reverse lookup via Google Maps API.

    Parameter
    ---------
        area : string, optional
            Looks for specific details of an address while locating.
            Global default: False

    Returns
    -------
        Depending upon passed value, function returns specific address related
        information.

    Notes
    -----
        Function uses Google Maps for retreiving latitude and longitude using
        Google Maps API. Hence it is necessary to generate the API key.
        You can generate it here: `https://console.developers.google.com`
    """
    import os
    from geocoder import osm
    from googlemaps import Client

    try:
        gmaps = Client(key=os.environ.get('CHARLOTTE_MAPS'))
        current_coords = gmaps.geolocate()
        location = osm(
            list(current_coords['location'].values()), method='reverse')
        if area is not None:
            try:
                return location.json[area]
            except:
                return 'null'
        else:
            try:
                return location.json['address']
            except:
                return 'null'
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def find(file: str, file_dir: str, min_score: int = 65) -> tuple:
    """
    Definition
    ----------
        Finds the matching file in the directory.

    Parameters
    ----------
        file : string, mandatory
            Name of the file you need to search in the directory.
            The name can be fuzzy.

        file_dir : string, mandatory
            Directory in which the file exists or needs to be searched in.

        min_score : integer, optional
            Minimum score/Threshold score that should match while making as
            approximate guess.
            Global default: 65

    Returns
    -------
        best_guess[0], current_score : tuple, default
            Returns correctly guessed file name with matching score.
    """
    from os import walk
    from fuzzywuzzy import fuzz
    from fuzzywuzzy.process import extract

    try:
        for root, _, files in walk(file_dir):
            guessed_files = extract(
                file, files, limit=3, scorer=fuzz.partial_ratio)
            no_match_score = 0
            no_match_found = f'Sorry, I could\'nt find \'{file}\' in the directory.'
            for best_guess in guessed_files:
                current_score = fuzz.partial_ratio(file, best_guess)
                if current_score > min_score and current_score > no_match_score:
                    return best_guess[0], current_score
                else:
                    return no_match_found, no_match_score
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def current_weather(city: str) -> str:
    """
    Definition
    ----------
        Returns the current weather for provided city.

    Parameter
    ---------
        city : string, mandatory
            Name of the city for which you need to find the weather.

    Returns
    -------
        choice(weather_condition) : string, default
            Current weather conditions for the asked city.

    Notes
    -----
        An account on `https://www.apixu.com` is required to get the api key.
        API calls are made to retreive the weather reports.
    """
    import os
    from random import choice
    from apixu.client import ApixuClient

    try:
        client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU'))

        local_area = client.current(q=city)
        name = local_area['location']['name']
        condition = local_area['current']['condition']['text']
        temperature_c = local_area['current']['temp_c']
        temperature_f = local_area['current']['temp_f']
        is_day = local_area['current']['is_day']
        wind_kph = local_area['current']['wind_kph']
        wind_mph = local_area['current']['wind_mph']
        wind_degree = local_area['current']['wind_degree']
        wind_dir = local_area['current']['wind_dir']
        pressure_in = local_area['current']['pressure_in']
        pressure_mb = local_area['current']['pressure_mb']
        precip_mm = local_area['current']['precip_mm']
        precip_in = local_area['current']['precip_in']
        humidity = local_area['current']['humidity']
        cloud = local_area['current']['cloud']
        feelslike_c = local_area['current']['feelslike_c']
        feelslike_f = local_area['current']['feelslike_f']
        vis_km = local_area['current']['vis_km']
        vis_miles = local_area['current']['vis_miles']
        uv = local_area['current']['uv']
        gust_kph = local_area['current']['gust_kph']
        gust_mph = local_area['current']['gust_mph']

        at_am = [f'Currently in {name} it\'s {temperature_c}°C and'
                 f' {condition} with winds running upto {wind_kph} km/h.',
                 f'Right now in {name} it\'s {temperature_c}°C and {condition}'
                 f' but because of the humidity it feels like'
                 f' {feelslike_c}°C.',
                 f'It is currently {condition} in {name} with '
                 f' {temperature_c}°C and winds running upto {wind_kph} km/h.',
                 f'It is {temperature_c}°C and {condition} in {name}'
                 f' with winds running upto {wind_kph} km/h but due to'
                 f' the current humidity it feels like {feelslike_c}°C.',
                 f'Weather in {name} is {temperature_c}°C with {condition}'
                 f' conditions and winds blowing in {wind_dir} direction.',
                 f'The weather today in {name} is {condition} with'
                 f' {temperature_c}°C.']
        at_pm = [f'Tonight the weather is {condition} in {name} with winds'
                 f' blowing in {wind_dir} direction at {wind_kph} km/h.'
                 f' Temperature is {temperature_c}°C.',
                 f'Tonight the weather is {condition} in {name} with'
                 f' {temperature_c}°C but due to {humidity}% humidity it feels'
                 f' like {feelslike_c}°C.',
                 f'The weather tonight in {name} is {condition} with'
                 f' {temperature_c}°C.',
                 f'Right now in {name} it\'s {temperature_c}°C and {condition}'
                 f' but due to humidity it feels like {feelslike_c}°C.',
                 f'Currently in {name} it\'s {temperature_c}°C and {condition}'
                 f' with winds running upto {wind_kph} km/h.']

        if is_day == 0:
            return choice(at_pm)
        else:
            return choice(at_am)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def forecast_weather(city: str, hours: int = None, mins: int = None) -> str:
    """
    Definition
    ----------
        Returns the weather forecast for provided city.

    Parameter
    ---------
        city : string, mandatory
            Name of the city for which you need to find the forecast.

        hours : integer, optional
            Projected number of hours for which you need weather forecast for.
            Global default: 5 hours

        mins : integer, optional
            Projected number of minutes for which you need weather forecast.
            Global default: 0 mins.

    Returns
    -------
        choice(weather_forecast) : string, default
            Forecasted weather conditions for the asked city.

    Notes
    -----
        An account on `https://www.apixu.com` is required to get the api key.
        API calls are made to retreive the weather reports.
    """
    import os
    from random import choice
    from apixu.client import ApixuClient

    try:
        client = ApixuClient(api_key=os.environ.get('CHARLOTTE_APIXU'))

        if hours is None or hours is 'None' or hours is 'null':
            if mins is None or mins is 'None' or mins is 'null':
                local_area = client.forecast(q=city, hour=5)
            else:
                min_to_hour = int(mins) // 60
                local_area = client.forecast(q=city, hour=min_to_hour)
        else:
            if int(hours) >= 23:
                local_area = client.forecast(q=city, days=1)
            else:
                local_area = client.forecast(q=city, hour=hours)
        name = local_area['location']['name']
        condition = local_area['current']['condition']['text']
        temperature_c = local_area['current']['temp_c']
        temperature_f = local_area['current']['temp_f']
        is_day = local_area['current']['is_day']
        wind_kph = local_area['current']['wind_kph']
        wind_mph = local_area['current']['wind_mph']
        wind_degree = local_area['current']['wind_degree']
        wind_dir = local_area['current']['wind_dir']
        pressure_in = local_area['current']['pressure_in']
        pressure_mb = local_area['current']['pressure_mb']
        precip_mm = local_area['current']['precip_mm']
        precip_in = local_area['current']['precip_in']
        humidity = local_area['current']['humidity']
        cloud = local_area['current']['cloud']
        feelslike_c = local_area['current']['feelslike_c']
        feelslike_f = local_area['current']['feelslike_f']
        vis_km = local_area['current']['vis_km']
        vis_miles = local_area['current']['vis_miles']
        uv = local_area['current']['uv']
        gust_kph = local_area['current']['gust_kph']
        gust_mph = local_area['current']['gust_mph']
        maxtemp_c = local_area['forecast']['forecastday'][0]['day']['maxtemp_c']
        maxtemp_f = local_area['forecast']['forecastday'][0]['day']['maxtemp_f']
        mintemp_c = local_area['forecast']['forecastday'][0]['day']['mintemp_c']
        mintemp_f = local_area['forecast']['forecastday'][0]['day']['mintemp_f']
        avgtemp_c = local_area['forecast']['forecastday'][0]['day']['avgtemp_c']
        avgtemp_f = local_area['forecast']['forecastday'][0]['day']['avgtemp_f']
        maxwind_kph = local_area['forecast']['forecastday'][0]['day']['maxwind_kph']
        maxwind_mph = local_area['forecast']['forecastday'][0]['day']['maxwind_mph']
        totalprecip_mm = local_area['forecast']['forecastday'][0]['day']['totalprecip_mm']
        totalprecip_in = local_area['forecast']['forecastday'][0]['day']['totalprecip_in']
        avgvis_km = local_area['forecast']['forecastday'][0]['day']['avgvis_km']
        avgvis_miles = local_area['forecast']['forecastday'][0]['day']['avgvis_miles']
        avghumidity = local_area['forecast']['forecastday'][0]['day']['avghumidity']
        forecast_condition = local_area['forecast']['forecastday'][0]['day']['condition']['text']
        forecast_uv = local_area['forecast']['forecastday'][0]['day']['uv']

        at_am = [f'Today, it will be {forecast_condition} with maximum'
                 f' temperature of {maxtemp_c}°C and minimum of'
                 f' {mintemp_c}°C.',
                 f'The temperature in {name} is predicted to be {avgtemp_c}°C'
                 f' and with {forecast_condition}.',
                 f'There will be winds blowing upto {maxwind_kph} km/h and'
                 f' temperature would be anywhere between {maxtemp_c}°C and'
                 f' {mintemp_c}°C.',
                 f'It is forecasted to be about {avgtemp_c}°C with'
                 f' {forecast_condition} in {name}.']
        at_pm = [f'Tonight, the weather in {name} is predicted to be'
                 f' {forecast_condition} with maximum temperature of'
                 f' {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                 f'Well, tonight it is forecasted to be {avgtemp_c}°C with'
                 f' {forecast_condition} in {name}.']
        with_hrs = [f'Well, the weather for {name} in next {hours} hours is'
                    f' forecasted to be {forecast_condition} with maximum'
                    f' of {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                    f'The climate for {name} in next {hours} hours is'
                    f' predicted to be {avgtemp_c}°C and with'
                    f' {forecast_condition}.',
                    f'In {name}, is forecasted to be about {avgtemp_c}°C with'
                    f' {forecast_condition} in next {hours} hours.']
        with_mins = [f'Well, the weather for {name} in next {mins} mins is'
                     f' forecasted to be {forecast_condition} with maximum'
                     f' of {maxtemp_c}°C and minimum of {mintemp_c}°C.',
                     f'The climate for {name} in next {mins} mins is'
                     f' predicted to be {avgtemp_c}°C and with'
                     f' {forecast_condition}.',
                     f'In {name}, is forecasted to be about {avgtemp_c}°C with'
                     f' {forecast_condition} in next {mins} mins.']

        if hours is None or hours is 'None' or hours is 'null':
            if mins is None or mins is 'None' or mins is 'null':
                if is_day == 0:
                    return choice(at_pm)
                else:
                    return choice(at_am)
            else:
                return choice(with_mins)
        else:
            return choice(with_hrs)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def current_forecast_weather(city: str) -> str:
    """
    Definition
    ----------
        Returns the weather report for provided city. This inlcudes both
        current weather and weather forecast for that city

    Parameter
    ---------
        city : string, mandatory
            Name of the city for which you need to find the weather.

    Returns
    -------
        choice(weather_current_forecast) : string, default
            Weather conditions and Forecast for the asked city.

    Notes
    -----
        An account on `https://www.apixu.com` is required to get the api key.
        API calls are made to retreive the weather reports.
    """
    return current_weather(city) + ' ' + forecast_weather(city)


def wish_user() -> str:
    """
    Definition
    ----------
        Wishes the user Good Morning/Evening based on the time of the day.
    """
    from datetime import datetime
    from random import choice

    hour = datetime.now().hour
    morning = choice([f'Good Morning, {title}.', 'Good Morning!'])
    afternoon = choice([f'Good Afternoon, {title}.', 'Good Afternoon!'])
    evening = choice([f'Good Evening, {title}.', 'Good Evening!'])
    night = f'Hello, {title}!'
    greeting = morning if hour >= 5 and hour < 12 else afternoon if hour >= 12 and hour < 17 else evening if hour >= 17 and hour < 22 else night
    return greeting


def string_match(text: str, text_list: list, min_score: int = 65) -> tuple:
    """
    Definition
    ----------
        Finds the matching string in the list.

    Parameters
    ----------
        text : string, mandatory
            Name of the file you need to search in the directory.
            The name can be fuzzy.

        file_dir : string, mandatory
            Directory in which the file exists or needs to be searched in.

        min_score : integer, optional
            Minimum score/Threshold score that should match while making as
            approximate guess.
            Global default: 65

    Returns
    -------
        best_guess[0], current_score : tuple, default
            Returns correctly guessed file name with matching score.
    """
    from os import walk
    from fuzzywuzzy import fuzz
    from fuzzywuzzy.process import extract

    try:
        if text is not None:
            guessed = extract(text, text_list, limit=3,
                              scorer=fuzz.partial_ratio)
            no_match_score = 0
            no_match_found = f'Sorry, I could\'nt find a matching \'{text}\'.'
            for best_guess in guessed:
                current_score = fuzz.partial_ratio(text, best_guess)
                if current_score > min_score and current_score > no_match_score:
                    return best_guess[0]
                else:
                    return no_match_found
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def play_music(file: str = None, file_dir: str = local_dir['music']) -> None:
    """
    Definition
    ----------
        Plays music from `D:/Music` directory.

    Parameters
    ----------
        file : string, mandatory
            Name of the file you need to search in the directory.
            The name can be fuzzy.

        file_dir : string, mandatory
            Directory in which the file exists or needs to be searched in.
            Here, it`s under Music directory.
            Global default: D:/Music/
    """
    from os import startfile, listdir
    from os.path import isfile, join
    from random import choice

    try:
        if file is not None:
            file_name, file_score = find(file, file_dir)
            if file_score == 0:
                return file_name
            else:
                music_file = join(file_dir, file_name)
                startfile(f'{music_file}')
        else:
            music_file = choice([join(local_dir['music'], file) for file in listdir(
                local_dir['music']) if isfile(join(local_dir['music'], file))])
            startfile(music_file)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def music_metadata_extractor(file: str) -> tuple:
    """
    Definition
    ----------
        Extracts the metadata from music files.

    Parameters
    ----------
        file : string, mandatory
            Name of the file you need to search in the directory.

    Returns
    -------
        music_file : string, default
        track_name : string, default
        track_artist : string, default
        track_albumartist : string, default
        track_composer : string, default
        track_album : string, default
        track_genre : string, default
        track_duration : string, default
        track_year : string, default
        track_filesize : string, default
            Metadata of the music file.
    """
    from os.path import basename
    from datetime import timedelta
    from hurry.filesize import size, alternative
    from tinytag import TinyTag

    try:
        music_track = TinyTag.get(file)
        music_file = basename(file)
        track_name = music_track.title
        track_artist = music_track.artist
        track_albumartist = music_track.albumartist
        track_composer = music_track.composer
        track_album = music_track.album
        track_genre = music_track.genre
        track_duration = str(timedelta(seconds=round(music_track.duration)))
        track_year = music_track.year
        track_filesize = size(music_track.filesize, system=alternative)

        return music_file, track_name, track_artist, track_albumartist, track_composer, track_album, track_genre, track_duration, track_year, track_filesize
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def play_music_by_attribute(music_file: str = None,
                            track_name: str = None,
                            track_artist: str = None,
                            track_albumartist: str = None,
                            track_composer: str = None,
                            track_album: str = None,
                            track_genre: str = None,
                            track_duration: str = None,
                            track_year: str = None,
                            track_filesize: str = None) -> None:
    from random import randint
    from numpy import ones
    from pandas import read_csv, Series

    try:
        if music_file is not None:
            play_music(music_file)
        else:
            music_csv_file = ai_file['music']
            df = read_csv(music_csv_file, encoding='utf-8', )
            master_dict = {
                'track_name': string_match(track_name, df['track_name'].dropna().tolist()),
                'track_artist': string_match(track_artist, df['track_artist'].dropna().tolist()),
                'track_albumartist': string_match(track_albumartist, df['track_albumartist'].dropna().tolist()),
                'track_composer': string_match(track_composer, df['track_composer'].dropna().tolist()),
                'track_album': string_match(track_album, df['track_album'].dropna().tolist()),
                'track_genre': string_match(track_genre, df['track_genre'].dropna().tolist()),
                'track_duration': string_match(track_duration, df['track_duration'].dropna().tolist()),
                'track_year': string_match(track_year, df['track_year'].dropna().tolist()),
                'track_filesize': string_match(track_filesize, df['track_filesize'].dropna().tolist())}

            filtered_dict = {k: v for k,
                             v in master_dict.items() if v is not None}
            filter_series = Series(ones(df.shape[0], dtype=bool))
            for column, value in filtered_dict.items():
                filter_series = ((df[column] == value) & filter_series)

            if len(df[filter_series]) > 1:
                random_pick = df[filter_series].iloc[randint(
                    0, len(df[filter_series])), 0]
                play_music(random_pick)
            elif len(df[filter_series]) == 1:
                play_music(df[filter_series].iloc[0, 0])
            else:
                return f'Sorry, {title}. I couldn\'t find any combination of the search parameters.'
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')
