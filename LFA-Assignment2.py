import json

def operator_precedence(op):
    if op in {'*', '+', '?'}:
        return 3
    if op == '.':  # concatenare
        return 2
    if op == '|':
        return 1
    return 0

def insert_concatenation(regex):
    result = ''
    for i in range(len(regex)):
        result += regex[i]
        if i + 1 < len(regex):
            curr, next_char = regex[i], regex[i + 1]
            if curr not in '(|' and next_char not in '|)*+?':
                result += '.'
    return result

def regex_to_postfix(regex):
    regex = insert_concatenation(regex)
    output, stack = '', []

    for char in regex:
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop()
        elif char in {'*', '+', '?', '.', '|'}:
            while stack and operator_precedence(stack[-1]) >= operator_precedence(char):
                output += stack.pop()
            stack.append(char)
        else:
            output += char

    while stack:
        output += stack.pop()
    return output

class State:
    def __init__(self):
        self.edges = {}
        self.epsilon = []

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

class DFA:
    def __init__(self):
        self.states = {}
        self.start = None
        self.accepts = set()

def postfix_to_nfa(postfix):
    stack = []
    for char in postfix:
        if char in '*+?':
            nfa = stack.pop()
            start, accept = State(), State()

            if char == '*':
                start.epsilon = [nfa.start, accept]
                nfa.accept.epsilon = [nfa.start, accept]
            elif char == '+':
                start.epsilon = [nfa.start]
                nfa.accept.epsilon = [nfa.start, accept]
            elif char == '?':
                start.epsilon = [nfa.start, accept]
                nfa.accept.epsilon = [accept]

            stack.append(NFA(start, accept))

        elif char == '.':
            nfa2, nfa1 = stack.pop(), stack.pop()
            nfa1.accept.epsilon = [nfa2.start]
            stack.append(NFA(nfa1.start, nfa2.accept))

        elif char == '|':
            nfa2, nfa1 = stack.pop(), stack.pop()
            start, accept = State(), State()
            start.epsilon = [nfa1.start, nfa2.start]
            nfa1.accept.epsilon = [accept]
            nfa2.accept.epsilon = [accept]
            stack.append(NFA(start, accept))

        else:
            start, accept = State(), State()
            start.edges[char] = [accept]
            stack.append(NFA(start, accept))

    return stack.pop()

def epsilon_closure(states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for next_state in state.epsilon:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def move(states, symbol):
    result = set()
    for state in states:
        if symbol in state.edges:
            result.update(state.edges[symbol])
    return result

def nfa_to_dfa(nfa):
    dfa = DFA()
    start_state = frozenset(epsilon_closure({nfa.start}))
    dfa.start = start_state
    dfa.states[start_state] = {}
    unprocessed = [start_state]

    while unprocessed:
        current = unprocessed.pop()
        transitions = {}
        symbols = set()

        for state in current:
            symbols.update(state.edges.keys())

        for symbol in symbols:
            if not symbol:
                continue
            next_set = epsilon_closure(move(current, symbol))
            next_frozen = frozenset(next_set)
            if next_frozen not in dfa.states:
                dfa.states[next_frozen] = {}
                unprocessed.append(next_frozen)
            transitions[symbol] = next_frozen

        dfa.states[current] = transitions

    for state_set in dfa.states:
        if nfa.accept in state_set:
            dfa.accepts.add(state_set)

    return dfa

def test_dfa_acceptance(dfa, input_str):
    current = dfa.start
    for char in input_str:
        if char in dfa.states[current]:
            current = dfa.states[current][char]
        else:
            return False
    return current in dfa.accepts

def run_tests(json_path="LFA-Assignment2_Regex_DFA_v2.json"):
    with open(json_path, 'r') as f:
        test_data = json.load(f)

    for test in test_data:
        regex = test['regex']
        test_cases = test['test_strings']
        postfix = regex_to_postfix(regex)
        nfa = postfix_to_nfa(postfix)
        dfa = nfa_to_dfa(nfa)

        for case in test_cases:
            input_str = case['input']
            expected = case['expected']
            result = test_dfa_acceptance(dfa, input_str)
            if result != expected:
                print(f"Eroare la regex: {regex}, input: '{input_str}' (asteptat: {expected}, obtinut: {result})")
                return

    print("Toate testele au fost trecute cu succes!")

if __name__ == "__main__":
    file_name = input("Introduceti numele fisierului JSON (fara extensie): ").strip()
    json_file = file_name + ".json" if file_name else "LFA-Assignment2_Regex_DFA_v2.json"
    run_tests(json_file)
