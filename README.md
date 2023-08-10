# PSSE-TimeSearch
Automate the process of searching PSSE .raw files on a specific timestamp and finding strictly equal or closest matching files, then copy them from source to destination if needed
## Usage
Script gives an exact result or an approximation a.k.a. the nearest matching file
>Please keep in mind the ``T`` variable while formatting the time ``dd.mm.YYYY(T)HH:MM``, this provides proper parsing
````
python3 locator.py 08.11.1997T12:00
````
When copying, set the ``source`` and ``destination`` folders in the [settings](https://github.com/The-Magicians-Code/PSSE-TimeSearch/blob/main/settings.cfg) file and use either of the copy flags (``-c`` or ``--copy``)
````
python3 locator.py 08.11.1997T12:00 -c
````
Multiple dates are also accepted
````
python3 locator.py 08.11.1997T12:00 01.02.1987T01:15
````
## Extras
Possibility to look for a specific date upon requesting a day of the week, implemented example for Wednesday
````python
#!/usr/bin/env python3
import calendar

# Example usage
year = 2023
month = 9

this_month = calendar.monthcalendar(year, month)
third_wednesday = find_nth_day(this_month, 3, 2) # calendar.WEDNESDAY can be used instead of the third argument for being verbose, calendar.WEDNESDAY's value is 2
sunday_before_third_wednesday = find_previous_sunday(this_month, third_wednesday)

print(
f"""The third Wednesday of {calendar.month_name[month]} {year} is on the {third_wednesday}th.
The sunday before that is {sunday_before_third_wednesday}th."""
)
````
Resulting in
````
The third Wednesday of September 2023 is on the 20th.
The sunday before that is 17th.
````
