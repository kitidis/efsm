from collections import OrderedDict
import os
import sys

def read_fsm(filename):
    #fsm_type = (0 - complete deterministic FSM, 1 - complete nondeterministic FSM)
    fsm = {
        'type':              'numeric',
        'fsm_type':          '',
        'states_count':      '',
        'states':            [],
        'inputs_count':      '',
        'inputs':            [],
        'outputs_count':     '',
        'outputs':           [],
        'initial_state':     '',
        'transitions_count': '',
        'transitions':       OrderedDict()
    }


    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line

    t_id = 0
    for x in content:
        params = x.strip().split(' ')

        if params[0] == 'F':
            fsm['fsm_type'] = params[1]
        elif params[0] == 's':
            fsm['states_count'] = int(params[1])
            if len(params) > 2:
                for x in range(2, len(params)):
                   fsm['states'].append(params[x])
        elif params[0] == 'i':
            fsm['inputs_count'] = int(params[1])
            if len(params) > 2:
                for x in range(2, len(params)):
                   fsm['inputs'].append(params[x])
        elif params[0] == 'o':
            fsm['outputs_count'] = int(params[1])
            if len(params) > 2:
                for x in range(2, len(params)):
                   fsm['outputs'].append(params[x])
        elif params[0] == 'n0':
            fsm['initial_state'] = params[1]
        elif params[0] == 'p':
            fsm['transitions_count'] = int(params[1])
        elif len(params) == 4:
            if (not params[0].isdigit()) or (not params[1].isdigit()) or (not params[2].isdigit()) or (not params[3].isdigit()):
                fsm['type'] = 'literal'

            fsm['transitions'][t_id] = {
                's1':     params[0],
                'input':  params[1],
                's2':     params[2],
                'output': params[3]
            }
            t_id += 1

    return fsm

def read_input_sequece(filename):
    sequences = []

    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line

    t_id = 0
    for line in content:
        sequences.append(line.strip().split(' '))


    return sequences

def write_sequeces(filename, sequeces):
    with open(filename, 'w') as f:
        for sequece in sequeces:
            f.write(' '.join(sequece) + "\n")
    
def generate_output_sequence(fsm_path, inputs_path):
    fsm = read_fsm(fsm_path)

    sequences = read_input_sequece(inputs_path)

    states = {}

    for t_id in fsm['transitions']:
        transition = fsm['transitions'][t_id]
        
        s1 = transition['s1']
        input = transition['input']

        if s1 not in states:
            states[s1] = {}

        states[s1][input] = {
            's2':     transition['s2'],
            'output': transition['output']
        }

    ret = []

    for sequence in sequences:
        sequence_with_outputs = []
        state = fsm['initial_state']

        for input in sequence:
            if state in states:
                if input in states[state]:
                    sequence_with_outputs.append('{}/{}'.format(input, states[state][input]['output']))
                    state = states[state][input]['s2']
                else:
                    print('Transition "{}/{}" not found'.format(state, input))
            else:
                print('State "{}" not found'.format(state))

        ret.append(sequence_with_outputs)

    return ret

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Tool for generation of output symbolsfor FSM v 1.0")
        print("Usage: {} [FSM file] [Input symbols file]".format(sys.argv[0]))

    if not os.path.exists(sys.argv[1]):
        print('Input FSM not exits')
        exit(1)

    if not os.path.exists(sys.argv[2]):
        print('Input symbols file not exits')
        exit(1)

    ret = generate_output_sequence(sys.argv[1], sys.argv[2])
    write_sequeces(sys.argv[3], ret)