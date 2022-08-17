import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class HLTV:
	def __init__(self):
		self.base_url = 'https://www.hltv.org'
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
		self.session = requests.Session()

	def get_matches(self):
		url = self.base_url + '/' + 'matches'
		response = self.session.get(url, headers=self.headers)
		soup = BeautifulSoup(response.text, 'html.parser')
		response = []
		allContent = soup.find_all('div', class_='upcomingMatch')
		


		for match in allContent:
			matchStats = {}
			link = match.find('a')['href']
			matchID = link.split('/')[2]

			emptyMatch = match.select_one(".matchInfoEmpty")
			if emptyMatch != None:
				event = {'name': emptyMatch.find('span').text }
			else:
				# get teams
				teams = match.select('.matchTeam')
				teamsData = []
				for i,team in enumerate(teams):
					tameName = team.select_one('.matchTeamName').text
					teamLogo = team.select_one('img')['src']
					teamData = {
						'id': match['team' + str(i+1)],
						'name': tameName,
						'logo': teamLogo
					}
					teamsData.append(teamData)



				event = {
					'name':match.select_one('.matchEventName').text,
					'logo':match.select_one('.matchEventLogo')['src'],
				}





			# Number of match stars
			stars = len(match.select_one('.matchRating').find_all('i', class_="fa fa-star"))
			
			# Match date
			date = match.select_one('.matchTime')['data-unix']
			date = int(date)
			date /= 1000
			date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%dT%H:%M:%SZ')

			# Match type
			matchType = match.select_one('.matchMeta').text

			matchStats = {
				'id':matchID,
				'link':self.base_url + link,
				'teams':teamsData,
				'event':event,
				'type':matchType,
				'stars':stars,
				'date':date,
			}


			response.append(matchStats)
			



		return response



