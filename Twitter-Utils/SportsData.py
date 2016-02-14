import os
import datetime
import requests
import simplejson as json


class SportsData:
    """
    Class to gather data from the Stattleship API
    Endpoints follow the pattern <sport>/<league>/<action>
    And the headers must look as follows:
    Content-Type: application/json"
    Accept: application/vnd.stattleship.com; version=1
    Authorization: Token token=ACCESS_TOKEN
    """

    def __init__(self):
        self.CLIENT_ID = os.environ['STAT_CLIENT_ID']
        self.STAT_CLIENT_SECRET = os.environ['STAT_CLIENT_SECRET']
        self.STAT_ACCESS_TOKEN = os.environ['STAT_ACCESS_TOKEN']
        self.base_url = 'https://www.stattleship.com/basketball/'
        self.nba_team_list = ['nba-atl', 'nba-bk', 'nba-bos', 'nba-cha', 'nba-chi',
                              'nba-cle', 'nba-dal', 'nba-den', 'nba-det', 'nba-gs',
                              'nba-hou', 'nba-ind', 'nba-lac', 'nba-lal', 'nba-mem',
                              'nba-mia', 'nba-mil', 'nba-min', 'nba-no', 'nba-ny',
                              'nba-okc', 'nba-orl', 'nba-phi', 'nba-pho', 'nba-por',
                              'nba-sa', 'nba-sac', 'nba-tor', 'nba-uta', 'nba-was']

    def get_games_for_team(self, team_id):

        """

        Gets all basketball games
        :param team_id: team_id as defined by stattleship API
        :return: returns content of response
        """

        url = self.base_url + '/nba/games?team_id=' + team_id
        headers = {
            'Authorization': str(self.STAT_ACCESS_TOKEN),
            'Accept': 'application/vnd.stattleship.com; version=1',
            'Content-Type': 'application/json'
        }

        res = requests.get(url, headers=headers)
        content = json.loads(res.content)

        return content['games']

    def get_games_within_time_range_for_team(self, team_id, time_range):

        """
        :param team_id: team_id as defined by stattleship API
        :param time_range: time range in DAYS given as an INT
        :return: returns a list with all games within time range
        """
        list_next_seven_days = []
        for x in range(0, time_range):
            current_date = datetime.datetime.now() + datetime.timedelta(days=x)
            list_next_seven_days.append(current_date.strftime("%B %d, %Y"))

        games = self.get_games_for_team(team_id=team_id)

        relevant_games_list = []

        for game in games:
            date_on = game['on'][3:]
            if date_on in list_next_seven_days:
                relevant_games_list.append(game)

        return relevant_games_list

    def get_upcoming_games_for_nba(self, time_range):
        """
        Returns a list of all upcoming games in the NBA within time range.
        Currently highly inefficient due to it having to twice as many API
        calls as it has too and thus every game is duplicated.  Optimization
        would be to check the team id before making a call thus making half
        the amount of calls.
        :param time_range: time range in DAYS given as an INT
        :return: return list of games object
        """
        upcoming_games = []
        for team in self.nba_team_list:
            upcoming_games_for_team = self.get_games_within_time_range_for_team(team, time_range)
            for game in upcoming_games_for_team:
                upcoming_games.append(game)

        return upcoming_games

    def pretty_print_schedule(self, time_range):
        """Prints pretty version of schedule"""
        for game in self.get_upcoming_games_for_nba(time_range):
            print(game['title'] + " " + game['on'])


t = SportsData()
t.pretty_print_schedule(7)
