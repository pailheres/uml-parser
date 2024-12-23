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
class ProcessPlantUmlTree(lark.visitors.Transformer):
    def __default__(self, data, children, meta):
        # Default method to handle unknown rules
        return children or data

    def VISIBILITY(self, item):
        visi = 'private' if item.value == '-' else 'protected' if item.value == '#' else 'public'
        return {item.type : visi}

    def FUNC_NAME(self, item):
        return {item.type : item.value}

    def CONSTRUCT_NAME(self, item):
        return {item.type : item.value}

    def PARAM_NAME(self, item):
        return {item.type : item.value}

    def VAR_NAME(self, item):
        return {item.type : item.value}

    def CLASS_NAME(self, item):
        return {item.type : item.value}

    def TYPE(self, item):
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
        #print('C')
        #print(item)
        for d in item:
            result.update(d)
        return {'class' : result}

    def RELATION_ARROW(self, item):
        arrow = 'extension' if item.value == '<|--' else 'composition' if item.value == '*--' else 'aggregation' if item.value == 'o--' else 'use'
        return {item.type : arrow}

    def RELATION_CLASS_NAME_BEFORE(self, item):
        return {item.type : item.value}

    def RELATION_CLASS_NAME_AFTER(self, item):
        return {item.type : item.value}
        
    def RELATION_LABEL(self, item):
        return {item.type : item.value}

    def RELATION_TEXT(self, item):
        return {item.type : item.value}

    def relationship(self, item):
        result = {}
        #print('R')
        #print(item)
        for d in item:
            #print(d)
            result.update(d)
        return {'relationship' : result}

    def check_and_add_state(self, a_state, a_state_list):
        #print(a_state)
        the_found = 0
        if a_state == '[*]':
            the_found = 1
        else :
            for st in a_state_list:
                #print('qwerty')
                #print(st)
                if a_state == st['name']:
                    the_found = 1
                    break
        if the_found == 0:
            a_state_list.append({'name': a_state, 'out_states': []})
        return

    def add_out_transition_to_state(self, a_from_state, a_to_state, a_state_list):
        #print('qwerty')
        #print(a_from_state)
        #print(a_to_state)
        #print(a_state_list)
        match = next((item for item in a_state_list if item.get('name') == a_from_state), None)
        if (match != None) :
            match['out_states'].append(a_to_state)
        return

    def state_declaration(self, item):
        result = {}
        result['name'] = ''
        result['states'] = []
        result['transitions'] = []
        result['out_states'] = []
        for d in item:
            #print("d:")
            #print(d)
            for key, value in d.items():
                if key == 'name':
                    result[key] = value
                elif key == 'transition':
                    result['transitions'].append(value)
                elif key == 'state':
                    result['states'].append(value)

        for tr in result['transitions']:
            self.check_and_add_state(tr['STATE_NAME_FROM'], result['states'])
            self.check_and_add_state(tr['STATE_NAME_TO'], result['states'])

        for tr in result['transitions']:
            self.add_out_transition_to_state(tr['STATE_NAME_FROM'], tr['STATE_NAME_TO'], result['states'])

        #pp.pprint('blob11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111:')
        #pp.pprint(result)
        #pp.pprint('222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222:')
            
        return {'state' : result}
        #return result

    def STATE_NAME(self, item):
        return {'name' : item.value}

    def STATE_NAME_FROM(self, item):
        return {item.type : item.value}

    def STATE_NAME_TO(self, item):
        return {item.type : item.value}

    def TRANSITION_LABEL(self, item):
        return {item.type : item.value}

    def transition(self, item):
        result = {}
        for d in item:
            #print("t:")
            #print(d)
            result.update(d)
        #print(result)
        return {'transition' : result}

    def state_diagram(self, item):
        result = {}
        result['states'] = []
        for d in item:
            for key, value in d.items():
                if key == 'state':
                    result['states'].append(value)
        return result


def f_write_fsm_file(a_fsm):
    print('qwerty1')
    pp.pprint(a_fsm)

    filename = f"out/{a_fsm['name'].lower()}.hpp"
    content = template_fsm_hpp.render(a_fsm)
    with open(filename, mode='w', encoding='utf-8') as message:
        message.write(content)
        print(f'... wrote {filename}')
    if ('states' in a_fsm):
        for the_child_fsm in a_fsm['states']:
            if ('states' in the_child_fsm):
                f_write_fsm_file(the_child_fsm)

    return;


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
    #grammar_file_path = os.path.join(dir_path, "grammar", "grammar_plantuml.ebnf")
    grammar_file_path = os.path.join(dir_path, "grammar", "grammar_mermaid.ebnf")
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
    #print(tree.pretty())
    #print ("-----\n")
    #print ("-----\n")
    #print(tree)
    pp.pprint(tree)
    #print ("-----\n")
    #print ("-----\n")
    #print ("-----\n")
    #print ("-----\n")
    #print ("-----\n")

    #ProcessPlantUmlTree2().visit_topdown(tree)
    the_model = ProcessPlantUmlTree().transform(tree)
    #print(tree.pretty())
    pp.pprint(the_model)
    ## Convert Lark tree to nested dictionary
    #tree_dict = tree_to_dict(tree)
    #print(tree_dict)
    
#    json_str = tree_to_json_str(tree)
#    print(json_str)

    environment = Environment(loader=FileSystemLoader("src/templates/"))
    template_class_hpp = environment.get_template("template_class_hpp.txt")
    template_fsm_hpp = environment.get_template("template_FSM_hpp.txt")



    relationship_dicts_list = [d['relationship'] for d in the_model if 'relationship' in d]
    extension_dicts_list = [d for d in relationship_dicts_list if d['RELATION_ARROW'] == 'extension']


    class_dicts = [d['class'] for d in the_model if 'class' in d]
    for the_class in class_dicts:
        the_class['base_classes'] = [d['RELATION_CLASS_NAME_BEFORE'] for d in extension_dicts_list if d['RELATION_CLASS_NAME_AFTER'] == the_class['CLASS_NAME']]
        filename = f"out/{the_class['CLASS_NAME'].lower()}.hpp"
        content = template_class_hpp.render(the_class)
        with open(filename, mode='w', encoding='utf-8') as message:
            message.write(content)
            print(f'... wrote {filename}')

    for the_fsm in the_model['states']:
        f_write_fsm_file(the_fsm)

    #fsm_dicts = [d['state'] for d in the_model if 'state' in d]
    #for the_fsm in fsm_dicts:
    #    filename = f"out/{the_fsm['name'].lower()}.hpp"
    #    content = template_fsm_hpp.render(the_fsm)
    #    with open(filename, mode='w', encoding='utf-8') as message:
    #        message.write(content)
    #        print(f'... wrote {filename}')
