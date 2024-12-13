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
import os
import json
import lark

#from lark import Lark
from sys import argv
from jinja2 import Environment, FileSystemLoader

import pprint
pp = pprint.PrettyPrinter(indent=1)

# Define a custom transformer to process a PlantUml Tree
class ProcessRequirementTree(lark.visitors.Transformer):
    def __default__(self, data, children, meta):
        # Default method to handle unknown rules
        return children or data

    def REQ_ID(self, item):
        return {item.type : item.value}

    def SOURCE(self, item):
        return {item.type : item.value}

    def PRIORITY(self, item):
        return {item.type : item.value}

    def STATUS(self, item):
        return {item.type : item.value}

    def VERIF_METHOD(self, item):
        return {item.type : item.value}

    def DEPENDENCIES(self, item):
        return {item.type : item.value}

    def DESCRIPTION(self, item):
        return {item.type : item.value}

    def DETAILS(self, item):
        return {item.type : item.value}

    def variable(self, item):
        result = {}
        for d in item:
            result.update(d)
        return {'variable' : result}

    def param(self, item):
        return item  #ca va dans param_list, donc pas besoin d'en faire un {key: value}, on sait deja que la liste contient juste des params

    def param_list(self, item):
        result = []
        for L in item:
            the_dict = {}
            for d in L:
                the_dict.update(d)
            result.append(the_dict)
        return {'param_list' : result}

    def function(self, item):
        result = {}
        for d in item:
            result.update(d)
        return {'function' : result}

    def constructor(self, item):
        result = {}
        for d in item:
            result.update(d)
        return {'constructor' : result}

    def class_element(self, item):
        #vari_or_func_dict = next((d for d in item if any(key in d for key in ['variable', 'function'])), None)
        vari_dict = next((d for d in item if any(key in d for key in ['variable'])), None)
        func_dict = next((d for d in item if any(key in d for key in ['function'])), None)
        construct_dict = next((d for d in item if any(key in d for key in ['constructor'])), None)
        visi_dict = next((d for d in item if any('VISIBILITY')), None)
        #vari_or_func_dict.update(visi_dict)
        if (vari_dict != None):
            vari_dict['variable'].update(visi_dict)
        if (func_dict != None):
            func_dict['function'].update(visi_dict)
        return vari_dict or func_dict or construct_dict

    def class_element_list(self, item):
        the_keys = ['variable', 'function', 'constructor']
        the_keys_dict = {}
        for key in the_keys:
            the_keys_dict[key] = {}
        result = []
        for d in item:  # loop the dictionaries list
            for key in the_keys:
                if key in d:
                    visi = 'public'
                    if 'VISIBILITY' in d[key]:
                        visi = d[key]['VISIBILITY']
                    if visi not in the_keys_dict[key]:
                        the_keys_dict[key][visi] = []
                    the_keys_dict[key][visi].append(d[key])
        return the_keys_dict

    def class_def(self, item):
        result = {}
        for d in item:
            result.update(d)
        return {'class' : result}

    def RELATION_ARROW(self, item):
        arrow = 'extension' if item.value == '<|--' else 'composition' if item.value == '*--' else 'aggregation' if item.value == 'o--' else 'use'
        return {item.type : arrow}

    def RELATION_CLASS_NAME(self, item):
        return {item.type : item.value}
        
    def RELATION_LABEL(self, item):
        return {item.type : item.value}

    def RELATION_TEXT(self, item):
        return {item.type : item.value}

    def relationship(self, item):
        result = []
        #print('A')
        #print(item)
        #for L in item:
        #    the_dict = {}
        #    for d in L:
        #        the_dict.update(d)
        #    result.append(the_dict)
        return {'relationship' : result}

    def start(self, item):
        the_model = {}
#        the_keys = ['requirement']
#        for key in the_keys:
#            the_model[key] = []
#
#        for d in item:
#            for key in the_keys:
#                if key in d:
#                    the_model[key].append(d)
#
        print("z")
        print(the_model)
        return the_model
    

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
    grammar_file_path = os.path.join(dir_path, "grammar", "grammar_req.ebnf")
    #grammar_file_path = os.path.join(dir_path, "grammar", "grammar_essai.ebnf")
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
    pp.pprint(tree)

#    #ProcessPlantUmlTree2().visit_topdown(tree)
    the_model = ProcessRequirementTree().transform(tree)
    #print(tree.pretty())
    #pp.pprint(the_model)
#
#    environment = Environment(loader=FileSystemLoader("src/templates/"))
#    template_class_hpp = environment.get_template("template_class_hpp.txt")
#
#    for the_class_dict in the_model['class']:
#        the_class = the_class_dict['class']
#        filename = f"out/{the_class['CLASS_NAME'].lower()}.hpp"
#        content = template_class_hpp.render(the_class)
#        with open(filename, mode='w', encoding='utf-8') as message:
#            message.write(content)
#            print(f'... wrote {filename}')
