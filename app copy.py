import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
import random
from flask import Flask, render_template, request, jsonify
from graphviz import Digraph
import re
app = Flask(__name__)

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_table = transitions
        self.start_state = start_state
        self.accept_states = accept_states




                    
               
    
    def simulate(self, string): #e.g 1001010
        current_state = self.start_state
        transitions = []
        for i, character in enumerate(string):
            next_state = self.transition_table.get((current_state, character)) #<K,V> ('q4', '1'): 'q3' 
            
            if next_state is None:
                return transitions, False
            transitions.append({
                'step': i + 1,
                'input': character,
                'current_state': current_state,
                'next_state': next_state,
                'is_accepting': next_state in self.accept_states
            })

            #after all, move the pointer of currentState to nextState.
            current_state = next_state
        return transitions, current_state in self.accept_states
    #current_state in self.accept_states means is it acccepted?
    






    #Function to split the transition string and include operators 
     
    def split_and_include_operators(text, operators):
        return text.split()



    def create_transition_table_from_string(input_string, initial_state='q1'):
        transitions = {}
        temp_transitions = []
        state_counter = 2  # Start from q2 for new states
        operators = ['*', '|']
        state_size = 0
        parts = DFA.split_and_include_operators(input_string, operators)
        current_state = initial_state
        last_symbol = None

        print(parts)

        for part in parts:
            if '*' in part:
                symbol = part.replace('*', '')
                transitions[(current_state, symbol)] = current_state
                print("*")

            elif '|' in part:
                symbol = part.replace('|', '')
                new_state = f'q{state_counter}'
                state_counter += 1
                # Current state goes to new state
                temp_transitions.append((current_state, symbol, new_state))
                # New state returns to itself
                temp_transitions.append((new_state, symbol, new_state))
                current_state = new_state
                print(temp_transitions)
                print("|")

            elif part.startswith('(') and part.endswith(')'):
                symbols = part.strip('()').split(',')
                new_state = f'q{state_counter}'
                state_counter += 1
                for symbol in symbols:
                    transitions[(current_state, symbol)] = new_state
                current_state = new_state
            else:  # Handle regular symbols or strings like 'abc', 'a', 'ab'
                last_symbol = part
                new_state = f'q{state_counter}'
                state_counter += 1
                transitions[(current_state, part)] = new_state
                current_state = new_state

        # Add the temporary transitions to the main transitions dictionary
        for current_state, symbol, new_state in temp_transitions:
            transitions[(current_state, symbol)] = new_state

        state_size = state_counter - 1
        return transitions




    @staticmethod
    def tuple_key_to_string_key(transitions): 
        return {str(k): v for k, v in transitions.items()}
    

    def format_transitions(transitions): 
        formatted = [] 
        for (state, char), next_state in transitions.items(): 
            formatted.append(f"{state},{char},{next_state}") 
        return "\n".join(formatted)
    

    @app.route('/design_dfa', methods=['GET']) 
    def design_dfa(): 
        input_string = request.args.get('input_string')
        transitions = DFA.create_transition_table_from_string(input_string)
        formatted_transitions = DFA.format_transitions(transitions)
        print(formatted_transitions)
        return jsonify({'transitions': formatted_transitions})


    

































    @classmethod    
    def generate_random_dfa_input(self, states_length=7, alphabet=('0', '1')):
        states = [f"q{i}" for i in range(1, states_length + 1)]
        start_state = random.choice(states)
        num_accept_states = random.randint(1, len(states))
        accept_states = random.sample(states, num_accept_states)
        transitions = {}

        for state in states:
            for symbol in alphabet:
                next_state = random.choice(states)
                transitions[(state, symbol)] = next_state

        return {
            "states": states,
            "alphabet": list(alphabet),
            "start_state": start_state,
            "accept_states": accept_states,
            "transitions": transitions
        }

              
    @app.route('/generate_random', methods=['GET'])
    def generate_random_dfa():
        size = request.args.get('size', type=int, default=4)  
        
        dfa_details = DFA.generate_random_dfa_input(states_length=size)  

        return {
            "states": ','.join(dfa_details["states"]),
            "alphabet": ','.join(dfa_details["alphabet"]),
            "start_state": dfa_details["start_state"],
            "accept_states": ','.join(dfa_details["accept_states"]),
            "transitions": "\n".join([f"{state},{symbol},{next_state}" for (state, symbol), next_state in dfa_details["transitions"].items()])
        }












    def generate_diagram(self, transitions, filename='static/dfa_diagram'):
        
        diagram_filenames = [] #basically get image here to html ;)



        # Initial diagram for the !FOREGROUND (for presentation, u know it. this is the background for html that keep the animation smoooooooooooooooth)
        dot = Digraph()

        for state in self.states: #draw all states
            shape = 'doublecircle' if state in self.accept_states else 'circle'
            dot.node(state, state, shape=shape)
        
        dot.node('start', '', shape='none')
        dot.edge('start', self.start_state, label="start")
        
        for (state, symbol), next_state in self.transition_table.items(): #draw all transition
            dot.edge(state, next_state, label=symbol)
        
        initial_filename = f"{filename}_step_0"
        dot.render(initial_filename, format='png', cleanup=True)
        diagram_filenames.append(f"dfa_diagram_step_0.png")
        print(f"bg DFA diagram saved as {initial_filename}")



        # Initial diagram for the start state
        dot = Digraph()

        for state in self.states: #draw all states
            shape = 'doublecircle' if state in self.accept_states else 'circle'
            if state == self.start_state:
                dot.node(state, state, shape=shape, style='filled', color='lightblue')
            else:
                dot.node(state, state, shape=shape)
        
        dot.node('start', '', shape='none')
        dot.edge('start', self.start_state, label="start", color='blue', penwidth='4.0')
        
        for (state, symbol), next_state in self.transition_table.items(): #draw all transition
            dot.edge(state, next_state, label=symbol)
        
        initial_filename = f"{filename}_step_1"
        dot.render(initial_filename, format='png', cleanup=True)
        diagram_filenames.append(f"dfa_diagram_step_1.png")
        print(f"Initial DFA diagram saved as {initial_filename}")


        






        # Diagrams for each transition
        for transition in transitions:
            dot = Digraph()
            for state in self.states: #draw states
                shape = 'doublecircle' if state in self.accept_states else 'circle'
                color = 'green' if state in self.accept_states else 'red'


                if state == transition['next_state']:
                    # print(transition['step'])
                    # print("over")
                    # print(len(transitions))
                    if transition['step'] == len(transitions): #last step
                        if state in self.accept_states:
                            dot.node(state, state, shape=shape, style='filled', color='green')
                        else: #end state but not accepting
                            dot.node(state, state, shape=shape, style='filled', color='red')

                    
                    else: #not accepting still next state
                        dot.node(state, state, shape=shape, style='filled', color=color, fillcolor='lightblue')

                elif state == transition['current_state']:  # prev state
                    dot.node(state, state, shape=shape, color='blue')

                else: # Default rendering for other states
                    dot.node(state, state, shape=shape)
            
            #drawing statr states
            dot.node('start', '', shape='none')
            dot.edge('start', self.start_state, label="start")

            
            #all transitions ps: state == currentState
            #     ('q4', '1'):     'q3' 
            for (state, symbol), next_state in self.transition_table.items():
                if state == transition['current_state'] and next_state == transition['next_state']:
                    dot.edge(state, next_state, label=symbol, color='blue', penwidth='2.0')
                else:
                    dot.edge(state, next_state, label=symbol)

            step = int(transition['step']) + 1
            step_filename = f"{filename}_step_{step}"
            dot.render(step_filename, format='png', cleanup=True)
            diagram_filenames.append(f"dfa_diagram_step_{step}.png")
            print(f"DFA diagram step {transition['step']} saved as {step_filename}.png also {step}")
        
        return diagram_filenames

@app.route('/') 
def home(): 
    return render_template('homepage.html')

@app.route('/dfa', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        states = set([state.strip() for state in request.form['states'].split(',')])
        alphabet = set([alphabet.strip() for alphabet in request.form['alphabet'].split(',')])
        start_state = request.form['start_state'].strip()
        accept_states = set([accpept.strip() for accpept in request.form['accept_states'].split(',')])
        transitions_raw = request.form.get('transitions[]', '').strip()
        # "q1,0,q2\nq1,1,q4\nq2,0,q3\nq2,1,q2\nq3,0,q3\nq3,1,q3\nq4,0,q4\nq4,1,q3"



        transitions_list = transitions_raw.split('\n')


        input_string = request.form['input_string']
        
        transitions = {}

#GInawang key value here <(current a, alphabet b), next state>
        for transition in transitions_list:
            if transition.strip():
                parts = transition.split(',')
                # "q4,0,q4", 
                if len(parts) == 3:
                    current_state, symbol, next_state = [part.strip() for part in parts]
                    transitions[(current_state, symbol)] = next_state

               
                else:
                    raise ValueError(f"Incorrect format for transition: {transition}")
        
        dfa = DFA(states, alphabet, transitions, start_state, accept_states)
        
        transitions, accepted = dfa.simulate(input_string) #returns transitions and current state, so set them in transitions, isAccepted

        diagram_filenames = dfa.generate_diagram(transitions, 'static/dfa_diagram')
        return render_template('index.html', transitions=transitions, accepted=accepted, diagram_filenames=diagram_filenames)
        
    return render_template('index.html', transitions=None, accepted=None)

if __name__ == '__main__':
    app.run(debug=True)


