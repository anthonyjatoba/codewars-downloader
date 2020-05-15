import os
from configparser import ConfigParser

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from challenge import Challenge
from download_source import download_source
from parser import Parser

CHALLENGE_URL = 'https://www.codewars.com/api/v1/code-challenges/{}'

file_formats = {
    'Python': '.py',
}

config = ConfigParser()
config.read('config.ini')

directory = config.get('settings', 'directory')

if __name__ == '__main__':
   
    # download_source()

    with open('challenges.html', 'r') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        solutions_elements = soup.findAll('div', {'class': 'list-item solutions'})

    # dict to store the challenges
    challenges = {'%d kyu' % n: [] for n in range(1, 9)}
    for solution_element in tqdm(solutions_elements, 'Parsing challenges'):
        #pbar.set_description("Processing")

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

    for kyu, challenge_list in challenges.items():
        for challenge in tqdm(challenge_list, 'Saving {}'.format(kyu)):
            kyu_path = os.path.join(directory, kyu, challenge.name)

            os.makedirs(kyu_path, exist_ok=True)

            with open(os.path.join(kyu_path, 'README.md'), 'w') as f:
                f.write(challenge.description)

            with open(os.path.join(kyu_path, challenge.name + file_formats[challenge.language]), 'w') as f:
                f.write(challenge.code)
