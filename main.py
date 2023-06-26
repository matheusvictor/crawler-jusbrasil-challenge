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
    regex = re.compile(regex_pattern)

    for element in rows:
        if regex.search(element.text.strip()):
            return remove_duplicated_space_and_line_breaks_from_text(
                remove_label_from_text(text=element.text, regex_pattern=regex))


def extract_process_number_from_jurisprudence_raw_data(raw_data):
    return raw_data.find_next('a').text.strip()


def main():
    try:
        html = urlopen(URL)
    except HTTPError as e:
        print(e)
    except URLError:
        print(f'This server could not be found!')
    else:
        bs = BeautifulSoup(html.read(), 'html.parser')

        main_table = bs.find('div', {'id': 'divDadosResultado-A'}).find('table')

        section_information_tables = main_table.find_all('table')

        jurisprudence_list = list()
        for index, jurisprudence_raw_data in enumerate(section_information_tables):
            jurisprudence = dict(
                _id=extract_process_number_from_jurisprudence_raw_data(jurisprudence_raw_data),
                numeroProcesso=extract_process_number_from_jurisprudence_raw_data(jurisprudence_raw_data),
                assunto=extract_data_information_from_jurisprudence_raw_data(
                    raw_data=jurisprudence_raw_data,
                    regex_pattern=r'Classe\/Assunto:\s+'
                ),
                ementa=extract_data_information_from_jurisprudence_raw_data(
                    raw_data=jurisprudence_raw_data,
                    regex_pattern=r'Ementa:\s*'
                ),
                relator=extract_data_information_from_jurisprudence_raw_data(
                    raw_data=jurisprudence_raw_data,
                    regex_pattern=r'Relator\(\w\):\s*'
                ),
                comarca=extract_data_information_from_jurisprudence_raw_data(
                    raw_data=jurisprudence_raw_data,
                    regex_pattern=r'Comarca:\s*'
                ),
                orgaoJulgador=extract_data_information_from_jurisprudence_raw_data(
                    raw_data=jurisprudence_raw_data,
                    regex_pattern=r'Órgão\sjulgador:\s*'
                ),
                dataJulgamento=extract_data_information_from_jurisprudence_raw_data(
                    raw_data=jurisprudence_raw_data,
                    regex_pattern=r'Data\sdo\sjulgamento:\s*'
                ),
                dataPublicacao=extract_data_information_from_jurisprudence_raw_data(
                    raw_data=jurisprudence_raw_data,
                    regex_pattern=r'Data\sde\spublicação:\s*'
                ),
            )

            jurisprudence_list.append(jurisprudence)

        try:
            save_json_file(data=jurisprudence_list, file_name='result')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
