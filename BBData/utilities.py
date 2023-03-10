from datetime import datetime
import json
import os

def first(iterable, default=None):
  for item in iterable:
    return item
  return default
  
def getDuration(then, now = datetime.now(), interval = "default"):

    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds() 
    
    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)   
      return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }

def currentTime():
    '''
    Generate the current time

    Returns:
        str: Current Time
    '''
    return datetime.now().strftime("%m/%d/%y %H:%M:%S")

def getFilesWithExtension(paths : list, extension : str = '.json', recursive=False):
  def listdirs(rootdir):
    paths = []
    for it in os.scandir(rootdir):
        if it.is_dir():
            paths.append(it.path)
            paths += listdirs(it)
    return paths

  files = []
  if recursive:
    [paths.__iadd__(listdirs(root)) for root in paths]
  for path in paths:
    for file in os.listdir(path):
      if file.endswith(extension):
          files.append(os.path.join(path, file))
  return files

def loadJsonLike(path):
  with open(path) as json_file:
    return json.load(json_file)

def saveJsonLike(dict, path):
  with open(path, "w") as outfile:
    json.dump(dict, outfile)