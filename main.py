import os
import json

import utils
from parser import Parser

json_file = "kivano_sections.json"
path = os.getcwd() 

with open(f'{path}/{json_file}', "r") as file:
    products_tree = json.load(file)
    utils.read_nested_dict(products_tree)

answer = utils.ask_user_section()
link = utils.find_link_by_numeric(products_tree, answer)

parser = Parser(link)
parser.main()

