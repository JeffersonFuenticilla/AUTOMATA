def dfa_no_2(input_string):
    # State representation
    current_state = "A"
    
    # Transition function table for minimized DFA
    transitions = {
        "A":   {'0': "B",   '1': "C_D"},
        "B":   {'0': "A",   '1': "C_D"},
        "C_D": {'0': "E",   '1': "C_D"},
        "E":   {'0': "E",   '1': "E"}
    }
    
    final_states = {"C_D"}

    # Process each symbol in the input string
    for char in input_string:
        if char not in ('0', '1'):
            return f"Invalid character '{char}' in input."
        current_state = transitions[current_state][char]

    # Check acceptance
    if current_state in final_states:
        return f"Input: '{input_string}' -> ACCEPTED (Ended in {current_state})"
    else:
        return f"Input: '{input_string}' -> REJECTED (Ended in {current_state})"


# Test cases from your activity document
accepted_test = ["1", "01", "001", "11"]
rejected_test = ["0", "010", "00", "10"]

print("--- DFA No. 2 Test Results ---")
for s in accepted_test + rejected_test:
    print(dfa_no_2(s))