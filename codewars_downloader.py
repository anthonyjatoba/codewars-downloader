import os

import requests
from bs4 import BeautifulSoup

from challenge import Challenge
from download_source import download_source
from parser import Parser

CHALLENGE_URL = 'https://www.codewars.com/api/v1/code-challenges/{}'

file_formats = {
    'Python': 'py',
}

if __name__ == '__main__':

    download_source()

    with open('challenges.html', 'r') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
        solutions_elements = soup.findAll("div", {"class": "list-item solutions"})

    # dict to store the challenges
    challenges = {'%d kyu' % n: [] for n in range(1, 9)}
    for solution_element in solutions_elements[:5]:
        parser = Parser(solution_element)

        challenge_id = parser.parse_id()

        # using codewars api to get info about the challenge
        response = requests.get(CHALLENGE_URL.format(challenge_id))
        js = response.json()

        # creating a challenge object
        challenge = Challenge.fromjson(js)

        challenge.code = parser.parse_code()
        challenge.language = parser.parse_language()

        challenges[challenge.kyu].append(challenge)

    for key, challenge_list in challenges.items():
        for challenge in challenge_list:
            path = 'solutions/{}/{}'.format(key, challenge.name)

            os.makedirs(path, exist_ok=True)

            with open(path + '/' + 'README.md', 'w') as file:
                file.write(challenge.description)

            with open(path + '/' + challenge.name + file_formats[challenge.language], 'w') as file:
                file.write(challenge.code)
