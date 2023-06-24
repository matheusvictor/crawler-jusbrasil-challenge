import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from utils import save_json_file

URL: str = 'https://storage.googleapis.com/jus-challenges/challenge-crawler.html'


def extract_process_number_from_jurisprudence_raw_data(raw_data):
    return raw_data.find_next('a').text.strip()


def extract_subject_from_jurisprudence_raw_data(raw_data):
    pass


def extract_summary_from_jurisprudence_raw_data(raw_data):
    rows = raw_data.find_all('tr')

    for element in rows:
        regex = re.compile(r'Ementa:\s+')
        if regex.search(element.text.strip()):
            summary_div = element.find('div')
            summary = summary_div.text.strip()
            # TODO: Realizar tratamentos (ex.: remoção da label 'Ementa:', encode, remover caracteres especiais como \n)
            return summary


def extract_reporter_from_jurisprudence_raw_data(raw_data):
    pass


def extract_county_from_jurisprudence_raw_data(raw_data):
    pass


def extract_judging_from_jurisprudence_raw_data(raw_data):
    pass


def extract_judgment_date_from_jurisprudence_raw_data(raw_data):
    pass


def extract_publish_date_from_jurisprudence_raw_data(raw_data):
    pass


def main():
    try:
        html = urlopen(URL)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print('This server could not be found!')
    else:
        bs = BeautifulSoup(html.read(), 'html.parser')

        main_table = bs.find('div', {'id': 'divDadosResultado-A'}).find('table')

        section_information_tables = main_table.find_all('table')

        jurisprudence_list = list()
        for index, jurisprudence_raw_data in enumerate(section_information_tables):
            jurisprudence = {
                "id": (index + 1),
                "numeroProcesso": extract_process_number_from_jurisprudence_raw_data(jurisprudence_raw_data),
                "assunto": extract_subject_from_jurisprudence_raw_data(jurisprudence_raw_data),
                "ementa": extract_summary_from_jurisprudence_raw_data(jurisprudence_raw_data),
                "relator": extract_reporter_from_jurisprudence_raw_data(jurisprudence_raw_data),
                "comarca": extract_county_from_jurisprudence_raw_data(jurisprudence_raw_data),
                "orgaoJulgador": extract_judging_from_jurisprudence_raw_data(jurisprudence_raw_data),
                "dataJulgamento": extract_judgment_date_from_jurisprudence_raw_data(jurisprudence_raw_data),
                "dataPublicacao": extract_publish_date_from_jurisprudence_raw_data(jurisprudence_raw_data),
            }

            jurisprudence_list.append(jurisprudence)

        save_json_file(data=jurisprudence_list, file_name='result')


if __name__ == '__main__':
    main()
