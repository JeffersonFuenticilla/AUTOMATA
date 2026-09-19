class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states)

    def process_string(self, input_string):
        """Sine-test ang input string kung tatanggapin o titanggihan ng DFA."""
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, f"Invalid symbol '{symbol}'"
            current_state = self.transitions[current_state][symbol]
        return current_state in self.accept_states, current_state

    def minimize(self):
        """Ginagamit ang Equivalence Partitioning Algorithm para i-minimize ang DFA."""
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

        while True:
            new_partitions = []
            for group in partitions:
                if len(group) <= 1:
                    new_partitions.append(group)
                    continue

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

        state_map = {}
        min_states = []
        min_accept_states = set()
        min_start_state = None

        for group in partitions:
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
# PAG-RUN NG APAT (4) NA HALIMBAWA
# =====================================================================

def main():
    print("=" * 60)
    print("HALIMBAWA 1: Board Example 1")
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
    
    for inp in ["0110", "01101", "011011"]:
        acc, end_st = min_dfa1.process_string(inp)
        print(f"Input: '{inp}' -> Accepted: {acc} (Ended at state: {end_st})")

    print("\n" + "=" * 60)
    print("HALIMBAWA 2: Board Example 2")
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
    
    for inp in ["1", "010", "101", "1000"]:
        acc, end_st = min_dfa2.process_string(inp)
        print(f"Input: '{inp}' -> Accepted: {acc} (Ended at state: {end_st})")

    print("\n" + "=" * 60)
    print("HALIMBAWA 3: Strings Ending in '10'")
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
    
    for inp in ["10", "0110", "101", "000"]:
        acc, end_st = min_dfa3.process_string(inp)
        print(f"Input: '{inp}' -> Accepted: {acc} (Ended at state: {end_st})")

    print("\n" + "=" * 60)
    print("HALIMBAWA 4: Minimized Partition Verification")
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
    
    for inp in ["00", "11", "01", "1010"]:
        acc, end_st = min_dfa4.process_string(inp)
        print(f"Input: '{inp}' -> Accepted: {acc} (Ended at state: {end_st})")


if __name__ == "__main__":
    main()