class Computer:
    '''Stores program list and other values of the IntCode Computer'''
    def __init__(self, program=[], input_val=0):
        self.program = program
        self.pointer = 0
        self.input_val = input_val
        self.opcode = None
        self.output_val = 0
        self.use_phase = False
        self.relative_base = 0
        self.opcode_funcs = {1: self.op1,
                             2: self.op2,
                             3: self.op3,
                             4: self.op4,
                             5: self.op5,
                             6: self.op6,
                             7: self.op7,
                             8: self.op8,
                             9: self.op9,
                             99: self.op99}

    def get_param_inds(self, modes):
        '''Returns the program indices for the parameters to be passed
        to the next opcode.'''
        param_inds = []
        for ind, m in enumerate(modes):
            if m == 0:
                param_inds.append(self.program[self.pointer+ind+1])
            elif m == 1:
                param_inds.append(self.pointer+ind+1)
            elif m == 2:
                param_inds.append(self.program[self.pointer+ind+1] +
                                  self.relative_base)
        return param_inds

    def op1(self, param_inds):
        op_output = self.program[param_inds[0]] + self.program[param_inds[1]]
        self.program[param_inds[2]] = op_output

        self.pointer += 4

    def op2(self, param_inds):
        op_output = self.program[param_inds[0]] * self.program[param_inds[1]]
        self.program[param_inds[2]] = op_output

        self.pointer += 4

    def op3(self, param_inds):
        op_output = self.input_val
        self.program[param_inds[0]] = op_output

        self.pointer += 2

    def op4(self, param_inds):
        self.output_val = self.program[param_inds[0]]

        self.pointer += 2

    def op5(self, param_inds):
        if self.program[param_inds[0]] != 0:
            self.pointer = self.program[param_inds[1]]
        else:
            self.pointer += 3

    def op6(self, param_inds):
        if self.program[param_inds[0]] == 0:
            self.pointer = self.program[param_inds[1]]
        else:
            self.pointer += 3

    def op7(self, param_inds):
        if self.program[param_inds[0]] < self.program[param_inds[1]]:
            self.program[param_inds[2]] = 1
        else:
            self.program[param_inds[2]] = 0
        self.pointer += 4

    def op8(self, param_inds):
        if self.program[param_inds[0]] == self.program[param_inds[1]]:
            self.program[param_inds[2]] = 1
        else:
            self.program[param_inds[2]] = 0
        self.pointer += 4

    def op9(self, param_inds):
        self.relative_base += self.program[param_inds[0]]
        self.pointer += 2

    def op99(self, param_inds):
        # print('op99: DONE')
        None

    def run_op(self, verbose=False):
        '''Runs the next opcode in the program'''
        opcode, modes = read_instruction(self.program[self.pointer])
        param_inds = self.get_param_inds(modes)
        if self.param_inds and (max(self.param_inds) > len(self.program)-1):
            # This adds more memory than necessary (+1000)
            self.program.extend(
                [0 for _ in range(max(param_inds) - len(self.program) + 1)])
        if verbose:
            print(self.program)
            print('Pointer: {}\nOpcode: {}\nparam_inds: {}\nrel base: {}'.format(
                self.pointer, opcode, param_inds, self.relative_base))
            print(len(self.program))

        self.opcode_funcs[opcode](param_inds)
        self.opcode = opcode


def input_to_program(fn):
    '''Reads input file and returns IntCode program as a list.'''
    with open(fn, 'r') as fh:
        for _ in range(1):
            program_string = fh.readline().rstrip()

    return [int(x) for x in program_string.split(',')]


def read_instruction(inst):
    '''Reads instruction and outputs opcode and parameter modes.'''
    opcode_nparams = {1: 3,
                      2: 3,
                      3: 1,
                      4: 1,
                      5: 2,
                      6: 2,
                      7: 3,
                      8: 3,
                      9: 1,
                      99: 0
                      }
    opcode = int(str(inst)[-2:])
    modes = str(inst)[:-2].zfill(opcode_nparams[opcode])
    modes = [int(m) for m in modes[-1::-1]]
    return opcode, modes
