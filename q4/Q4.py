''' code to minimize dfa  ''' 
import json 
import sys
''' function to print dfa optimally '''
def print_dfa(dfa):
    
    print("states : ")
    for i in dfa['states'] :
        print(i)
    print("transition :") 
    for s in dfa['transition_function'] :
        print("old state : {0} , input : {1} and next state : {2}".format(s[0],s[1],s[2]))
    print("Alphabet")
    for l in dfa['letters']:
        print(l)
    print("Initial_state")
    for s in dfa['start_states']:
        print(s)
    print("final_state")
    for s in dfa['final_states']:
        print(s)
''' loads to the dfa from file '''
def load_input(infile):
    f = open(infile)
    dfa = json.load(f)
    f.close()
    #print_dfa(dfa)
    return dfa


''' function to remove unreachable states:'''
def unreachable(dfa,graph):
    reachable = dfa['start_states']
    new_states = dfa['start_states']
    while(True):
        temp = []
        for s in new_states:
            #check if s leads to new states
            for l in dfa['letters']:
                var = graph[s][l]
                already_reachable = 0
                #check if var is already there
                for r in temp:
                    if(r == var):
                        already_reachable = 1
                        break
                if(already_reachable == 0):
                    temp.append(var)
    
        temp_new = []
        #check s is not in reachable already
        for s in temp:
            is_there = 0
            for r in reachable:
                if(s == r):
                    is_there = 1
            if(is_there == 0):
                temp_new.append(s)
        new_states = temp_new
        reachable = reachable + new_states
        if(len(new_states) == 0):
            break
    not_reachable = []
    for s in dfa['states']:
        non_reachable = 1
        for r in reachable:
            if(s == r):
                non_reachable = 0
        if(non_reachable == 1):
            not_reachable.append(s)

    #print("REACHABLE = {0}".format(reachable))
    #print("NON_REACHABLE = {0}".format(not_reachable))
    dfa['states'] = reachable
    is_reachable = {}
    for s in reachable:
        is_reachable[s] = 1
    for s in not_reachable:
        is_reachable[s] = 0
    non_delete_states = []
    for f in dfa['final_states']:
        if(is_reachable[f] == 1):
            non_delete_states.append(f)
    
    dfa['final_states'] = non_delete_states
    #print("FINAL = {0}".format(non_delete_states))
    
    #print(is_reachable)
    remaining_transition = []
    for l in dfa['transition_function']:
        if(is_reachable[l[0]] == 1 and is_reachable[l[2]] == 1):
            remaining_transition.append(l)
    #print("TRANSITION = {0}".format(remaining_transition))
    dfa['transition_function'] = remaining_transition
    #print_dfa(dfa)
    return dfa
    


        

''' minimizes the dfa using partitioning '''
def partition(dfa,outfile):
    #print("Calling Partition")
    #create graph
    graph = {}
    for s in dfa['states']:
        graph[s] = {}
        for l in dfa['letters'] :
            graph[s][l] = ""
    for l in dfa['transition_function']:
        f = l[0]
        letter = l[1]
        to = l[2]
        graph[f][letter] = to
    #print("Calling ")
    dfa = unreachable(dfa,graph)
    #print_dfa(dfa)
    #print("RETURNED")
    
    state_identity = {}
    for s in dfa['states']:
        state_identity[s] = 0
    for s in dfa['final_states']:
        state_identity[s] = 1
    size = len(dfa['states'])
    #print(state_identity)
    while(True):
        size -= 1
        #if(size < - 2):
        #   break
        isThereAnyPartition = 0
        identities = []
        temp = []
        for s in state_identity:
            temp.append(state_identity[s])
        for i in temp :
            if i not in identities:
                identities.append(i)
        #print(size)
        #print("identities : {0}".format(identities))

        #print("haha")
        val = 0
        
        new_state_identities = {}
        for s in dfa['states'] :
            new_state_identities[s] = -1
        
        #print(size)
        #print("naha")
        #print(new_state_identities)
 
        #print_dfa(dfa)
        for r in identities:
            #print("")
            #print("state identity with id {0}".format(r))
            current_state = []
            for s in dfa['states']:
                if(state_identity[s] == r):
                    current_state.append(s)
            #print("Current_State = {0}".format(current_state))
            diction = {}
            for state1 in current_state:
                diction[state1] = {}
                for state2 in current_state:
                    diction[state1][state2] = 0
            for s1 in current_state:
                for s2 in current_state:
                    
                    same_partition = 1
                    if(s1 == s2):
                        diction[s1][s2] = 1
                        diction[s2][s1] = 1
                    else:
                        #print("CHECKING WHETHER {0} and {1} are equivalent".format(s1,s2))
                        for l in dfa['letters']:
                            #print("FOR letter {0} : State : {1} to {2} and state : {3} to {4} ".format(l,s1,graph[s1][l],s2,graph[s2][l]))
                            if(state_identity[graph[s1][l]] != state_identity[graph[s2][l]]):
                                same_partition = 0
                                isThereAnyPartition = 1
                                #print("FOR letter {0} : State : {1} to {2} and state : {3} to {4} ".format(l,s1,graph[s1][l],s2,graph[s2][l]))
                        if(same_partition == 1):
                            #print("{0} and {1} are  equivalent".format(s1,s2))
                            diction[s1][s2] = 1
                            diction[s2][s1] = 1
                        else:
                            #print("{0} and {1} are not equivalent".format(s1,s2))
                            diction[s1][s2] = 0
                            diction[s2][s1] = 0
            for s3 in current_state:
                if(new_state_identities[s3] == -1):
                    new_state_identities[s3] = val
                    for rr in diction[s3]:
                        if(diction[s3][rr] == 1):
                            new_state_identities[rr] = val
                    val += 1
        for s in state_identity:
            state_identity[s] = new_state_identities[s]
        if(isThereAnyPartition == 0):
            break
    #print(state_identity)
    max_val = 0
    for r in state_identity:
        if(max_val <= state_identity[r]):
            max_val = state_identity[r]
    list_of_states = []
    reverse_hash = {}
    for z in range(max_val + 1):
        current_state = []
        for s in dfa['states']:
            if(state_identity[s] == z):
                current_state.append(s)
        list_of_states.append(current_state)
        reverse_hash[z] = current_state
    #print("LIST")
    #for r in list_of_states:
        #print(r)
    transition = []
    for r in list_of_states:
        for l in dfa['letters']:
            #print(r)
            #print(l)
            #print(graph[r[0]][l])
            #print("")
            iden = state_identity[graph[r[0]][l]]
            to = reverse_hash[iden]
            transition.append([r,l,to])
    
    temp1 = []
    for s in dfa['final_states']:
        temp1.append(state_identity[s])
    new_final = []
    for i in temp1:
        if reverse_hash[i] not in new_final:
            new_final.append(reverse_hash[i])
    temp2 = []
    new_start = []
    for s in dfa['start_states']:
        temp2.append(state_identity[s])
    for i in temp2:
        if reverse_hash[i] not in new_start:
            new_start.append(reverse_hash[i])
    #print(new_start,new_final)
    dfa['start_states'] = new_start
    dfa['final_states'] = new_final
    dfa['states'] = list_of_states
    dfa['transition_function'] = transition

#    print_dfa(dfa)
    g = open(outfile,"w")
    json.dump(dfa,g,indent=4)


partition(load_input(sys.argv[1]),sys.argv[2])
    


         


        
    
    
