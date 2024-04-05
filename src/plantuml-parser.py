# Copyright 2018 Pedro Cuadra - pjcuadra@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import pprint
import os
import json
import lark


#from lark import Lark
from sys import argv
from jinja2 import Environment, FileSystemLoader


#lark_tree_to_json is from https://gist.github.com/charles-esterbrook/9ab557d70391fd85ebac2b1a59a326cf
def tree_to_json_str(item):
    output = []
    tree_to_json(tree, output.append)  # will build output in memory
    return ''.join(output)

def tree_to_json(item, write=None):
    """ Writes a Lark tree as a JSON dictionary. """
    if write is None: write = sys.stdout.write
    _tree_to_json(item, write, 0)

def _tree_to_json(item, write, level):
    indent = '  ' * level
    level += 1
    if isinstance(item, lark.Tree):
        write(f'{indent}{{ "type": "{item.data}", "children": [\n')
        sep = ''
        for child in item.children:
            write(indent)
            write(sep)
            _tree_to_json(child, write, level)
            sep = ',\n'
        write(f'{indent}] }}\n')
    elif isinstance(item, lark.Token):
        # reminder: Lark Tokens are directly strings
        # token attrs include: line, end_line, column, end_column, pos_in_stream, end_pos
        write(f'{indent}{{ "type": "{item.type}", "text": "{item}", "line": {item.line}, "col": {item.column} }}\n')
    #else:
        #print ("qwerty" + item)
        #assert False, item  # fall-through

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            if len(argv) > 1:
                if argv[1][0] != '-':
                    opts[argv[0]] = argv[1]
                else:
                    opts[argv[0]] = True
            elif len(argv) == 1:
                opts[argv[0]] = True

        # Reduce the argument list by copying it starting from index 1.
        argv = argv[1:]
    return opts


if __name__ == '__main__':
    myargs = getopts(argv)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    #grammar_file_path = os.path.join(dir_path, "grammar", "grammar.ebnf")
    grammar_file_path = os.path.join(dir_path, "grammar", "grammar_for_lalr.ebnf")
    f_gram = open(grammar_file_path)

    #parser = lark.Lark(f_gram.read())
    parser = lark.Lark(f_gram.read() , parser="lalr")

    if '-i' in myargs:
        f = open(myargs['-i'])
    else:
        exit(1)

    if '-v' in myargs:
        logging.basicConfig(level=logging.INFO)

    tree = parser.parse(f.read())
    print(tree)
    print ("-----\n")
    print(tree.pretty())
    
    json_str = tree_to_json_str(tree)
    print(json_str)
    
#    environment = Environment(loader=FileSystemLoader("src/templates/"))
#    template_class_hpp = environment.get_template("template_class_hpp.txt")
#    
#    
#    the_classes = [{
#        'class_name' : 'qwerty',
#        'functions' : [{
#            'name' : 'f_func',
#            'return_type' : 'void',
#            'params' : [{
#                'type' : 'UINT8',
#                'name' : 'a_param'
#            }
#        }]
#    }]
#    
#    for the_class in the_classes:
#        filename = f"out/{the_class['class_name'].lower()}.hpp"
#        content = template_class_hpp.render(the_class)
#        with open(filename, mode='w', encoding='utf-8') as message:
#            message.write(content)
#            print(f'... wrote {filename}')
