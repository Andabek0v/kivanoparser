import os
import time
import schedule
import datetime as dt

from parser import Parser
from const import DOMEN

def read_nested_dict(dict_: dict):
    """
        Struct printing nested dictionary data type 
    """
    main_numeric = 1
    for main_title, nest_dict in dict_.items():
        print(f'{main_numeric}. {main_title}')
        first_nest_num = 1
        if type(nest_dict) == dict:
            for title, links in nest_dict.items():
                print(f'\n\t{main_numeric}.{first_nest_num}. {title}\n')
                if type(links) != str: 
                    deep_numeric = 1
                    for link in links:
                        print(f'\t\t{main_numeric}.{first_nest_num}.{deep_numeric}. {DOMEN + link}')
                        deep_numeric += 1
                else:
                    print(f'\t\t{DOMEN + links}')
                first_nest_num += 1
        else:
            print(f'\t{main_numeric}.{first_nest_num}. {DOMEN + nest_dict}')
        print('=='*70)
        main_numeric += 1


def ask_user_section() -> str:
    description = """
                        Hello!
    You are welcomed by a scraper for the site kivano.kg.
    You will see a list of all products on the site. 
    Нou need a link by numbering from which you want to get data.
    Example: 4.1.2\n"""
    print(description)
    answer = input('Enter the numeric separated by `.` : ')
    return answer


def find_link_by_numeric(dict_: dict, numeric: str) -> str:
    """
        This function find link by numeric and return link
    """
    numeric_list = [int(i) for i in numeric.split('.')]
    title = list(dict_.keys())[numeric_list[0]-1]
    if type(dict_[title]) == dict:
        sub_title = list(dict_[title].keys())[numeric_list[1]-1]
        link = dict_[title][sub_title][numeric_list[-1]-1]
        return link
    else:
        return dict_[title]

def create_directory() -> str:
    """
        This function create new diretory and return path
    """
    path = "/home/hello/Desktop/Python19/week4/web-crawling/kivano/data/"
    new_folder =  str(dt.date.today())
    try: 
        os.mkdir(path=path+new_folder)
    except Exception as ex:
        print(f'Cannot create directory `{new_folder}’: File exists')
    return path + new_folder


def send_message(data) -> None:
    """
        Print message in system notification
    """
    title = 'Your parser script performed an action'
    message = f'{len(data)} data parsed!'
    os.system(f'notify-send "{title}" "{message}"')


def cyclic_start(link):
    """
        Loop for running script every hour
    """
    schedule.every(1).hours.do(Parser.create_new_instance(link).main)
    while True:
        schedule.run_pending()
        time.sleep(1)