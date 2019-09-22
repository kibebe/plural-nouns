#Script constructs the plural of an English noun according to various plural rules
#Not conclusive, some rules not taken care of
#use of iterators

import re

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

class LazyRules:
    ''' Iterator that uses build_apply_match_functions to constrcuts functions
        lazily
    '''
    rules_filename = 'plural-rules.txt'
    def __init__(self):
        self.pattern_file = open(self.rules_filename, encoding='utf-8')
        self.cache = []

    def __iter__(self):
        self.cache_index = 0
        return self

    def __next__(self):
        self.cache_index += 1
        if len(self.cache) >= self.cache_index:
            return self.cache[self.cache_index - 1]

        if self.pattern_file.closed:
            raise StopIteration

        line = self.pattern_file.readline()
        if not line:
            self.pattern_file.close()
            raise StopIteration
                                   
        pattern, search, replace = line.split(None, 3)
        funcs = build_apply_match_functions(pattern, search, replace)
        self.cache.append(funcs)
        return funcs

rules = LazyRules()

def plural(noun):
    '''Generic function that takes an English noun and constructs the plural'''
    for match_rule, apply_rule in rules:
        if match_rule(noun):
            return apply_rule(noun)

if __name__ == '__main__':
    noun = input("English noun: ")
    print('Plural: {}'.format(plural(noun.lower()))) 
                                   
