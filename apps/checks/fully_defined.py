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

def write_fsm(fsm, filename):
    text = "F {}\n".format(fsm['fsm_type'])
    text += "s {}{}\n".format(fsm['states_count'], (' ' + ' '.join(str(v) for x,v in fsm['states'].items()) if len(fsm['states']) > 0 else ''))
    text += "i {}{}\n".format(fsm['inputs_count'], (' ' + ' '.join(str(v) for x,v in fsm['inputs'].items()) if len(fsm['inputs']) > 0 else ''))
    text += "o {}{}\n".format(fsm['outputs_count'], (' ' + ' '.join(str(v) for x,v in fsm['outputs'].items()) if len(fsm['outputs']) > 0 else ''))
    text += "n0 {}\n".format(fsm['initial_state'])
    text += "p {}\n".format(fsm['transitions_count'])

    for t_id in fsm['transitions']:
        transition = fsm['transitions'][t_id]
        text += "{} {} {} {}\n".format(transition['s1'], transition['input'], transition['s2'], transition['output'])

    with open(filename, 'w') as f:
        f.write(text)

def is_fully_defined(path, fixed_fsm_path = None):
    errors = []

    fsm = read_fsm(path)

    states_inputs = {}

    missed_transitions = []
    new_output_symbol = fsm['outputs_count']

    for t_id in fsm['transitions']:
        transition = fsm['transitions'][t_id]

        id = '{} / {}'.format(transition['s1'], transition['input'])

        if id in states_inputs:
            states_inputs[id] += 1
        else:
            states_inputs[id] = 1
       
    if len(states_inputs) < fsm['states_count'] * fsm['inputs_count']:
        for state in range(0, fsm['states_count']):
            for input in range(0, fsm['inputs_count']):
                id = '{} / {}'.format(state, input)
                if id not in states_inputs:
                    errors.append(id)
                    missed_transitions.append({
                        's1':     state,
                        'input':  input,
                        's2':     state,
                        'output': new_output_symbol
                    })

    if fixed_fsm_path is not None:
        fsm['outputs_count'] += 1
        for transition in missed_transitions:
            fsm['transitions'][len(fsm['transitions'])] = transition

        fsm['transitions_count'] += len(missed_transitions)

        write_fsm(fsm, fixed_fsm_path)
        return True, None

    if len(errors):
        return False, '\n'.join(errors)

    return True, None

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Tool for check fully definition of FSM v 1.0")
        print("Usage: {} [FSM file] <fixed FSM file>".format(sys.argv[0]))

    if not os.path.exists(sys.argv[1]):
        print('Input FSM not exits')
        exit(1)

    fixed_fsm_path = None
    if len(sys.argv) == 3:
        fixed_fsm_path = sys.argv[2]

    ret, errors = is_fully_defined(sys.argv[1], fixed_fsm_path)
    if ret:
        print('FSM fully defined')
    else:
        print('FSM not fully defined')
        print('Not defined transitions (State / Input):\n' + errors)