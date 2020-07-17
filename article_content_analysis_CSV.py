'''
Takes an output csv file from Lexis Nexis providing article content and date, and a
csv file containing a list of key words. Counts the number of times any key word is 
mentioned in the articles and outputs a data set of counted key words for each date
'''

import csv
import itertools
import pandas as pd
from collections import Counter
from string import punctuation
import unicodedata


def analyse_article_content(content_csv, keyword_csv, outfile_name, content_column = 'hlead', date_column = 'date'):
	
	# Create list of keywords from 'keyword_stems.csv'
	with open(keyword_csv, 'r', encoding = 'utf-8-sig') as f:
		reader = csv.reader(f)
		keywords = list(reader)
	keywords = list(itertools.chain(*keywords))

	# Create database from news content csv file
	news_content = pd.read_csv(content_csv)
	news_content = news_content.dropna(thresh=3)


	for column in news_content[[content_column]]:
		columnSeriesObj = news_content[column]
		article_hlead = columnSeriesObj.values
	article_wordlist = article_hlead.tolist()

	for column in news_content[[date_column]]:
		columnSeriesObj = news_content[column]
		article_date = columnSeriesObj.values

	
	keyword_counter = []
	for i in article_wordlist:
		counts = Counter(x.rstrip(punctuation).lower() for x in i.split())
		list_word_counts  = counts.most_common()

		keyword_hits_list = []
		for x in range(0, len(list_word_counts)):
			
			temp = list(list_word_counts[x]) # convert from tuple to list
			temp[1] = str(temp[1]) #change number (at index 1) into string
			n_temp = [(unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore')).lower().decode() for word in temp] #normalised umlauts in data

			#check word (at index 0) against list of keywords, add new column = 1 if match, = 0 otherwise.
			hits = 0 
			for i in range(0, len(keywords)):
				if keywords[i] in n_temp[0]:
					hits = hits + 1
			if hits != 0:
				n_temp.append(1)
			else:
				n_temp.append(0)

			keyword_hits = int(n_temp[1])*int(n_temp[2])
			keyword_hits_list.append(keyword_hits)
		
		keyword_counts = sum(keyword_hits_list)
		keyword_counter.append(keyword_counts)
		
	
	df = pd.DataFrame({"date": article_date, "keywords": keyword_counter})
	df.to_csv(outfile_name, index=False)

					
# replace with file names of content files, output file name for each news source, and column names for article text and date
analyse_article_content(news_content, keyword_stems, news_output, content_column = 'hlead', date_column = 'date')


