import os
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

    challenges = {'{} kyu'.format(i):[] for i in range(1, 9)}
    for solution_element in solutions_elements[:3]:
        title = solution_element.find('div', {'class': 'item-title'})
        challenge_id = title.find('a')['href'].split('/')[-1]

        CHALLENGE_URL = CHALLENGE_BASE_URL.format(challenge_id)
        
        response = requests.get(CHALLENGE_URL)
        js = response.json()
        
        challenge = Challenge.fromjson(js)

        challenge.code = solution_element.findAll('code')[0].get_text()
        
        challenges[challenge.kyu].append(challenge)

    for key, challenge_list in challenges.items():
        print(key)
        for challenge in challenge_list:
            dir = 'solutions/{}/{}'.format(key, challenge.name)
            os.makedirs(dir, exist_ok=True)

            with open(dir + '/' + 'README.md', 'w') as file:
                file.write(challenge.description)

            with open(dir + '/' + challenge.name + '.py', 'w') as file:
                file.write(challenge.code)