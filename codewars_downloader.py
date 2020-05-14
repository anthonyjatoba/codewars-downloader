import re
import requests
import json
from bs4 import BeautifulSoup
from challenge import Challenge
from download_source import download_source

CHALLENGE_BASE_URL = 'https://www.codewars.com/api/v1/code-challenges/{}' 

if __name__ == '__main__':
    
    # download_source()

    with open('challenges.html', 'r') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
        solutions_elements = soup.findAll("div", {"class": "list-item solutions"})

    for solution_element in solutions_elements[:3]:
        title = solution_element.find('div', {'class': 'item-title'})
        challenge_id = title.find('a')['href'].split('/')[-1]

        CHALLENGE_URL = CHALLENGE_BASE_URL.format(challenge_id)
        
        response = requests.get(CHALLENGE_URL)
        js = response.json() 
        challenge = Challenge.fromjson(js)

        challenge.code = solution_element.findAll('code')[0].get_text()
        print()
        print(challenge)
        print(challenge.code)
