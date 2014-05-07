#!/usr/bin/python

import sys
import getopt
import datetime
import time
import urllib
import urllib2
from xml.dom import minidom


API_KEY = "mmtghjxxh675uvw2uh9xv792"
BASE_URL = "http://api.hotwire.com/v1/search/hotel?"
DATE_FORMAT = "%m/%d/%Y"
NUM_RESULTS_TO_DISPLAY = 30


def SanitizeStarStr(star):
  if len(star) == 1 and int(star) < 6:
    return star + ".0"
  elif len(star) == 3 and "." in star:
    return star
  raise ValueError("Star must be of format 4.0, 4, or 4.5")


def IsWeekend(date):
  return date.weekday() == 5 or date.weekday() == 6


def ContainsWeekend(start_date, end_date):
  while start_date != end_date + datetime.timedelta(days=1):
    if IsWeekend(start_date):
      return True
    start_date += datetime.timedelta(days=1)
  return False


def ExecuteQuery(dest, start_date, time_delta, star, should_skip_weekends):
  end_date = start_date + time_delta - datetime.timedelta(days=1)
  if should_skip_weekends and ContainsWeekend(start_date, end_date):
    end_date += datetime.timedelta(days=2)

  params = {
      "apikey": API_KEY,
      "dest": urllib.quote(dest),
      "rooms": "1",
      "adults": "1",
      "children": "0",
      "startdate": start_date.strftime(DATE_FORMAT),
      "enddate": end_date.strftime(DATE_FORMAT)}

  params_list = [key + "=" + value for key, value in params.iteritems()]
  url = BASE_URL + "&".join(params_list)
  page = ""
  for _ in xrange(3):
    try:
      page = urllib2.urlopen(url, timeout=2).read()
      break
    except Exception:
      print >>sys.stderr, "Request to hotwire timed out, retrying"

  if not page:
    return

  xmldoc = minidom.parseString(page)
  hotel_results = xmldoc.getElementsByTagName("HotelResult")

  found_tuples = []
  for hotel_result in hotel_results:
    star_rating = hotel_result.getElementsByTagName("StarRating")[0]
    if star_rating.firstChild.nodeValue == star:
      avg_price_per_night = hotel_result.getElementsByTagName(
          "AveragePricePerNight")[0].firstChild.nodeValue
      deep_link = hotel_result.getElementsByTagName(
          "DeepLink")[0].firstChild.nodeValue
      found_tuples.append(
          (avg_price_per_night, start_date, end_date, deep_link))
  if found_tuples:
    found_tuples.sort(key=lambda x: x[0])
    return found_tuples[0]
  else:
    return None


def Usage():
  print """Usage: ./hotterwire.py --startdate=5/1/2014 --enddate=5/10/2014 \\
    --duration=3 --star=4.5 --destination=Wailea [--skip_weekends]
  """


def main(argv):
  try:
      opts, args = getopt.getopt(argv, "",
          ["startdate=", "enddate=", "duration=", "star=", "destination=",
           "skip_weekends"])
  except getopt.GetoptError:
    Usage()
    sys.exit(1)

  if len(opts) < 5 or args:
    Usage()
    sys.exit(1)

  should_skip_weekends = False
  for opt, arg in opts:
    if opt == "--startdate":
      start_date = datetime.datetime.strptime(arg, DATE_FORMAT)
    elif opt == "--enddate":
      end_date = datetime.datetime.strptime(arg, DATE_FORMAT)
    elif opt == "--duration":
      days = int(arg)
    elif opt == "--star":
      star = SanitizeStarStr(arg)
    elif opt == "--destination":
      dest = arg
    elif opt == "--skip_weekends":
      should_skip_weekends = True
    else:
      Usage()
      sys.exit(1)

  current_date = start_date

  results = []
  while current_date != end_date:
    result = ExecuteQuery(
        dest, current_date, datetime.timedelta(days=days), star,
        should_skip_weekends)
    time.sleep(.5)
    if result:
      results.append(result)
    current_date += datetime.timedelta(days=1)

  if not results:
    print 'No results could be found. Try different parameters'
    sys.exit()

  results.sort(key=lambda x: x[0])

  print "Found results:"
  for result in results[0:NUM_RESULTS_TO_DISPLAY]:
    print "*" * 80
    print "price: %s\ncheckin: %s\ncheckout: %s\nbooking link: %s" % (
        result[0], result[1].strftime(DATE_FORMAT),
        result[2].strftime(DATE_FORMAT), result[3])


if __name__ == '__main__':
  main(sys.argv[1:])
