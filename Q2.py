'''This is python code to transform a NFA to DFA '''
import json
global_counter = 0



def load_input():
    f = open('nfa.json')
    nfa = json.load(f)
    f.close()
    '''for (k,v) in dfa.items():
        print("Key : " + k)
        for z in v:
            print(z)
            '''
    return nfa


''' function to convert num to binary '''
def num_to_binary(size,x):
    ans = ""
    while(x > 0):
        y = x % 2
        x = x // 2
        ans = ans + str(y)
    while(len(ans) < size):
        ans = ans + '0'
    rev_ans = ans[::-1]
    return rev_ans

     
def generate_states(nfa_states):
    size = len(nfa_states)
    dfa_size = 2**size 
    dfa_states = []
    for i in range(dfa_size):
        binary = num_to_binary(size,i)
        new_state = []
        for i in range(len(binary)):
            if(binary[i] == '1'):
                new_state.append(nfa_states[i])
        dfa_states.append(new_state)
    #print(dfa_states)
    return dfa_states


'''test function to check generation of dfa states '''
def test_generation():
    nfa = load_input()
    dfa_states = generate_states(nfa['states'])

''' create a graph to check e closures '''
def e_closures():
    nfa = load_input()
    edges = nfa['transition_function']
    states = nfa['states']
    dictionary = {}
    for s in states:
        dictionary[s] = []
    e_graph = []
    for e in edges:
        if(e[1] == '$'):
            dictionary[e[0]].append(e[2])

    distance = {}
    for s in states:
        distance[s] = {}
        for s2 in states :
            if(s2 == s):
                distance[s][s2] = 0
            else:
                distance[s][s2] = 1000000
    for s in states:
        edge_list = dictionary[s]
        for r in edge_list:
            distance[s][r] = 1
    for i in range(len(states)):
        for j in range(len(states)):
            for k in range(len(states)):
                if(distance[states[i]][states[k]] < 1000000 and distance[states[k]][states[j]] < 1000000):
                    distance[states[i]][states[j]] = min(distance[states[i]][states[j]],distance[states[i]][states[k]] + distance[states[k]][states[j]])
    e_closures = {}
    for s in states:
        closure = []
        for d in states:
            if(distance[s][d] < 1000000):
                closure.append(d)
        e_closures[s] = closure
        
    #print(e_closures)

    return e_closures                 

    
''' creates a dictionary for help '''
def graph_creation():
    nfa = load_input()
    alphabet = nfa['letters']
    states = nfa['states']
    graph = {}
    for s in states:
        graph[s] = {}
        for inp in alphabet:
            graph[s][inp] = []
    
    transition = nfa['transition_function']
    for t in transition:
        graph[t[0]][t[1]].append(t[2])
    #print(graph)
    return graph
            

''' function to create the alphabet of dfa '''
def letters():
    nfa = load_input()
    alphabet = nfa['letters']
    new_alphabet = []
    for al in alphabet:
        if(al != '$'):
            new_alphabet.append(al)
    return new_alphabet
''' helper function to remove duplicates'''
def remove_duplicates(list1):
    res = []
    [res.append(x) for x in list1 if x not in res]
    return res

''' function to generate transition '''
def transition():
    nfa = load_input()
    dfa_alphabet = letters()
    dfa_states = generate_states(nfa['states'])
    e_closure = e_closures()
    transition_list = []
    graph = graph_creation()
    
    for state in dfa_states:
        for letter in dfa_alphabet:
            next_states = []
            for s in state:
                if(len(graph[s][letter])> 0):
                    close = []
                    for r in graph[s][letter]:
                        close = close + e_closure[r]
                    next_states = next_states + graph[s][letter] + close
            next_states = remove_duplicates(next_states)
            unit = [state,letter,next_states]
            transition_list.append(unit)
    #print(transition_list)
    return transition_list

''' create dfa dictionary'''
def dfa():
    nfa = load_input()
    dfa = {}
    e_closure = e_closures()
    dfa['states'] = generate_states(nfa['states'])
    dfa['letters'] = letters()
    dfa['transition_function'] = transition()
    dfa['start_states'] = e_closure[nfa['start_states'][0]]
    dfa['final_states'] = []
    nfa_final_states = nfa['final_states']
    for states in dfa['states']:
        ans = 0
        if(len(states) > 0):
            for s in states:
                for z in nfa_final_states:
                    if(s == z):
                        ans = 1
            if(ans == 1):           
                dfa['final_states'].append(states) 
    #print(dfa)
    return dfa

''' function to check correctness '''
def compare(dfa):
    f = open('dfa.json')
    ans = json.load(f)
    f.close()
    var = True
    for key in dfa:
        if(dfa[key] != ans[key]):
            var = False
            print(key + "WRONG")
    if(var):
        print("ANSWER CORRECT")
    else:
        print("WRONG")

''' function to print dfa optimally '''
def print_dfa(dfa):
    f = open('dfa.json')
    ans = json.load(f)
    f.close()
    print("states : ")
    for i in dfa['states'] :
        print(i)
    print("transition :") 
    for s in dfa['transition_function'] :
        print("old state : {0} , input : {1} and next state : {2}".format(s[0],s[1],s[2]))
    print("Actual transition :")
    for a in ans['transition_function'] :
        print("old state : {0}, input : {1} and next state : {2}".format(a[0],a[1],a[2]))
    print("Initial_state")
    for s in dfa['start_states']:
        print(s)
    print("final_state")
    for s in dfa['final_states']:
        print(s)

print_dfa(dfa())
compare(dfa())