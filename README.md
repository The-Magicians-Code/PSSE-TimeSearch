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
