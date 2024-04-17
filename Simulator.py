import sys

#NOT TO BE EDITED.
unswapped_dict = {"zero": "00000"[::-1], "ra": "00001"[::-1], "sp": "00010"[::-1], "gp": "00011"[::-1], "tp": "00100"[::-1], "t0": "00101"[::-1], "t1": "00110"[::-1], "t2": "00111"[::-1], "s0": "01000"[::-1], "s1": "01001"[::-1], "a0": "01010"[::-1], "a1": "01011"[::-1], "a2": "01100"[::-1], "a3": "01101"[::-1], "a4": "01110"[::-1], "a5": "01111"[::-1], "a6": "10000"[::-1], "a7": "10001"[::-1], "s2": "10010"[::-1], "s3": "10011"[::-1], "s4": "10100"[::-1], "s5": "10101"[::-1], "s6": "10110"[::-1], "s7": "10111"[::-1], "s8": "11000"[::-1], "s9": "11001"[::-1], "s10": "11010"[::-1], "s11": "11011"[::-1], "t3": "11100"[::-1], "t4": "11101"[::-1], "t5": "11110"[::-1], "t6": "11111"[::-1]}

#WILL BE USED AS VARIANTS
Memory_Data = [0 for i in range((32*4)+1)]
Regs = {key: 0 for key in unswapped_dict.keys()}
Regs['sp'] = 256


def sext(val, bits = 32):
    if (val > (1 << bits) - 1 or val < -(1 << bits)):
        return
    sint = ''
    if (val >= 0):
        sint += bin(val)[2:]
    else:
        sint = bin((1 << bits) + val)[2:]
    msb = '0' if val >= 0 else '1'
    sint = sint[::-1]
    while (len(sint) < bits):
        sint += msb
    sint = sint[::-1]
    return('0b'+sint)


def sext_hex(val, bits = 8):
    if (val > (1 << bits) - 1 or val < -(1 << bits)):
        return
    sint = ''
    if (val >= 0):
        sint += hex(val)[2:]
    else:
        sint = hex((1 << bits) + val)[2:]
    msb = '0' if val >= 0 else 'f'
    sint = sint[::-1]
    while (len(sint) < bits):  # Each hexadecimal digit represents 4 binary digits
        sint += msb
    sint = sint[::-1]
    return('0x'+sint)


def addition(int1, int2, bits=32):
    result = int1 + int2

    # Handle overflow
    if result > (2 ** (bits - 1))-1:
        result -= 2 ** (bits-1)
    elif result < -(2 ** (bits - 1)):
        result += 2 ** (bits-1)

    return result

def execute(inst):
    global pc
    if(inst[0] == 'add'):
        Regs[inst[1]] = addition(Regs[inst[2]], Regs[inst[3]])
    elif(inst[0] == 'sub'):
        Regs[inst[1]] = addition(Regs[inst[2]], -Regs[inst[3]])
    elif(inst[0]=='slt'):
        if (Regs[inst[2]])<(Regs[inst[3]]):
            Regs[inst[1]]=1
    elif(inst[0]=='sltu'):
        if Regs[inst[2]]<Regs[inst[3]]:
            Regs[inst[1]]=1
    elif(inst[0]=='xor'):
        Regs[inst[1]]=(Regs[inst[2]])^(Regs[inst[3]])
    elif(inst[0]=='sll'):
        Regs[inst[1]]=Regs[inst[2]]<<((Regs[inst[3]])%32)
    elif(inst[0]=='srl'):
        Regs[inst[1]]=Regs[inst[2]]>>(Regs[inst[3]])%32
    elif(inst[0]=='or'):
        Regs[inst[1]]=Regs[inst[2]]|Regs[inst[3]]
    elif(inst[0]=='and'):
        Regs[inst[1]]=Regs[inst[2]]&Regs[inst[3]]
    elif(inst[0]=='lw'):
        Regs[inst[1]]=Memory_Data[(Regs[inst[3]]+(inst[2]))%(2**(16))]
    elif(inst[0]=='addi'):
    
        Regs[inst[1]]=Regs[inst[2]]+inst[3]
    elif(inst[0]=='sltiu'):
        if(Regs[inst[2]]<inst[3]):
            Regs[inst[1]]=1
    elif(inst[0]=='jalr'):
        Regs[inst[1]]=pc+4
        pc=(Regs[inst[2]]+(inst[3]))
        pc -= 4
    elif(inst[0]=='sw'):
        Memory_Data[(Regs[inst[3]]+inst[2])%(2**(16))]=Regs[inst[1]]
    elif(inst[0]=='beq'):
        if (Regs[inst[1]])==(Regs[inst[2]]):
            pc += ((inst[3]))
    elif(inst[0]=='bne'):
        if (Regs[inst[1]])!=(Regs[inst[2]]):
            pc+=((inst[3]))
            pc-=4
    elif(inst[0]=='bge'):
        if (Regs[inst[1]])>=(Regs[inst[2]]):
            pc+=((inst[3]))
    elif(inst[0]=='bgeu'):
        if abs(Regs[inst[1]])>=abs(Regs[inst[2]]):
            pc+=((inst[3]))
    elif(inst[0]=='blt'):
        if (Regs[inst[1]])<(Regs[inst[2]]):
            pc+=((inst[3]))
    elif(inst[0]=='bltu'):
        if abs(Regs[inst[1]])<abs(Regs[inst[2]]):
            pc+=((inst[3]))
    elif(inst[0]=='auipc'):
        Regs[inst[1]]= pc + (inst[2])
    elif(inst[0]=='lui'):
        Regs[inst[1]]=(inst[2])
    elif(inst[0]=='jal'):
        Regs[inst[1]]=pc+4
        pc+=((inst[2]))
        pc-=4
    Regs['zero'] = 0

def number(inst,type):
    inst = inst[::-1]
    def twos_complement_to_decimal(binary_str):
        if binary_str[0] == '1':
            inverted = ''.join('1' if bit == '0' else '0' for bit in binary_str)
            positive_equivalent = bin(int(inverted, 2) + 1)[2:]
            decimal_value = -int(positive_equivalent, 2)
        else:
            decimal_value = int(binary_str, 2)
        return decimal_value

    if type == 'B' : 

        def BTypeImmCalc(inst):
            inst = inst[::-1]
            imm = '0' + inst[8:12] + inst[25:31] + inst[7] + inst[31]
            imm = imm[::-1]
            return str(imm)
            
        s = BTypeImmCalc(inst)

        while (len(s) >= 2 and s[1] == '1'):
            s = s[:1] + s[2:]
        return twos_complement_to_decimal(s)
    
    elif type == 'I' :

        def ITypeImmCalc(inst):
            return str(inst[0:12])
        s = ITypeImmCalc(inst)

        while (len(s) >= 2 and s[1] == '1'):
            s = s[:1] + s[2:]
        return twos_complement_to_decimal(s)
    
    elif type == 'S' :
        def STypeImmCalc(inst):
            inst=inst[::-1]
            imm=inst[7:12]+inst[25:32]
            imm=imm[::-1]
            return str(imm)
        s = STypeImmCalc(inst)

        while (len(s) >= 2 and s[1] == '1'):
            s = s[:1] + s[2:]
        return twos_complement_to_decimal(s)
    
    elif type == 'U' :

        def UTypeImmCalc(inst):
            return str(inst[0:20])
        s = UTypeImmCalc(inst)
        if s == '11111111111111111111' :
            return -1
        else : s = s + '000000000000'
        return twos_complement_to_decimal(s)
    
    elif type == 'J' :
        
        def JTypeImmCalc(inst):
            inst = inst[::-1]
            imm = '0' + inst[21:32] + inst[20] + inst [12:20] + inst[31]
            imm = imm[::-1]
            return str(imm)

        s = JTypeImmCalc(inst)

        while (len(s) >= 2 and s[1] == '1'):
            s = s[:1] + s[2:]
        return twos_complement_to_decimal(s)
       

def instructionType(instruction):
    register_dict = {value: key for key, value in unswapped_dict.items()}
    instruction=instruction[::-1]

    currentInstruction=[]
    if(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='000'[::-1] and instruction[25:32]=='0000000'[::-1]):
        currentInstruction.append('add')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='000'[::-1] and instruction[25:32]=='0100000'[::-1]):
        currentInstruction.append('sub')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='001'[::-1] and instruction[25:32]=='0000000'[::-1]):
        currentInstruction.append('sll')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='010'[::-1] and instruction[25:32]=='0000000'[::-1]):
        currentInstruction.append('slt')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='011'[::-1] and instruction[25:32]=='0000000'[::-1]):
        currentInstruction.append('sltu')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='100'[::-1] and instruction[25:32]=='0000000'[::-1]):
        currentInstruction.append('xor')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='101'[::-1] and instruction[25:32]=='0000000'[::-1]):
        currentInstruction.append('srl')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='110'[::-1] and instruction[25:32]=='0000000'[::-1]):
        currentInstruction.append('or')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0110011'[::-1] and instruction[12:15]=='111'[::-1] and instruction[25:32]=='0000000'[::-1]):
        currentInstruction.append('and')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        return currentInstruction
    elif(instruction[0:7]=='0000011'[::-1] and instruction[12:15]=='010'[::-1]):
        currentInstruction.append('lw')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(number(instruction,'I'))
        currentInstruction.append(register_dict[instruction[15:20]])
        return currentInstruction
    elif(instruction[0:7]=='0010011'[::-1] and instruction[12:15]=='000'[::-1]):
        currentInstruction.append('addi')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(number(instruction,'I'))   
        return currentInstruction
    elif(instruction[0:7]=='0010011'[::-1] and instruction[12:15]=='011'[::-1]):
        currentInstruction.append('sltiu')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(number(instruction,'I'))
        return currentInstruction
    elif(instruction[0:7]=='1100111'[::-1] and instruction[12:15]=='000'[::-1]):
        currentInstruction.append('jalr')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(number(instruction,'I'))  
        return currentInstruction
    elif(instruction[0:7]=='0100011'[::-1] and instruction[12:15]=='010'[::-1]):
        currentInstruction.append('sw')
        currentInstruction.append(register_dict[instruction[20:25]])
        currentInstruction.append(number(instruction,'S'))
        currentInstruction.append(register_dict[instruction[15:20]])    
        return currentInstruction
    elif(instruction[0:7]=='1100011'[::-1] and instruction[12:15]=='000'[::-1]):
        currentInstruction.append('beq')
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        currentInstruction.append(number(instruction,'B'))
        return currentInstruction
    elif(instruction[0:7]=='1100011'[::-1] and instruction[12:15]=='001'[::-1]):
        currentInstruction.append('bne')
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        currentInstruction.append(number(instruction,'B'))
        return currentInstruction
    elif(instruction[0:7]=='1100011'[::-1] and instruction[12:15]=='100'[::-1]):
        currentInstruction.append('blt')
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        currentInstruction.append(number(instruction,'B'))
        return currentInstruction
    elif(instruction[0:7]=='1100011'[::-1] and instruction[12:15]=='101'[::-1]):
        currentInstruction.append('bge')
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        currentInstruction.append(number(instruction,'B'))
        return currentInstruction
    elif(instruction[0:7]=='1100011'[::-1] and instruction[12:15]=='110'[::-1]):
        currentInstruction.append('bltu')
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        currentInstruction.append(number(instruction,'B'))
        return currentInstruction
    elif(instruction[0:7]=='1100011'[::-1] and instruction[12:15]=='111'[::-1]):
        currentInstruction.append('bgeu')
        currentInstruction.append(register_dict[instruction[15:20]])
        currentInstruction.append(register_dict[instruction[20:25]])
        currentInstruction.append(number(instruction,'B'))
        return currentInstruction
    elif(instruction[0:7]=='0110111'[::-1]):
        currentInstruction.append('lui')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(number(instruction,'U'))
        return currentInstruction
    elif(instruction[0:7]=='0010111'[::-1]):
        currentInstruction.append('auipc')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(number(instruction,'U'))
        return currentInstruction
    elif(instruction[0:7]=='1101111'[::-1]):
        currentInstruction.append('jal')
        currentInstruction.append(register_dict[instruction[7:12]])
        currentInstruction.append(number(instruction,'J'))
        return currentInstruction
    elif(instruction[0:7]=='0000000'[::-1] and instruction[12:15]=='000'[::-1] and instruction[25:32]=='0000000'[::-1]):
        if(instruction[20:25]!='00000'[::-1]):
            currentInstruction.append('mul')
            currentInstruction.append(register_dict[instruction[7:12]])
            currentInstruction.append(register_dict[instruction[15:20]])
            currentInstruction.append(register_dict[instruction[20:25]])
            return currentInstruction
        elif(instruction[15:20]!='00000'[::-1] or instruction[7:12]!='00000'[::-1]):
            currentInstruction.append('rvrs')
            currentInstruction.append(register_dict[instruction[7:12]])
            currentInstruction.append(register_dict[instruction[15:20]])
            return currentInstruction
        else: 
            currentInstruction.append('rst/hault')
            return currentInstruction

instructionList = []
inputfilepath = sys.argv[1]
inputFile=open(inputfilepath,'r')
inputList=[]
for line in inputFile:
    inputList.append(line)
inputFile.close()

for i in range(inputList.count('\n')):
    inputList.remove('\n')

for i in inputList:
    instructionList.append(instructionType(i[0:32]))
    for j in range(3):
        instructionList.append(None)

outputfilepath = sys.argv[2]
output=open(outputfilepath,'a')
pc = 0
while pc < len(instructionList):
    if (instructionList[pc] != ['beq', 'zero', 'zero', 0]): 
        execute(instructionList[pc])
    else:
        break
    pc += 4
    output.write(sext(pc) + ' ')
    for i in Regs:
        output.write(sext(Regs[i])+ ' ')
    output.write('\n')
output.write(sext(pc) + ' ')
for i in Regs:
    output.write(sext(Regs[i])+ ' ')
output.write('\n')

for i in range(0,13):
    if (i%4 == 0):
        output.write('0x0001000'+hex(i)[2:] + ':' + sext(Memory_Data[i]))
        output.write('\n')
for i in range(13,127):
    if (i%4 == 0):
        output.write('0x000100'+hex(i)[2:] + ':' + sext(Memory_Data[i]))
        output.write('\n')

output.close()