#!/usr/bin/env python3
# @Author: Tanel Treuberg
# @Github: https://github.com/The-Magicians-Code
# @Description: Automate the process of searching PSSE .raw files 
# on a specific timestamp and finding strictly equal or closest matching files

from configparser import ConfigParser
from pathlib import Path
from glob import glob
import argparse
import datetime
import calendar
import shutil

def find_nth_day(current_month: list[list[int, int]], week: int, day: int) -> int:
    """
    Finds the nth occurrence of a specific day in the given month.

    Args:
        current_month (list[list[int, int]]): A matrix representing the calendar for the given month.
            Each element in the matrix represents a day of the month.
            The matrix is a list of lists, where each inner list represents a week.
        week (int): The week number (1 - 5) for the desired occurrence.
        day (int): The day number (0 - 6, where Monday is 0 and Sunday is 6) for the desired day.

    Returns:
        int: The day of the nth occurrence of the desired day.

    Raises:
        ValueError: If the week number is not between 1 and 5, or if the day number is not between 0 and 6.

    """

    if week > 5 or week < 1:
        raise ValueError("Pick from weeks 1 - 5")
    if day > 6 or day < 0:
        raise ValueError("Pick from days 0 - 6 (Mon - Sun)")
    
    return current_month[week - 1][day] if current_month[0][day] != 0 else current_month[week][day]

def find_previous_sunday(current_month: list[list[int, int]], day: int) -> int:
    """
    Finds the date of the previous Sunday in the given month.

    Args:
        current_month (list[list[int, int]]): A matrix representing the calendar for the given month.
            Each element in the matrix represents a day of the month.
            The matrix is a list of lists, where each inner list represents a week.
        day (int): The numeric representation of the day as in date, 30th for example -> (30)

    Returns:
        int: The day of the previous Sunday.

    """

    week_for_sunday = [index for index, week in enumerate(current_month) if day in week][0]
    return this_month[week_for_sunday - 1][6]

def valid_date(timestamp: str) -> str:
    """
    Validates a timestamp string in the format "dd.mm.YYYYTHH:MM".

    Args:
        timestamp (str): The timestamp string to validate.

    Returns:
        str: The validated timestamp string if it is in the correct format.

    Raises:
        argparse.ArgumentTypeError: If the timestamp string is not in the correct format.

    Example:
        >>> valid_date("31.12.2022T23:59")
        '31.12.2022T23:59'
    """

    try:
        datetime.datetime.strptime(timestamp, "%d.%m.%YT%H:%M")
        return timestamp
    except ValueError as e:
        raise argparse.ArgumentTypeError(e)

def nearest_value(all_possibilites: list[int, int], key: int) -> str:
    """
    Finds the value from a list of possibilities that is closest to a given key.
    
    Args:
        all_possibilities (list[int]): A list of integers representing all possible values.
        key (int): The target integer to find the closest value to.
    
    Returns:
        str: The closest value from the list as a string. If the closest value is less than 10,
             it is returned with a leading zero. If the list is empty, an empty string is returned
    
    Raises:
        None
    
    Example:
        >>> nearest_value([5, 12, 8, 3], 7)
        '08'
    """
    
    if not all_possibilites:
        print("No data to process")
        return ""
    
    distances = [abs(value - key) for value in all_possibilites]
    closest_value_index = distances.index(min(distances))
    closest_value = all_possibilites[closest_value_index]
    solution = str(closest_value) if closest_value > 9 else "0" + str(closest_value)
    
    return solution

def searcher(date_input: str, haystack: str) -> str:
    """
    Searches for a specific file based on the given date and time.

    Args:
        date_input (str): A string representing the date and time in the format "YYYY.MM.DD HHMM".

    Returns:
        str: The filename of the closest matching file based on the given date and time. Empty string if none found

    Raises:
        None

    Example:
        >>> searcher("2022.01.15T13:45")
        'PTI_SE_2022.01.15_1400.raw'
    """

    date, time = date_input.split("T")
    hour_key, minute_key = [int(item) for item in time.split(":")]

    # Format date for filename
    formatted_date = "".join(date.split("."))
    needle = f"PTI_SE_{formatted_date}_*.raw"
    query = (Path(haystack) / needle).__str__()
    results = glob(query)

    if not results:
        print(f"There are no files on the current date: {date}")
        return ""
    
    # Find all available hours
    hours = [int(filename[-8:-6]) for filename in results]
    closest_hour = nearest_value(hours, hour_key)
    # Find all files with the closest hour
    narrowed_down_files = [file for file in results if file[-8:-6] == closest_hour]
    # Find all minutes in the hour
    minutes = [int(filename[-6:-4]) for filename in narrowed_down_files]
    closest_minute = nearest_value(minutes, minute_key)

    return f"PTI_SE_{formatted_date}_{closest_hour}{closest_minute}.raw"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Searching PSSE .raw files on or close to a specific time")
    parser.add_argument('timestamps', nargs="+", type=valid_date, metavar="date")
    parser.add_argument('-c', '--copy', action="store_true")
    parser.add_argument('--conf', default="settings.cfg", help="Configuration file, defaults to settings.cfg from the script directory")
    args = parser.parse_args()

    project_directory = Path(__file__).parent.resolve()

    conf = ConfigParser()
    if args.conf:
        config_path = Path(args.conf).__str__()
    else:
        config_path = (project_directory / args.conf).__str__()

    conf.read(config_path)
    configuration = conf["global"]


    # Check if destination exists and make if not
    dest = Path(configuration["destination"])
    dest.mkdir(parents=True, exist_ok=True)

    # Find and filter all valid filenames
    # File format: PTI_SE_DDMMYYYY_HHMM.raw
    files_to_copy = list(filter(None, [searcher(i, haystack=configuration["source"]) for i in args.timestamps]))
    print(f"Found matches: {files_to_copy}")

    if args.copy:
        # Copy files from source to destination
        copied_files = [shutil.copy(str(Path(configuration["source"]) / file), str(dest)) for file in files_to_copy]
        print(f"Files copied: {copied_files}")
