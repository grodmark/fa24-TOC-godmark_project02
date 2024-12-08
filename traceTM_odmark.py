import csv
import argparse
import itertools
import sys


def check_next(transitions, curr, string, pos, path, all_paths, next_state, steps, max_steps):
    if path is None:
        path = [curr]

    if all_paths is None:
        all_paths = []
    
    if max_steps > 0 and steps > max_steps:
        print("Error: Step Limit Exceeded")
        return None
    
    if int(pos) >= len(string):
        transition_found = 0
        for states in transitions:
            if '_' == states[1]:
                if states[0] == curr:
                    transition_found = 1
                    curr_path = path + [[string[:pos+1], states[2], '_']]
                    string = string[:pos+1] + states[3] + string[pos+1:]
                    if states[4] == 'R':
                        new_pos = pos + 1
                    else:
                        new_pos = pos - 1
                    curr_steps = steps + 1
                    all_paths = check_next(transitions, states[2], string, new_pos, curr_path, all_paths, None, curr_steps, max_steps)
        if not transition_found:
            all_paths.append(path)
        return all_paths
    
    s = string[pos]

    for states in transitions:
        if states[0] == curr and states[1] == s:
            curr_path = path + [[string[:pos+1], states[2], string[pos+1:]]]
            string = string[:pos] + states[3] + string[pos+1:]
            if states[4] == 'R':
                new_pos = pos + 1
            else:
                new_pos = pos - 1
            curr_steps = steps + 1
            all_paths = check_next(transitions, states[2], string, new_pos, curr_path, all_paths, None, curr_steps, max_steps)
    return all_paths

parser = argparse.ArgumentParser(description="Parse inputs to determine cases")


# Required argument: Test file name
parser.add_argument(
    'test_file', 
    type=str, 
    help="The name of the test file."
)

# Required argument: Input string
parser.add_argument(
    'input_string', 
    type=str, 
    help="The input string to process."
)

# Optional argument: Max depth
parser.add_argument(
    '--max_depth', 
    type=int, 
    default=0,  # Default value if not provided
    help="The maximum depth (optional, default is 10)."
)

# Parse the arguments
args = parser.parse_args()

# Print the parsed arguments
print(f"Test File: {args.test_file}")
print(f"Input String: {args.input_string}")
if args.max_depth > 0:
    print(f"Max Depth: {args.max_depth}")
else:
    print("Max Depth: Unlimited")

reader = []

try:
    with open(args.test_file, mode='r') as file:
        read = csv.reader(file)
        reader = list(read)
except:
    print("ERROR: File does not exist")
    sys.exit()

machine = reader[0][0]
states = reader[1]
q0 = reader[4][0]
q_acc = reader[5]
q_rej = reader[6]
transitions = list(reader[7:])

curr = q0
steps = 0

pos = 0
final = check_next(transitions, curr, args.input_string, pos, [], None, None, 0, args.max_depth)

print("Tree Depth:", max(len(path) for path in final))
print("Number of Simulations:", sum(len(path) for path in final))

for path in final:
    if path[-1][1] == q_acc[0]:
        print("String accepted in:", len(path))

for path in final:
    print(path)

