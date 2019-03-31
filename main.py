import os
import re
from tika import parser

from research_paper import ResearchPaper

paper_directory = 'papers'

def parse_papers(directory):
    research_paper_names = [file_name for file_name in os.listdir(paper_directory) if file_name != '.DS_Store']
    research_papers = [ResearchPaper(file_name) for file_name in research_paper_names]
    extract_paper_data(research_papers)
    # print_papers(research_papers)

def extract_paper_data(research_papers):
	page_regex = re.compile('<div((.|\n)*?)<\/div>')

	for paper in research_papers:
		pdf_file_object = parser.from_file(paper_directory + '/' + paper.file_name, xmlContent=True)
		pdf_xml = pdf_file_object['content']
		search_obj = page_regex.search(pdf_xml)
		if search_obj:
			first_page_text = search_obj.group()
			add_date_information(paper, get_paper_dates(first_page_text))
			add_first_name_information(paper, get_first_name(paper.last_name, first_page_text))
	print_papers(research_papers)
			

def add_date_information(paper, paper_dates):
	if type(paper_dates) is tuple and len(paper_dates) == 2:
		received_date, accepted_date = paper_dates
		paper.add_received(received_date)
		paper.add_accepted(accepted_date)

def add_first_name_information(paper, first_name):
	if first_name != -1:
		paper.add_first_name(first_name.lower().capitalize())


def get_paper_dates(first_page_text):
	date_regex = re.compile('Received (.+) ; accepted ([0-9]+ \w+ [0-9]+)')
	date_match = date_regex.search(first_page_text)
	return tuple(date_match.groups()) if date_match else -1

def get_first_name(last_name, first_page_text):
	# if last_name == 'Martel': print(first_page_text)
	name_regex = re.compile('<p>(\w+)(?: \w\.)? (?=(?:{u_last_name}|{last_name}))'.format(u_last_name=last_name.upper(), last_name=last_name))
	first_name = name_regex.search(first_page_text)
	if first_name:
		return first_name.groups()[0]
	else:
		line_regex = re.compile('<p>(.+(?:{u_last_name}|{last_name}).*)'.format(u_last_name=last_name.upper(), last_name=last_name))
		line_with_name = line_regex.search(first_page_text)
		if line_with_name:
			# Split the match object to grab the first name on that string
			line = line_with_name.groups()[0].split(' ')
			return line[0] if '.' not in line[0] else -1
		else:
			return -1
	

def print_papers(papers):
	for paper in papers:
		if paper:
			print(paper)

if __name__ == '__main__': 
    parse_papers(paper_directory)