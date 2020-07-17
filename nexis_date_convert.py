# Translates long form dates from Nexis output into dates that excel will recognise and be able to sort

import csv
import itertools
import pandas as pd


def date_converter(longform_dates, csv_name):
	
	#create empty list for dates in new format
	new_date_list = []
	day = ''
	month = ''
	year = ''
	
	#import csv file of long form dates into list
	with open(longform_dates, 'r', encoding = 'utf-8-sig') as f:
		reader = csv.reader(f)
		dates = list(reader)
	dates_list = list(itertools.chain(*dates)) 

	for d in dates_list:

		#Remove days of week if included (in daily newspapers)
		list_raw = d.split()
		list_d = [list_raw[len(list_raw)-3], list_raw[len(list_raw)-2], list_raw[len(list_raw)-1]]

		#remove '.' from days, ensure in dd format
		day = list_d[0].replace(".", "")
		if len(day) == 1:
			day = "0" + day
		
		#Dictionary of long form month names in original file (edit as necessary) and months in mm format
		months_dict = {
		'Januar' : '01', 
		'Februar': '02', 
		'März' : '03', 
		'April' : '04',
		'Mai'  : '05',
		'Juni' : '06',
		'Juli' : '07',
		'August' : '08',
		'September' : '09',
		'Oktober' : '10',
		'November' : '11',
		'Dezember' : '12'}

		if list_d[1] in months_dict:
			month = months_dict.get(list_d[1])
	
		year = list_d[2]

		date_as_list = [day, month, year]
		newdate = '/'.join(date_as_list)

		new_date_list.append(newdate)

	dates_df = pd.DataFrame(new_date_list)
	dates_df.to_csv(csv_name, index=False, header=True)
	print(dates_df)


#Replace with file names of original and new dates
date_converter(longform_dates = 'derspiegel_dates.csv',
				 csv_name = "derspiegel_dates_NEW.csv")

date_converter(longform_dates = 'diewelt_dates.csv',
				csv_name = "diewelt_dates_NEW.csv")


