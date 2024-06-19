import graphviz
import random

class FiniteStateMachine:
    def __init__(self, description_file):
        self.states = set()
        self.inputs = set()
        self.outputs = set()
        self.initial_state = None
        self.transitions = []
        self.current_state = None
        
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
            self.inputs.add(input_symbol)
            end_state = int(line[2])
            output_symbol = int(line[3])
            self.outputs.add(output_symbol)
            self.transitions.append((start_state, input_symbol, end_state, output_symbol))

    def step(self, input_symbol):
        output_symbol = None

        for transition in self.transitions:
            start_state, transition_input, end_state, transition_output = transition
            if self.current_state == start_state and input_symbol == transition_input:
                current_state = end_state
                output_symbol = transition_output
                break

        return current_state, output_symbol
    
    def gen_random_seq(self, n):
        """Generates random input string length of n

        Args:
            n (_int_): _desireble sequence length_
        """
        seq = []
        inputs = list(self.inputs)
        for i in range(n):
            seq.append(random.choice(inputs))
        return seq
        
    def input_sequence(self, seq):
        """Feeds the sequence to the machine with step() function

        Args:
            seq (_list_): _description_
        """
        self.current_state = self.initial_state
        
        output = []
        for i in range(len(seq)):
            output.append(self.step(seq[i]))
        return output
    
    def mutate(self, mutation_type):
        """
        mutation types:
        t: Error in transition
        o: Error in output
        s: Error in extra state
        """
        if mutation_type == 't':  
            self._mutate_transition_error()
        elif mutation_type == 'o':  
            self._mutate_output_error()
        elif mutation_type == 's':  
            self._mutate_extra_state_error()
        else:
            raise ValueError("Invalid mutation type")
        
    def _mutate_transition_error(self):
        transition_index = random.randint(0, len(self.transitions) - 1)
        start_state, input_symbol, end_state, output_symbol = self.transitions[transition_index]
        new_end_state = random.randint(0, self.num_states - 1)
        while new_end_state == end_state:
            new_end_state = random.randint(0, self.num_states - 1)
        self.transitions[transition_index] = (start_state, input_symbol, new_end_state, output_symbol)

    def _mutate_output_error(self):
        transition_index = random.randint(0, len(self.transitions) - 1)
        start_state, input_symbol, end_state, output_symbol = self.transitions[transition_index]
        new_output_symbol = random.randint(0, self.num_outputs - 1)
        while new_output_symbol == output_symbol:
            new_output_symbol = random.randint(0, self.num_outputs - 1)
        self.transitions[transition_index] = (start_state, input_symbol, end_state, new_output_symbol)

    def _mutate_extra_state_error(self):
        state_index = random.randint(0, self.num_states - 1)
        new_state_index = self.num_states
        self.num_states += 1
        self.states.add(new_state_index)

        for transition in self.transitions:
            start_state, input_symbol, end_state, output_symbol = transition
            if start_state == state_index:
                self.transitions.append((new_state_index, input_symbol, end_state, output_symbol))
                self.num_transitions += 1
                
        for transition in self.transitions:
            start_state, input_symbol, end_state, output_symbol = transition
            if end_state == state_index:
                self.transitions.remove(transition)
                self.transitions.append((start_state, input_symbol, new_state_index, output_symbol))
                break
                
        

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
            dot.edge(str(start_state), str(end_state), f"In: {input_symbol}, Out: {output_symbol}")

        self.graph = dot

# Usage example
def test():
    fsm = FiniteStateMachine('etalon.fsm')


    fsm_mutated = FiniteStateMachine('etalon.fsm')
    fsm_mutated.mutate('s')

    n = 1
    out1 = fsm.input_sequence(fsm.gen_random_seq(n))
    out2 = fsm_mutated.input_sequence(fsm.gen_random_seq(n))
    if out1 != out2:
        print("Error detected")
    else:
        print("No error")

    fsm.create_graph()
    fsm.graph.render('fsm_diagram', format='png')

    fsm_mutated.create_graph()
    fsm_mutated.graph.render('fsm_mutated_diagram', format='png')

if __name__ == "__main__":
    test()