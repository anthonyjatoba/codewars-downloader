class Parser:

    def __init__(self, solution_element):
        self.solution_element = solution_element

    def parse_id(self):
        title = self.solution_element.find('div', {'class': 'item-title'})
        return title.find('a')['href'].split('/')[-1]

    def parse_language(self):
        return self.solution_element.find('h6').get_text()[:-1]

    def parse_code(self):
        return self.solution_element.findAll('code')[0].get_text()
