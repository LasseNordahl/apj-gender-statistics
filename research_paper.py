import re

class ResearchPaper:

    def __init__(self, file_name):
        self.file_name = file_name
        self.first_name = None
        self.last_name = self.parse_last_name(file_name)
        self.received_date = None
        self.accepted_date = None

    def __str__(self):
        return 'ResearchPaper(File Name="{file_name}", First Name="{first_name}", Last Name="{last_name}", Received="{received}", Accepted="{accepted}")'\
            .format(file_name=self.file_name, first_name=self.first_name, last_name=self.last_name, received=self.received_date, accepted=self.accepted_date)

    def __bool__(self):
        return (self.file_name != None and self.first_name != None and self.last_name != None and self.received_date != None and self.accepted_date != None)

    def parse_last_name(self, file_name):
        name_regex = re.compile('([A-Za-z_]*)(?=_[0-9]+)')
        last_name = name_regex.search(file_name)
        if last_name:
           pre_last_name = last_name.group()
           return ' '.join([name.capitalize() for name in pre_last_name.split('_')])
        else:
            raise TypeError('ResearchPaper __init__ - No last name found in ' + self.file_name)

    def add_page_text(self, page_text):
        self.add_page_text = page_text

    def add_first_name(self, first_name):
        self.first_name = first_name

    def add_received(self, received):
        self.received_date = received

    def add_accepted(self, accepted):
        self.accepted_date = accepted