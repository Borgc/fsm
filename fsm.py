import graphviz

class FiniteStateMachine:
    def __init__(self, description_file):
        self.states = []
        self.inputs = []
        self.outputs = []
        self.initial_state = None
        self.transitions = []

        self.parse_description(description_file)
        self.create_graph()

    def parse_description(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Parse header
        assert lines[0].startswith('F'), "Invalid file format"
        self.num_states = int(lines[1].split()[1])
        self.num_inputs = int(lines[2].split()[1])
        self.num_outputs = int(lines[3].split()[1])
        self.initial_state = int(lines[4].split()[1])

        # Parse transitions
        self.num_transitions = int(lines[5].split()[1])
        for i in range(6, 6 + self.num_transitions):
            line = lines[i].split()
            start_state = int(line[0])
            input_symbol = int(line[1])
            end_state = int(line[2])
            output_symbol = int(line[3])
            self.transitions.append((start_state, input_symbol, end_state, output_symbol))

    def step(self, input_symbol):
        current_state = self.initial_state
        output_symbol = None

        for transition in self.transitions:
            start_state, transition_input, end_state, transition_output = transition
            if current_state == start_state and input_symbol == transition_input:
                current_state = end_state
                output_symbol = transition_output
                break

        return current_state, output_symbol

    def create_graph(self):
        dot = graphviz.Digraph(comment='Finite State Machine')

        # Add states
        for state in range(self.num_states):
            if state == self.initial_state:
                dot.node(str(state), f"State {state}", shape='doublecircle')
            else:
                dot.node(str(state), f"State {state}", shape='circle')

        # Add transitions
        for transition in self.transitions:
            start_state, input_symbol, end_state, output_symbol = transition
            dot.edge(str(start_state), str(end_state), f"Input: {input_symbol}, Output: {output_symbol}")

        self.graph = dot

# Usage example
fsm = FiniteStateMachine('etalon.fsm')
current_state, output = fsm.step(1)
print(f"Current state: {current_state}, Output: {output}")
fsm.graph.render('fsm_diagram', format='png')