#Script constructs the plural of an English noun according to various plural rules
#Not conclusive, some rules not taken care of
#use of generators

import re

rules = []
def build_apply_match_functions(pattern, search, replace):
    '''A closure function that build two function dynamicaly;
    match_rule => matches a pattern against a noun, returns true or None
    apply_rule => applies the plural rule if the corresponding match_rule was succesful
    '''
    def match_rule(word):
        return re.search(pattern, word)

    def apply_rule(word):
        return re.sub(search, replace, word)

    return (match_rule, apply_rule)

def rules(rules_file='plural-rules.txt'):
    '''A generator function that builds and spits macth_rule and apply_rule functions on demand'''
    with open(rules_file, encoding='utf-8') as pattern_file:
        for line in pattern_file:
            pattern, search, replace = line.split(None, 3)
            yield build_apply_match_functions(pattern, search, replace)

def plural(noun):
    '''Generic function that takes an English noun and constructs the plural'''
    for match_rule, apply_rule in rules():
        if match_rule(noun):
            return apply_rule(noun)

if __name__ == "__main__":
    noun = input("English noun: ")
    print('Plural: {}'.format(plural(noun.lower())))
