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

# Define a function to recursively convert the Lark tree to a nested structure
def tree_to_dict(item):
    the_node = 'blableblibloblu'
    the_data = None

    if isinstance(item, lark.Tree):
        if isinstance(item.data, lark.Token):
            if item.data.type == 'RULE':
                if item.data.value != '' :
                    the_node = item.data.value
                    the_data = [tree_to_dict(child) for child in item.children]
    else :
        if isinstance(item, lark.Token):
            the_node = item.type
            the_data = item.value

    return {
        the_node : the_data
    }

def tree_to_class(item):
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
        bla

def tree_to_struct(item):
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

# Define a custom transformer to process a PlantUml Tree
class ProcessPlantUmlTree2(lark.visitors.Visitor):
    start = dict

class s_class:
    variables = {}

# Define a custom transformer to process a PlantUml Tree
class ProcessPlantUmlTree(lark.visitors.Transformer):
    #def __default__(self, data, children, meta):
    #    # Default method to handle unknown rules
    #    return children or data
    #
    #def start(self, tree):
    #    #print(tree)
    #    return tree
    #    
    #def class_def(self, item):
    #    for bla in item :
    #        print(bla)
    #        if isinstance(bla, lark.Tree):
    #            print("blablabla:"+bla.data)
    #        elif isinstance(bla, lark.Token):
    #            print("blebleble:"+bla.type)
    #       
    #    print(item)
    #
    #    return item
        

    def variable(self, item):
        print("a")
#        for terminal in item.children:
#            if isinstance(terminal, lark.Token):
#                if terminal.type == 'VAR_NAME'

        if len(item) == 2:
            if isinstance(item[0], lark.Token):
                if isinstance(item[1], lark.Token):
                    print(item)
                    return item[0], item[1]

    def var(self, item):
        print("b")
        if len(item) == 1:
            print(item)
            return item[0].value

    def type(self, item):
        print("c")
        if len(item) == 1:
            print(item)
            return item[0].value

    #def variable(self, children):
    #    return "the variable"
    #
    #def type(self, tree):
    #    print(tree.data)
    #    print(tree.children)
    #    #for child in tree.children:
    #    #    self.visit(child)
    #
    #def method(self, children):
    #    return "the method"
    #
    #def relationship(self, children):
    #    return "the relationship"
    #
    #def skinparam(self, children):
    #    return "the skinparam"

if __name__ == '__main__':
    myargs = getopts(argv)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    #grammar_file_path = os.path.join(dir_path, "grammar", "grammar.ebnf")
    grammar_file_path = os.path.join(dir_path, "grammar", "grammar_for_lalr.ebnf")
    f_gram = open(grammar_file_path)

    #parser = lark.Lark(f_gram.read())
    #parser = lark.Lark(f_gram.read() , parser="lalr")#, lexer="contextual")
    parser = lark.Lark(f_gram.read() , parser="earley", ambiguity="explicit")#, lexer="contextual")

    if '-i' in myargs:
        f = open(myargs['-i'])
    else:
        exit(1)

    if '-v' in myargs:
        logging.basicConfig(level=logging.INFO)

    tree = parser.parse(f.read())
    print(tree.pretty())
    print ("-----\n")
    print ("-----\n")
    print(tree)
    print ("-----\n")
    print ("-----\n")
    print ("-----\n")
    print ("-----\n")
    print ("-----\n")
    #ProcessPlantUmlTree2().visit_topdown(tree)
    #ProcessPlantUmlTree().transform(tree)

    # Convert Lark tree to nested dictionary
    tree_dict = tree_to_dict(tree)
    print(tree_dict)

#    print(tree.pretty())
    
#    json_str = tree_to_json_str(tree)
#    print(json_str)
#    
    environment = Environment(loader=FileSystemLoader("src/templates/"))
    template_class_hpp = environment.get_template("template_class_hpp.txt")
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
    the_start = {'classes':[]}
    if 'start' in tree_dict:
        for item in tree_dict['start']:
            if 'class_def' in item:
                the_class = None
                for class_item in item['class_def']:
                    print(class_item)
                    if 'CLASS_NAME' in class_item:
                        print(class_item['CLASS_NAME'])
                        the_class = {
                            'CLASS_NAME' : class_item['CLASS_NAME'],
                            'var' : {'public':[], 'protected':[], 'private':[]},
                            'func' : {'public':[], 'protected':[], 'private':[]}
                        }
                    if 'vari_or_func' in class_item:
                        for varfunc_item in class_item['vari_or_func']:
                            if 'VISIBILITY' in varfunc_item:
                                visibility = 'public'
                                if varfunc_item['VISIBILITY'] == '#':
                                    visibility = 'protected'
                                elif varfunc_item['VISIBILITY'] == '-':
                                    visibility = 'private'
                                    
                                print(visibility)
                                if 'variable' in varfunc_item:
                                    for var_item in varfunc_item['variable']:
                                        if 'VAR_NAME' in var_item:
                                            if 'TYPE' in var_item:
                                                the_class['var'][visibility].append({'VAR_NAME': var_item['VAR_NAME'], 'TYPE' : var_item['TYPE']})
                                                    
                                                    
                                                
                                    
                                

                the_start['classes'].append(the_class)
            
    print(the_start)
        
    for the_class in the_start['classes']:
        filename = f"out/{the_class['CLASS_NAME'].lower()}.hpp"
        content = template_class_hpp.render(the_class)
        with open(filename, mode='w', encoding='utf-8') as message:
            message.write(content)
            print(f'... wrote {filename}')
