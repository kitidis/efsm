from collections import OrderedDict
import argparse
import os

# read fsm
def read_fsm(filename):
    #fsm_type = (0 - complete deterministic FSM, 1 - complete nondeterministic FSM)
    fsm = {
        'type':              'numeric',
        'fsm_type':          None,
        'states_count':      None,
        'states':            [],
        'inputs_count':      None,
        'inputs':            [],
        'outputs_count':     None,
        'outputs':           [],
        'initial_state':     None,
        'transitions_count': None,
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

# write fsm

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

    print(text)
    with open(filename, 'w') as f:
        f.write(text)

# read description
def read_description(filename):
    #fsm_type = (0 - complete deterministic FSM, 1 - complete nondeterministic FSM)
    description = {
        'states':  OrderedDict(),
        'inputs':  OrderedDict(),
        'outputs': OrderedDict()
    }


    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line

    for x in content:
        params = x.strip().split(' ')

        if params[0] == 's':
            description['states'][params[2]] = int(params[1])
        elif params[0] == 'i':
            description['inputs'][params[2]] = int(params[1])
        elif params[0] == 'o':
            description['outputs'][params[2]] = int(params[1])

    return description

# write description
def write_description(description, filename):
    text = ''
    for k,v in description['states'].items():
        text += "s {} {}\n".format(v, k)

    for k,v in description['inputs'].items():
        text += "i {} {}\n".format(v, k)

    for k,v in description['outputs'].items():
        text += "o {} {}\n".format(v, k)

    print(text)
    with open(filename, 'w') as f:
        f.write(text)

def validate_fsm(fsm):
    errors = []

    if fsm['states_count'] is None:
        errors.append('Undefined number of states')

    if fsm['inputs_count'] is None:
        errors.append('Undefined number of inputs')

    if fsm['outputs_count'] is None:
        errors.append('Undefined number of outputs')

    if fsm['transitions_count'] is None:
        errors.append('Undefined number of transitions')

    if fsm['initial_state'] is None:
        errors.append('Initial state not defined')

    # states
    if len(fsm['states']) > 0:
        if len(fsm['states']) != fsm['states_count']:
            errors.append('Wrong number of states {}/{}'.format(len(fsm['states']), fsm['states_count']))

    # inputs
    if len(fsm['inputs']) > 0:
        if len(fsm['inputs']) != fsm['inputs_count']:
            errors.append('Wrong number of inputs {}/{}'.format(len(fsm['inputs']), fsm['inputs_count']))

    # outputs
    if len(fsm['outputs']) > 0:
        if len(fsm['outputs']) != fsm['outputs_count']:
            errors.append('Wrong number of outputs {}/{}'.format(len(fsm['outputs']), fsm['outputs_count']))

    # transitions
    if len(fsm['transitions']) != fsm['transitions_count']:
        errors.append('Wrong number of transitions {}/{}'.format(len(fsm['transitions']), fsm['transitions_count']))

    # validate transitions
    for t_id in fsm['transitions']:
        transition = fsm['transitions'][t_id]

        s1 = transition['s1']
        input = transition['input']
        s2 = transition['s2']
        output = transition['output']

        if len(fsm['states']) > 0:
            if s1 not in fsm['states']:
                errors.append('Transition {}, state {} not in states list'.format(t_id+1, s1))
        else:
            if int(s1) >= fsm['states_count']:
                errors.append('Transition {}, state {} higher than number of states {}'.format(t_id, s1, fsm['states_count']))

        if len(fsm['states']) > 0:
            if s2 not in fsm['states']:
                errors.append('Transition {}, state {} not in states list'.format(t_id, s2))
        else:
            if int(s2) >= fsm['states_count']:
                errors.append('Transition {}, state {} higher than number of states {}'.format(t_id, s2, fsm['states_count']))

        if len(fsm['inputs']) > 0:
            if input not in fsm['inputs']:
                errors.append('Transition {}, input {} not in inputs list'.format(t_id, input))
        else:
            if int(input) >= fsm['inputs_count']:
                errors.append('Transition {}, input {} higher than number of inputs {}'.format(t_id, input, fsm['inputs_count']))

        if len(fsm['outputs']) > 0:
            if output not in fsm['outputs']:
                errors.append('Transition {}, output {} not in outputs list'.format(t_id, output))
        else:
            if int(output) >= fsm['outputs_count']:
                errors.append('Transition {}, output {} higher than number of outputs {}'.format(t_id, output, fsm['outputs_count']))

        t_id += 1

    if len(fsm['states'])> 0 and fsm['initial_state'] is not None:
        if fsm['initial_state'] not in fsm['states']:
                errors.append('Initial state {} not in states list'.format(fsm['initial_state']))

    return errors

def sort_transitions(fsm):
    fsm['transitions'] = OrderedDict(sorted(fsm['transitions'].items(), key=lambda x: int(x[1]['s1']) * fsm['states_count'] + int(x[1]['input'])))

    return fsm

def convert_to_numeric_representation(fsm):
    new_fsm = {
        'type':              'literal',
        'fsm_type':          fsm['fsm_type'],
        'states_count':      fsm['states_count'],
        'states':            {},
        'inputs_count':      fsm['inputs_count'],
        'inputs':            {},
        'outputs_count':     fsm['outputs_count'],
        'outputs':           {},
        'initial_state':     '',
        'transitions_count': fsm['transitions_count'],
        'transitions':       OrderedDict()
    }

    states  = OrderedDict()
    inputs  = OrderedDict()
    outputs = OrderedDict()


    states[fsm['initial_state']] = 0
    new_fsm['initial_state'] = 0

    new_transitions = OrderedDict()
    for t_id in fsm['transitions']:
        transition = fsm['transitions'][t_id]

        s1 = transition['s1']
        input = transition['input']
        s2 = transition['s2']
        output = transition['output']

        if s1 in states:
            s1 = states[s1]
        else:
            states[s1] = len(states)
            s1 = len(states) - 1

        if s2 in states:
            s2 = states[s2]
        else:
            states[s2] = len(states)
            s2 = len(states) - 1

        if input in inputs:
            input = inputs[input]
        else:
            inputs[input] = len(inputs)
            input = len(inputs) - 1

        if output in outputs:
            output = outputs[output]
        else:
            outputs[output] = len(outputs)
            output = len(outputs) - 1

        new_fsm['transitions'][t_id] = {
            's1':     s1,
            'input':  input,
            's2':     s2,
            'output': output
        }

    description = {
        'states':  states,
        'inputs':  inputs,
        'outputs': outputs
    }

    # sort transitions by state/input
    new_fsm = sort_transitions(new_fsm)

    return new_fsm, description

def convert_to_literal_representation(fsm, description):
    new_fsm = {
        'type':              'literal',
        'fsm_type':          fsm['fsm_type'],
        'states_count':      fsm['states_count'],
        'states':            {},
        'inputs_count':      fsm['inputs_count'],
        'inputs':            {},
        'outputs_count':     fsm['outputs_count'],
        'outputs':           {},
        'initial_state':     '',
        'transitions_count': fsm['transitions_count'],
        'transitions':       OrderedDict()
    }

    states  = OrderedDict()
    inputs  = OrderedDict()
    outputs = OrderedDict()

    for k,v in description['states'].items():
        states[v] = k
        new_fsm['states'][v] = k

    for k,v in description['inputs'].items():
        inputs[v] = k
        new_fsm['inputs'][v] = k

    for k,v in description['outputs'].items():
        outputs[v] = k
        new_fsm['outputs'][v] = k

    new_transitions = OrderedDict()
    for t_id in fsm['transitions']:
        transition = fsm['transitions'][t_id]

        s1 = transition['s1']
        input = transition['input']
        s2 = transition['s2']
        output = transition['output']

        if int(s1) in states.keys():
            s1 = states[int(s1)]
        else:
            print('State {} not exist in description file'.format(s1))
            exit(1)

        if int(s2) in states.keys():
            s2 = states[int(s2)]
        else:
            print('State {} not exist in description file'.format(s1))
            exit(1)

        if int(input) in inputs.keys():
            input = inputs[int(input)]
        else:
            print('Input {} not exist in description file'.format(s1))
            exit(1)

        if int(output) in outputs.keys():
            output = outputs[int(output)]
        else:
            print('Output {} not exist in description file'.format(s1))
            exit(1)

        new_fsm['transitions'][t_id] = {
            's1':     s1,
            'input':  input,
            's2':     s2,
            'output': output
        }

    if int(fsm['initial_state']) in states.keys():
        new_fsm['initial_state'] = states[int(fsm['initial_state'])]
    else:
        print('State {} not exist in description file'.format(s1))   
        exit(1)

    return new_fsm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Conversation/Validation of FSM v 1.0')
    parser.add_argument('-if', dest='input_fsm', type=str,
                        help='input FSM')
    parser.add_argument('-id', dest='input_description', type=str,
                        help='input FSM description')

    parser.add_argument('-of', dest='output_fsm', type=str,
                        help='output FSM')
    parser.add_argument('-od', dest='output_description', type=str,
                        help='output FSM description')


    args = parser.parse_args()

    # convert to literal
    if (args.input_fsm is not None) and (args.input_description is not None) and (args.output_fsm is not None):
        if not os.path.exists(args.input_fsm):
            print('Input FSM not exits')
            exit(1)

        if not os.path.exists(args.input_description):
            print('Input Description not exits')
            exit(1)

        fsm = read_fsm(args.input_fsm)
        description = read_description(args.input_description)

        # validate
        errors = validate_fsm(fsm)
        if len(errors) > 0:
            print('\n'.join(errors))
            exit(1)

        new_fsm = convert_to_literal_representation(fsm, description)

        write_fsm(new_fsm, args.output_fsm)
    # convert to numeric
    elif (args.input_fsm is not None) and (args.output_fsm is not None) and (args.output_description is not None):
        if not os.path.exists(args.input_fsm):
            print('Input FSM not exits')
            exit(1)

        fsm = read_fsm(args.input_fsm)

        # validate
        errors = validate_fsm(fsm)
        if len(errors) > 0:
            print('\n'.join(errors))
            exit(1)

        new_fsm, new_description = convert_to_numeric_representation(fsm)

        write_fsm(new_fsm, args.output_fsm)
        write_description(new_description, args.output_description)
    else:
        parser.print_help()