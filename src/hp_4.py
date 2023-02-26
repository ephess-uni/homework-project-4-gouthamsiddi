# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict
import csv


def reformat_dates(dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date in dates:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
        new_dates.append(datetime_obj.strftime('%d %b %Y'))
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError('Start date must be a string')
    if not isinstance(n, int):
        raise TypeError('n must be an integer')
    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_list = [start_date + timedelta(days=i) for i in range(n)]
    return date_list


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))



def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    fees = {}
    with open(infile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            due_date = datetime.strptime(row['date_due'], '%m/%d/%Y')
            return_date = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            if return_date > due_date:
                days_late = (return_date - due_date).days
                late_fee = days_late * 0.25
                fees[row['patron_id']] = fees.get(row['patron_id'], 0) + late_fee
    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['patron_id', 'late_fees'])
        for patron_id, fee in fees.items():
            writer.writerow([patron_id, round(fee, 2)])



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    #BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
