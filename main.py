import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from utils import save_json_file

URL: str = 'https://storage.googleapis.com/jus-challenges/challenge-crawler.html'


def remove_duplicated_space_and_line_breaks_from_text(text):
    return re.sub(pattern=r'\s+', repl=' ', string=text.strip())


def remove_label_from_text(text, regex_pattern):
    return re.sub(string=text, pattern=regex_pattern, repl='')


def extract_date_from_text(text):
    regex = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    return regex.search(text).group(0)


def extract_data_information_from_jurisprudence_raw_data(raw_data, regex_pattern):
    rows = raw_data.find_all('tr')
    regex = re.compile(r'{0}'.format(regex_pattern))

    for element in rows:
        if regex.search(element.text.strip()):
            return remove_duplicated_space_and_line_breaks_from_text(
                remove_label_from_text(text=element.text, regex_pattern=regex))


def extract_process_number_from_jurisprudence_raw_data(raw_data):
    return raw_data.find_next('a').text.strip()


def extract_subject_from_jurisprudence_raw_data(raw_data):
    pass


def extract_summary_from_jurisprudence_raw_data(raw_data):
    # TODO: Realizar tratamentos (ex.: remoção da label 'Ementa:', encode, remover caracteres especiais como \n)
    # TODO: Limpar final da ementa (remover espaços ou caracteres especiais como - e colocar ponto final)
    rows = raw_data.find_all('tr')
    regex = re.compile(r'Ementa:\s+')

    for element in rows:
        if regex.search(element.text.strip()):
            summary_div = element.find('div')
            summary = remove_label_from_text(text=summary_div.text, regex_pattern=regex)
            return remove_duplicated_space_and_line_breaks_from_text(summary)


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
            # TODO: Corrigir extração do compo Relator(a)
            jurisprudence = {
                "id": (index + 1),
                "numeroProcesso": extract_process_number_from_jurisprudence_raw_data(jurisprudence_raw_data),
                "assunto": extract_data_information_from_jurisprudence_raw_data(raw_data=jurisprudence_raw_data,
                                                                                regex_pattern='Classe/Assunto:\s+'),
                "ementa": extract_data_information_from_jurisprudence_raw_data(raw_data=jurisprudence_raw_data,
                                                                               regex_pattern='Ementa:\s+'),
                "relator": extract_data_information_from_jurisprudence_raw_data(raw_data=jurisprudence_raw_data,
                                                                                regex_pattern='Relator(a):\s+'),
                "comarca": extract_data_information_from_jurisprudence_raw_data(raw_data=jurisprudence_raw_data,
                                                                                regex_pattern='Comarca:\s+'),
                "orgaoJulgador": extract_data_information_from_jurisprudence_raw_data(raw_data=jurisprudence_raw_data,
                                                                                      regex_pattern='Órgão julgador:\s+'),
                "dataJulgamento": extract_data_information_from_jurisprudence_raw_data(raw_data=jurisprudence_raw_data,
                                                                                       regex_pattern='Data do julgamento:\s+'),
                "dataPublicacao": extract_data_information_from_jurisprudence_raw_data(raw_data=jurisprudence_raw_data,
                                                                                       regex_pattern='Data de publicação:\s+'),
            }

            jurisprudence_list.append(jurisprudence)

        save_json_file(data=jurisprudence_list, file_name='result')


if __name__ == '__main__':
    main()
