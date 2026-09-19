def dfa_no_1(input_string):
    # State representation
    current_state = "q0"
    
    # Transition function table for minimized DFA
    transitions = {
        "q0":   {'0': "q0",   '1': "q1q3"},
        "q1q3": {'0': "q2q4", '1': "q1q3"},
        "q2q4": {'0': "q0",   '1': "q1q3"}
    }
    
    final_states = {"q2q4"}

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
accepted_test = ["10", "010", "110", "0110"]
rejected_test = ["0", "1", "00", "101"]

print("--- DFA No. 1 Test Results ---")
for s in accepted_test + rejected_test:
    print(dfa_no_1(s))