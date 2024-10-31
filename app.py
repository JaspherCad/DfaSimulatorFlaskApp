import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

from flask import Flask, render_template, request
from graphviz import Digraph

app = Flask(__name__)

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_table = transitions
        self.start_state = start_state
        self.accept_states = accept_states
    
    def simulate(self, string):
        current_state = self.start_state
        transitions = []
        for i, character in enumerate(string):
            next_state = self.transition_table.get((current_state, character))
            if next_state is None:
                return transitions, False
            transitions.append({
                'step': i + 1,
                'input': character,
                'current_state': current_state,
                'next_state': next_state,
                'is_accepting': next_state in self.accept_states
            })
            current_state = next_state
        return transitions, current_state in self.accept_states
    
    def generate_diagram(self, transitions, filename='static/dfa_diagram'):
        diagram_filenames = []
        # Initial diagram for the start state
        dot = Digraph()
        for state in self.states:
            shape = 'doublecircle' if state in self.accept_states else 'circle'
            if state == self.start_state:
                dot.node(state, state, shape=shape, style='filled', color='yellow')
            else:
                dot.node(state, state, shape=shape)
        
        dot.node('start', '', shape='none')
        dot.edge('start', self.start_state)
        
        for (state, symbol), next_state in self.transition_table.items():
            dot.edge(state, next_state, label=symbol)
        
        initial_filename = f"{filename}_step_0"
        dot.render(initial_filename, format='png', cleanup=True)
        diagram_filenames.append(initial_filename)
        print(f"Initial DFA diagram saved as {initial_filename}")

        # Diagrams for each transition
        for transition in transitions:
            dot = Digraph()
            for state in self.states:
                if state in self.accept_states:
                    shape = 'doublecircle'
                else:
                    shape = 'circle'
                if state == transition['next_state']:
                    dot.node(state, state, shape=shape, style='filled', color='yellow')
                else:
                    dot.node(state, state, shape=shape)
            
            dot.node('start', '', shape='none')
            dot.edge('start', self.start_state)
            
            for (state, symbol), next_state in self.transition_table.items():
                dot.edge(state, next_state, label=symbol)
            
            step_filename = f"{filename}_step_{transition['step']}"
            dot.render(step_filename, format='png', cleanup=True)
            diagram_filenames.append(f"dfa_diagram_step_{transition['step']}.png")
            print(f"DFA diagram step {transition['step']} saved as {step_filename}.png")
        
        return diagram_filenames

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        states = set(request.form['states'].split(','))
        alphabet = set(request.form['alphabet'].split(','))
        start_state = request.form['start_state']
        accept_states = set(request.form['accept_states'].split(','))
        transitions_raw = request.form.get('transitions[]', '').strip()
        transitions_list = transitions_raw.split('\n')
        input_string = request.form['input_string']
        
        transitions = {}
        for transition in transitions_list:
            if transition.strip():
                parts = transition.split(',')
                if len(parts) == 3:
                    current_state, symbol, next_state = [part.strip() for part in parts]
                    transitions[(current_state, symbol)] = next_state
                else:
                    raise ValueError(f"Incorrect format for transition: {transition}")
        
        dfa = DFA(states, alphabet, transitions, start_state, accept_states)
        transitions, accepted = dfa.simulate(input_string)
        diagram_filenames = dfa.generate_diagram(transitions, 'static/dfa_diagram')
        return render_template('index.html', transitions=transitions, accepted=accepted, diagram_filenames=diagram_filenames)
    
    return render_template('index.html', transitions=None, accepted=None)

if __name__ == '__main__':
    app.run(debug=True)


