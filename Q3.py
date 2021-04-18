''' code to generate regex from dfa ''' 
import json 

''' function to print dfa optimally '''
def print_dfa(dfa):
    
    print("states : ")
    for i in dfa['states'] :
        print(i)
    print("transition :") 
    for s in dfa['transition_function'] :
        print("old state : {0} , input : {1} and next state : {2}".format(s[0],s[1],s[2]))
    
    print("Initial_state")
    for s in dfa['start_states']:
        print(s)
    print("final_state")
    for s in dfa['final_states']:
        print(s)
''' loads to the dfa from file '''
def load_input():
    f = open('dfa2.json')
    dfa = json.load(f)
    f.close()
    #print_dfa(dfa)
    return dfa
''' clean the string '''
def clean(str):
    ans = ""
    for i in range(len(str) - 1):
        if((str[i] == '(' and str[i+1] == ')')):
            continue
        else:
            ans = ans + str[i]
    return ans

def convert(dfa):
    #add $ to the alphabet
    dfa['letters'].append('$')
    #add start and accept states
    dfa['states'].append('start')
    dfa['states'].append('final')
    
    #add edges from start to start_states
    for s in dfa['start_states']:
        dfa['transition_function'].append(["start","$",s])
    
    #add edges from final states to final 
    for s in dfa['final_states']:
        dfa['transition_function'].append([s,"$","final"])
    
    

    #modifying the start and final states 
    dfa['start_states'] = ["start"]
    dfa['final_states'] = ["final"]

    #print_dfa(dfa)
    
    #create graph
    #print("graph creation")
    graph = {}
    for s in dfa['states']:
        graph[s] = {}
        for r in dfa['states']:
            graph[s][r] = "%"
    for l in dfa['transition_function']:
        #print(l)
        fm = l[0]
        to = l[2]
        alphabet = l[1]
        #print(fm,to,alphabet)
        #print(graph[fm][to])
        if(graph[fm][to] == "%"):
            graph[fm][to] = alphabet
        else:
            graph[fm][to] = "(" + graph[fm][to] + "+" + alphabet + ")"
        #print("new val : {0}".format(graph[fm][to]))
    
    '''
    for s in  dfa['states']:
        for z in dfa['states']:
            print("From : {0} to {1} using {2}".format(s,z,graph[s][z]))
    print("") 
    '''    
        
    #delete states
    while(len(dfa['states']) > 2):
        for s in dfa['states']:
            #choose state to delete
            if(s != "start" and s != "final"):
                chosen_state = s
                break
        #update graph 
        for s in dfa['states']:
            for r in dfa['states']:
                if(s != chosen_state and r != chosen_state and s != "final" and r!="start") :
                    
                    #print("s : {0} and r : {1}".format(s,r))
                    temp = ""
                    z = 0
                    if(graph[s][chosen_state] != "$" and graph[s][chosen_state] != "%"):
                        temp = graph[s][chosen_state]
                    if(graph[s][chosen_state] == "%"):
                        z += 1
                    if(graph[chosen_state][r] == "%"):
                        z += 1
                    if(graph[chosen_state][chosen_state] != "$" and graph[chosen_state][chosen_state]!= "%"):
                        temp += graph[chosen_state][chosen_state] + "*"
                        
                        
                    if(graph[chosen_state][r] != "$" and graph[chosen_state][r] != "%"):
                        temp += graph[chosen_state][r]
                        
                    if(z > 0):
                        temp = "%"
                    
                    
                    if(temp != "%" and graph[s][r] != "%"):
                        graph[s][r] =  "(" + temp + "+" + graph[s][r] + ")"
                    elif(temp != "%"):
                        graph[s][r] = temp
                    elif(graph[s][r] != "%"):
                        graph[s][r] = graph[s][r]
                    #print("setting graph({0},{1}) to {2}".format(s,r,graph[s][r]))
                    #print("start,start : {0}".format(graph['start']['start']))


        #delete states
        states = []
        for s in dfa['states']: 
            if(s != chosen_state):
                states.append(s)
        dfa['states'] = states
        '''
        print("After deleting states : {0}".format(chosen_state))
        
        for s in  dfa['states']:
            for z in dfa['states']:
                if(graph[s][z] != ""):
                    print("From : {0} to {1} using {2}".format(s,z,graph[s][z]))
        print("")
        '''
        


    print(graph["start"]["final"])

convert(load_input())