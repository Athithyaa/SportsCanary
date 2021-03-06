import os
import json
import requests
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth


class GnipSearchClient:
    def __init__(self):
        self.username = os.environ['GNIP_USERNAME']
        self.password = os.environ['GNIP_PASSWORD']
        self.url = os.environ['GNIP_URL']
        self.counter = 0

    # Date is done by UTC, which is a five hour difference to EST.
    # Kobe's last game was 10:30 EST, so 2:30 AM UTC on the 14
    # from_date = '201604140230'
    # to_date = '201604140530'
    # max_results = 500
    def initial_search(self, query, max_results, from_date, to_date, number_of_pages):
        """
        Uses Gnip's Search-API
        :param query: words to query
        :param max_results: 10-500, defaults to 100
        :param from_date: UTC timestamp to minute
        :param to_date: UTC timestamp to minute
        :param number_of_pages: How many pages to obtain, pages come in max results sizes, ie max of 500 tweets per page
        """
        next_token = ''
        query = '?query=' + str(query) + '&maxResults=' + str(max_results)
        date = '&fromDate=' + str(from_date) + '&toDate=' + str(to_date)
        for i in range(number_of_pages):
            if next_token == '':
                url = self.url + query + date
            else:
                url = self.url + query + date + '&next=' + next_token

            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            content = json.loads(r.content)

            self.save_json_blog_to_disk(content, self.counter)
            self.counter += 1
            try:
                next_token = content['next']
            except KeyError:
                print('No next found.')
                break

    def save_json_blog_to_disk(self, json_blob, counter):
        file_path = self.get_file_path(counter)
        with open(file_path, 'w') as outfile:
            json.dump(json_blob, outfile)

    @staticmethod
    def get_file_path(counter):
        wd = os.getcwd()
        return wd + '/Gnip_Client/Gnip_Search_' + str(counter) + '.json'

    def load_json_blob(self, counter):
        file_path = self.get_file_path(counter)
        with open(file_path) as data_file:
            return json.load(data_file)

    @staticmethod
    def create_start_time():
        return datetime(2016, 04, 14, 02, 30)

    @staticmethod
    def convert_date_to_gnip_format(date):
        return date.strftime('%Y%m%d%H%M')

    @staticmethod
    def move_date_forward_by(date, days=0, hours=0, minutes=0):
        return date + timedelta(days=days, hours=hours, minutes=minutes)

    def iterate_through_game_at_minute_intervals(self):
        try:
            from_date = datetime(2016, 04, 14, 02, 30)
            to_date = datetime(2016, 04, 14, 02, 31)
            max_results = 500
            query = 'Kobe'
            number_of_pages = 5
            while to_date != datetime(2016, 04, 14, 05, 31):
                print(self.convert_date_to_gnip_format(from_date))
                print(self.convert_date_to_gnip_format(to_date))
                # self.initial_search(query=query, max_results=max_results,
                #                     from_date=self.convert_date_to_gnip_format(from_date),
                #                     to_date=self.convert_date_to_gnip_format(to_date),
                #                     number_of_pages=number_of_pages)
                from_date = self.move_date_forward_by(from_date, minutes=1)
                to_date = self.move_date_forward_by(to_date, minutes=1)
            return True
        except:
            return None
