'''This is python code to transform regex to NFA '''
''' The regex can have alphabets ,() and * , + ''' 
''' + denotes union and * denotes Kleene Star'''
''' Alphabet is common : {0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}'''
''' first create the NFA graph and then convert it into appropriate dictionary '''
''' graph is a list of [from,edge-char,to] '''

global_counter = 0
import string
import sys
import json

''' class to denote nfa '''
class nfa :
    def __init__(self,start,size):
        self.start_state = start
        self.final_state = start + size - 1
        self.transition_list = []


''' formats the input regex to add a char ? to denote concatenation.This helps in parsing '''
def format_regular_expression(str):
    regex = ""
    regex = regex + str[0]
    regex_size = 1
    for i in range(len(str)):
        if(i > 0):
            
            if(str[i] != '+' and str[i] != '*' and str[i] != ')'):
        
                if(regex[regex_size - 1] != '+'  and regex[regex_size - 1] != '?' and regex[regex_size - 1] != '('):
                    regex = regex + "?" + str[i]
                    regex_size += 2
                else:
                    regex = regex + str[i]
                    regex_size += 1
            else:
                regex = regex + str[i]
                regex_size += 1
    return regex

''' function to test formating of the string '''
def test_formatin():
    str = "a*ba+a(ab)a"
    print(format_regular_expression(str))


''' returns a postfix expression  from infix using shunting yard '''
def shunting_yard(infix):
    stack = [] 
    output = ""
    
    for ex in infix:
        #print(infix)
        #print(ex)
        if(ex.isalnum()):
            output = output + ex
        elif(ex == '('):
            stack.append(ex)
        elif(ex == ')'):
            while(1):
                u = stack.pop()
                if(u == '('):
                    break
                else:
                    output = output + u
        elif(ex == '*'):
            while(1):
                if(len(stack) == 0):
                    stack.append('*')
                    break
                u = stack[-1]
                if(u == '('):
                    stack.append(ex)
                    break
                elif(u == '*'):
                    r = stack.pop()
                    output = output + r
                    
                    
                elif(u == '?' or u == '+'):
                    stack.append(ex)
                    break
        elif(ex == '?'):
            while(1):
                if(len(stack) == 0):
                    stack.append(ex)
                    break
                u = stack[-1]
                if(u == '('):
                    stack.append(ex)
                    break
                elif(u == '*' or u == '?'):
                    k = stack.pop()
                    output = output + k
                elif(u == '+'):
                    stack.append(ex)
                    break
        elif(ex == '+'):
            while(1):
                if(len(stack) == 0):
                    stack.append(ex)
                    break
                u = stack[-1]
                if(u == '('):
                    stack.append(ex)
                    break
                elif(u == '+' or u == '?' or u == '*'):
                    z = stack.pop()
                    output = output + z
      #  print("output : {0} and stack : {1}".format(output, stack))
        
    while(len(stack) != 0):
        z = stack.pop()
        if(z != '(' or z != ')'):
            output = output + z

    return output


''' functionn to test shunting_yard '''
def test_shunting_yard():
    str = "a(a+b)*b"
    print(shunting_yard(format_regular_expression(str)))

''' construct a empty nfa,equivalent to rule 1 of thompson '''
def construct_empty_nfa():
    global global_counter
    new_nfa = nfa(global_counter,2)
    global_counter += 2
    new_nfa.transition_list.append([new_nfa.start_state,"$",new_nfa.final_state])
    return new_nfa

''' construct a one symbol nfa,equivalent to rule 2 of thompson '''
def construct_symbol_nfa(a):
    #print("construct {0}".format(a))
    global global_counter
    new_nfa = nfa(global_counter,2)
    global_counter += 2
    new_nfa.transition_list.append([new_nfa.start_state,a,new_nfa.final_state])
    #print("CREATED NFA:")
    #print_nfa(new_nfa)
    return new_nfa

''' construct a union of 2 nfa ,equivalent to rule 3 of thompson '''
def union_nfa(nfa1,nfa2):
    #print("union")
    global global_counter
    new_nfa = nfa(global_counter,2)
    global_counter += 2
    for r in nfa1.transition_list:
        new_nfa.transition_list.append(r)
    for r in nfa2.transition_list:
        new_nfa.transition_list.append(r)
    new_nfa.transition_list.append([new_nfa.start_state,"$",nfa1.start_state])
    new_nfa.transition_list.append([new_nfa.start_state,"$",nfa2.start_state])
    new_nfa.transition_list.append([nfa1.final_state,"$",new_nfa.final_state])
    new_nfa.transition_list.append([nfa2.final_state,"$",new_nfa.final_state])
    #print("CREATED NFA:")
    #print_nfa(new_nfa)
    return new_nfa

''' construct a concatenation of 2 nfa,equivalent to rule 4 of thompson '''
def concatenate_nfa(nfa1,nfa2):
    
    #print("concatenate")
    for z in nfa2.transition_list:
        if(z[0] == nfa2.start_state):
            z[0] = nfa1.final_state
        nfa1.transition_list.append(z)
   
    nfa1.final_state = nfa2.final_state
    #print("CREATED NFA:")
    #print_nfa(nfa1)
    return nfa1

''' star operation on a nfa,equivalent to rule 5 of thompson '''
def star_nfa(nfa1):
    #print("star")
    global global_counter
    new_nfa = nfa(global_counter,2)
    global_counter += 2
    for z in nfa1.transition_list:
        new_nfa.transition_list.append(z)
    new_nfa.transition_list.append([new_nfa.start_state,"$",nfa1.start_state])
    new_nfa.transition_list.append([nfa1.final_state,"$",new_nfa.final_state])
    new_nfa.transition_list.append([nfa1.final_state,"$",nfa1.start_state])
    new_nfa.transition_list.append([new_nfa.start_state,"$",new_nfa.final_state])
    #print("CREATED NFA:")
    #print_nfa(new_nfa)
    return new_nfa
    


''' create a nfa given a postfix regex '''
def create_nfa(postfix):
    #print(postfix)
    stack = []
    for char in postfix:
        #print(char)
        if(char.isalnum()):
            stack.append(construct_symbol_nfa(char))
        elif(char == "$"):
            stack.append(construct_empty_nfa())
        elif(char == '*'):
            nfa1 = stack.pop()
            stack.append(star_nfa(nfa1))
        elif(char == '+'):
            nfa1 = stack.pop()
            nfa2 = stack.pop()
            stack.append(union_nfa(nfa2,nfa1))
        elif(char == '?'):
            nfa1 = stack.pop()
            nfa2 = stack.pop()
            stack.append(concatenate_nfa(nfa2,nfa1))
        '''for nfas in stack : 
            print_nfa(nfas)'''
    final_nfa = stack.pop()
    return final_nfa

''' function to print a nfa '''
def print_nfa(nfa):
    print("start_state : {0}".format(nfa.start_state))
    print("final_state : {0}".format(nfa.final_state))
    for edges in nfa.transition_list:
        print("From : {0} ,to : {1} using : {2}".format(edges[0],edges[2],edges[1]))
''' function to generate the nfa '''
def generate_nfa(nfa,alpha):
    final_nfa = {}
    hash_num = {}
    temp = []
    for l in nfa.transition_list:
        temp.append(l[0])
        temp.append(l[2])
    state_index = []
    for s in temp:
        if s not in state_index:
            state_index.append(s)
    cnt = 0
    states = []
    for r in state_index:
        hash_num[r] = "Q" + str(cnt)
        cnt += 1
        states.append(hash_num[r])
    final_nfa['states'] = states
    start_state = [hash_num[nfa.start_state]]
    final_state = [hash_num[nfa.final_state]]
    letters = list(string.ascii_lowercase)
    num = []
    for i in range(10):
        num.append(str(i))
    alphabet = letters + num + ["$"]
    transition = []
    for i in nfa.transition_list:
        l1 = hash_num[i[0]]
        l2 = hash_num[i[2]] 
        char = i[1]
        transition.append([l1,char,l2])

    final_nfa['letters'] = alpha
    final_nfa['transition_function'] = transition
    final_nfa['start_states'] = start_state
    final_nfa['final_states'] = final_state
    return final_nfa
    
        



''' function to test create_nfa''' 
def test_nfa_creation(inp_file,out_file):
    #str = "a(a+b)*b"
    f = open(inp_file)
    regex = json.load(f)
    f.close()
    g = open(out_file,"w")

    str = regex['regex']
    alphabet = []
    temp = []
    for l in str:
        if(l.isalnum()):
            temp.append(l)
    for s in temp:
        if s not in alphabet:
            alphabet.append(s)
    json.dump(generate_nfa(create_nfa(shunting_yard(format_regular_expression(str))),alphabet),g,indent=6)
    g.close()



input_path = sys.argv[1]
output_path = sys.argv[2]
test_nfa_creation(input_path,output_path)  
           
