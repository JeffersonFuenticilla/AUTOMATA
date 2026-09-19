class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions  # dict: {state: {symbol: next_state}}
        self.start_state = start_state
        self.accept_states = set(accept_states)

    def process_string(self, input_string):
        """Simulates the DFA on an input string."""
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, f"Invalid symbol '{symbol}'"
            current_state = self.transitions[current_state][symbol]
        return current_state in self.accept_states, current_state

    def minimize(self):
        """Minimizes the DFA using the Equivalence Partitioning algorithm."""
        # 1. Initial Partition P0: [Accepting states, Non-accepting states]
        non_accept = self.states - self.accept_states
        partitions = []
        if non_accept:
            partitions.append(non_accept)
        if self.accept_states:
            partitions.append(self.accept_states)

        def get_partition_index(state, current_partitions):
            for idx, group in enumerate(current_partitions):
                if state in group:
                    return idx
            return -1

        # 2. Refine Partitions iteratively
        while True:
            new_partitions = []
            for group in partitions:
                if len(group) <= 1:
                    new_partitions.append(group)
                    continue

                # Group states by their transition destination partition signature
                signature_map = {}
                for state in group:
                    signature = tuple(
                        get_partition_index(self.transitions[state][char], partitions)
                        for char in sorted(self.alphabet)
                    )
                    signature_map.setdefault(signature, set()).add(state)

                new_partitions.extend(signature_map.values())

            if len(new_partitions) == len(partitions):
                break
            partitions = new_partitions

        # 3. Construct Minimized DFA
        state_map = {}
        min_states = []
        min_accept_states = set()
        min_start_state = None

        for group in partitions:
            # Name the group state by joining state names sorted
            group_name = "".join(sorted(list(group)))
            min_states.append(group_name)

            for state in group:
                state_map[state] = group_name

            if self.start_state in group:
                min_start_state = group_name

            if any(s in self.accept_states for s in group):
                min_accept_states.add(group_name)

        min_transitions = {}
        for group in partitions:
            group_name = "".join(sorted(list(group)))
            representative = next(iter(group))
            min_transitions[group_name] = {}
            for char in sorted(self.alphabet):
                dest = self.transitions[representative][char]
                min_transitions[group_name][char] = state_map[dest]

        return DFA(
            states=min_states,
            alphabet=self.alphabet,
            transitions=min_transitions,
            start_state=min_start_state,
            accept_states=min_accept_states
        )


# =====================================================================
# RUNNING ALL 4 EXAMPLES
# =====================================================================

def run_examples():
    print("=" * 60)
    print("EXAMPLE 1: Board Example 1")
    print("=" * 60)
    dfa1 = DFA(
        states={'A', 'B', 'C', 'D', 'E'},
        alphabet={'0', '1'},
        transitions={
            'A': {'0': 'B', '1': 'C'},
            'B': {'0': 'B', '1': 'D'},
            'C': {'0': 'A', '1': 'C'},
            'D': {'0': 'B', '1': 'C'},
            'E': {'0': 'B', '1': 'C'},
        },
        start_state='A',
        accept_states={'E'}
    )
    min_dfa1 = dfa1.minimize()
    print("Minimized States:", min_dfa1.states)
    print("Minimized Transitions:", min_dfa1.transitions)
    
    test_inputs_1 = ["0110", "01101", "011011"]
    for inp in test_inputs_1:
        acc, end_st = min_dfa1.process_string(inp)
        print(f"Input: '{inp}' -> Accepted: {acc} (Ended at: {end_st})")

    print("\n" + "=" * 60)
    print("EXAMPLE 2: Board Example 2")
    print("=" * 60)
    dfa2 = DFA(
        states={'A', 'B', 'C', 'D', 'E', 'F'},
        alphabet={'0', '1'},
        transitions={
            'A': {'0': 'B', '1': 'C'},
            'B': {'0': 'A', '1': 'D'},
            'C': {'0': 'E', '1': 'F'},
            'D': {'0': 'E', '1': 'F'},
            'E': {'0': 'E', '1': 'F'},
            'F': {'0': 'F', '1': 'F'},
        },
        start_state='A',
        accept_states={'C', 'D', 'E'}
    )
    min_dfa2 = dfa2.minimize()
    print("Minimized States:", min_dfa2.states)
    print("Minimized Transitions:", min_dfa2.transitions)
    
    test_inputs_2 = ["1", "010", "101", "1000"]
    for inp in test_inputs_2:
        acc, end_st = min_dfa2.process_string(inp)
        print(f"Input: '{inp}' -> Accepted: {acc} (Ended at: {end_st})")

    print("\n" + "=" * 60)
    print("EXAMPLE 3: DFA Accepting Strings Ending in '10'")
    print("=" * 60)
    dfa3 = DFA(
        states={'q0', 'q1', 'q2', 'q3', 'q4'},
        alphabet={'0', '1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q2', '1': 'q3'},
            'q2': {'0': 'q0', '1': 'q1'},
            'q3': {'0': 'q4', '1': 'q3'},
            'q4': {'0': 'q0', '1': 'q1'},
        },
        start_state='q0',
        accept_states={'q2', 'q4'}
    )
    min_dfa3 = dfa3.minimize()
    print("Minimized States:", min_dfa3.states)
    print("Minimized Transitions:", min_dfa3.transitions)
    
    test_inputs_3 = ["10", "0110", "101", "000"]
    for inp in test_inputs_3:
        acc, end_st = min_dfa3.process_string(inp)
        print(f"Input: '{inp}' -> Accepted: {acc} (Ended at: {end_st})")

    print("\n" + "=" * 60)
    print("EXAMPLE 4: Alternate State Partitioning")
    print("=" * 60)
    dfa4 = DFA(
        states={'A', 'B', 'C', 'D', 'E', 'F'},
        alphabet={'0', '1'},
        transitions={
            'A': {'0': 'B', '1': 'C'},
            'B': {'0': 'A', '1': 'D'},
            'C': {'0': 'D', '1': 'A'},
            'D': {'0': 'C', '1': 'B'},
            'E': {'0': 'F', '1': 'C'},
            'F': {'0': 'E', '1': 'D'},
        },
        start_state='A',
        accept_states={'A', 'F'}
    )
    min_dfa4 = dfa4.minimize()
    print("Minimized States:", min_dfa4.states)
    print("Minimized Transitions:", min_dfa4.transitions)
    
    test_inputs_4 = ["00", "11", "01", "1010"]
    for inp in test_inputs_4:
        acc, end_st = min_dfa4.process_string(inp)
        print(f"Input: '{inp}' -> Accepted: {acc} (Ended at: {end_st})")


if __name__ == "__main__":
    run_examples()