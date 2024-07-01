from collections import defaultdict
#########################################################################
def first_set(grammar):
    first = defaultdict(set)
    nullable = set()


    def add_first(lhs, production):
        i = 0
        while i < len(production):
            symbol = production[i]
            if symbol.islower() or not symbol.isalpha():
                first[lhs].add(symbol)
                break
            else:
                first[lhs] |= (first[symbol] - {'λ'})
                if symbol not in nullable:
                    break
            i += 1
        if i == len(production):
            first[lhs].add('λ')


    for lhs, rhs in grammar.items():
        for production in rhs:
            if production == 'λ':
                nullable.add(lhs)
                first[lhs].add('λ')
            elif production[0].islower() or not production[0].isalpha():
                first[lhs].add(production[0])
    
    changed = True
    while changed:
        changed = False
        for lhs, rhs in grammar.items():
            for production in rhs:
                before_change = len(first[lhs])
                add_first(lhs, production)
                if len(first[lhs]) > before_change:
                    changed = True

    return first, nullable
########################################################################

########################################################################
def follow_set(grammar, start_symbol, first, nullable):
    follow = defaultdict(set)
    follow[start_symbol].add('$')


    def add_follow(lhs, production, trailer):
        for symbol in reversed(production):
            if symbol.islower() or not symbol.isalpha():
                trailer = {symbol}
            else:
                follow[symbol] |= trailer
                if symbol in nullable:
                    trailer |= (first[symbol] - {'λ'})
                else:
                    trailer = first[symbol]


    changed = True
    while changed:
        changed = False
        for lhs, rhs in grammar.items():
            for production in rhs:
                trailer = follow[lhs]
                before_change = {symbol: len(follow[symbol]) for symbol in production if symbol.isalpha()}
                add_follow(lhs, production, trailer)
                for symbol in production:
                    if symbol.isalpha() and len(follow[symbol]) > before_change[symbol]:
                        changed = True

    return follow
########################################################################
# Function to check if the grammar is LL(1)
def ll1Checker(grammar, start_symbol):
    first, nullable = first_set(grammar)
    follow = follow_set(grammar, start_symbol, first, nullable)

    for lhs, rhs in grammar.items():
        local_first = []
        for production in rhs:
            production_first = set()
            i = 0
            while i < len(production):
                symbol = production[i]
                if symbol.islower() or not symbol.isalpha():
                    production_first.add(symbol)
                    break
                else:
                    production_first |= first[symbol]
                    if symbol not in nullable:
                        break
                i += 1
            if i == len(production):
                production_first |= follow[lhs]
            local_first.append(production_first)

        for i in range(len(local_first)):
            for j in range(i + 1, len(local_first)):
                if local_first[i] & local_first[j]:
                    return False

    return True
########################################################################
# Given grammar
#this is a LL1
grammar = {
    'E': ['TA'],
    'A': ['+TA', 'λ'],
    'T': ['FB'],
    'B': ['*FB', 'λ'],
    'F': ['(E)', 'id']
}

#not LL1
grammar2 = {
    'E': ['E+T','T'],
    'T': ['T*F', 'F'],
    'F': ['(E)', 'id']
}
#not ll1
grammar3 = {
    'S': ['AB','Bd'],
    'A': ['aA','d'],
    'B': ['bB','λ']
}
#this is LL1
grammar4 = {
    'S': ['ABD','bd'],
    'A': ['aA','d'],
    'B': ['bB','λ'],
    'D': ['AD','λ']
}
#not ll1
grammar5 = {
    'S': ['AB','bd'],
    'A': ['aA','λ'],
    'B': ['bB','λ']
}
#test
#its ll1
grammar6 = {
    'S': ['ABC'],
    'A': ['a', 'λ'],
    'B': ['b', 'λ'],
    'C': ['c', 'λ']
}

#not ll1
grammar7 = {
    'S': ['aA', 'aB'],
    'A': ['c'],
    'B': ['d']
}
#its ll1
grammar = {
    'S': ['aB', 'bA'],
    'A': ['a', 'λ'],
    'B': ['b', 'λ']
}
#not ll1
grammar9 = {
    'S': ['AC', 'AD'],
    'A': ['a', 'λ'],
    'C': ['c'],
    'D': ['d']
}

#ll1 
grammar10 = {
    'S': ['AB'],
    'A': ['aA', 'λ'],
    'B': ['bB', 'λ']
}

start_symbol = 'S'

if ll1Checker(grammar, start_symbol):
    print("The grammar is LL(1).")
else:
    print("The grammar is not LL(1).")
