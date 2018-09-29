"""
Data parser for text Files
Supports file types: .txt
For Similar movies, Response of first data point becomes Line of next data point
Written By: Shantanu Mantri on 9/28/2018
"""
import csv

class DataParser:
	
	def __init__(self, filename, delimiter):
		self.filename = filename
		self.delimiter = delimiter
		self.linedict = {}

	def addData(self, csvfilename):
		to_write = []
		if self.filename.split(".")[-1] == "txt":
			f = open(self.filename, "r", encoding="cp1252")
			lines = f.readlines()
			prev_movie = lines[0].split(self.delimiter)[2]
			idx = 0
			
			while idx + 1 < len(lines):
				line = lines[idx + 1]
				parts = line.split(self.delimiter)
				cur_movie = parts[2]
				if prev_movie == cur_movie:
					prev_line = lines[idx].split(self.delimiter)[-1]
					response = parts[-1]
					to_write.append([prev_line.rstrip("\n\r")
						, response.rstrip("\n\r")])
					prev_movie = cur_movie
					idx += 1
				else:
					prev_movie = cur_movie
					idx += 1

		with open(csvfilename, mode='w', encoding='cp1252') as csv_file:
			fieldnames = ["Line", "Response"]
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator = '\n')
			writer.writeheader()
			for l in to_write:
				writer.writerow({'Line': l[0], 'Response': l[1]})
		f.close()

dp = DataParser("../data/movie_lines.txt", "+++$+++")
dp.addData("../data/movie_lines.csv")

