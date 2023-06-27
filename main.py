import re
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from utils import save_json_file, valid_date_format

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
            rows = jurisprudence_raw_data.find_all('tr')

            process_number = None
            subject = None
            summary = None
            reporter = None
            publish_date = None
            county = None
            judging_agent = None
            judging_date = None

            for line in rows:

                if re.compile(r'Classe\/Assunto:\s+').search(line.text.strip()):
                    subject = remove_label_from_text(text=line.text, regex_pattern=r'Classe\/Assunto:\s+')
                    subject = remove_duplicated_space_and_line_breaks_from_text(subject)
                elif re.compile(r'Ementa:\s*').search(line.text.strip()):
                    summary = remove_label_from_text(text=line.text, regex_pattern=r'Ementa:\s*')
                    summary = remove_duplicated_space_and_line_breaks_from_text(summary)
                elif re.compile(r'Relator\(\w\):\s*').search(line.text.strip()):
                    reporter = remove_label_from_text(text=line.text, regex_pattern=r'Relator\(\w\):\s*')
                    reporter = remove_duplicated_space_and_line_breaks_from_text(reporter)
                elif re.compile(r'Comarca:\s*').search(line.text.strip()):
                    county = remove_label_from_text(text=line.text, regex_pattern=r'Comarca:\s*')
                    county = remove_duplicated_space_and_line_breaks_from_text(county)
                elif re.compile(r'Órgão\sjulgador:\s*').search(line.text.strip()):
                    judging_agent = remove_label_from_text(text=line.text, regex_pattern=r'Órgão\sjulgador:\s*')
                    judging_agent = remove_duplicated_space_and_line_breaks_from_text(judging_agent)
                elif re.compile(r'Data\sdo\sjulgamento:\s*').search(line.text.strip()):
                    judging_date = remove_label_from_text(text=line.text, regex_pattern=r'Data\sdo\sjulgamento:\s*')
                    judging_date = remove_duplicated_space_and_line_breaks_from_text(judging_date)
                elif re.compile(r'Data\sde\spublicação:\s*').search(line.text.strip()):
                    publish_date = remove_label_from_text(text=line.text, regex_pattern=r'Data\sde\spublicação:\s*')
                    publish_date = remove_duplicated_space_and_line_breaks_from_text(publish_date)
                else:
                    process_number = extract_process_number_from_jurisprudence_raw_data(jurisprudence_raw_data)

            jurisprudence = dict(
                _id=(index + 1),
                numeroProcesso=process_number,
                assunto=subject,
                ementa=summary,
                relator=reporter,
                comarca=county,
                orgaoJulgador=judging_agent,
                dataJulgamento=judging_date,
                dataPublicacao=publish_date,
                _dataJulgamentoValida=valid_date_format(judging_date),
                _dataPublicacaoValida=valid_date_format(publish_date)
            )

            jurisprudence_list.append(jurisprudence)

        try:
            save_json_file(data=jurisprudence_list, file_name='result')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
