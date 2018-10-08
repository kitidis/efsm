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

def is_deterministic(path):
    errors = []

    fsm = read_fsm(path)

    states_inputs = {}

    for t_id in fsm['transitions']:
        transition = fsm['transitions'][t_id]

        id = '{} / {}'.format(transition['s1'], transition['input'])

        if id in states_inputs:
            states_inputs[id] += 1
        else:
            states_inputs[id] = 1
       
    for id in states_inputs:
        if states_inputs[id] > 1:
            errors.append(id)

    if len(errors):
        return False, '\n'.join(errors)

    return True, None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Tool for check deterministic of FSM v 1.0")
        print("Usage: {} [FSM file]".format(sys.argv[0]))

    if not os.path.exists(sys.argv[1]):
        print('Input FSM not exits')
        exit(1)

    ret, errors = is_deterministic(sys.argv[1])
    if ret:
        print('FSM deterministic')
    else:
        print('FSM not deterministic')
        print('Not deterministic transitions (State / Input):\n' + errors)