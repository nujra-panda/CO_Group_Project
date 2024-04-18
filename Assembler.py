import sys
def immediateConverter(intVal,numOfBits):
    if(intVal>=0):
        return(bin(intVal)[2:].zfill(numOfBits))
    else: 
        return(bin(2 ** (numOfBits) + intVal)[2:])
def check(inputList):
    present=False
    for i in range(len(inputList)):
        if((inputList[i]=="beq zero,zero,0")or(inputList[i]=="beq zero,zero,0\n")):
            present=True
            break
    bool1=False
    bool2=False
    if(not present):
        return("Error: Virtual Hault is missing")
    elif((present)and((inputList[-1]!="beq zero,zero,0"))):
        bool1=True
        if((inputList[-1]!="beq zero,zero,0\n")and(present)):
            bool2=True
    if((bool1)and(bool2)):
        return("Virtual Hault is not being used as the last instruction")
    return(1)
labelIndex=dict()
def lineSolver(instruction,lineIndex):
    if ((instruction == "\n")or(instruction=="")) :
        return
    exceptionBI1=['lw','sw']
    exceptionBI2=['jal','lui','auipc']
    outputStr=''
    elements=[]
    elements.append(instruction[0:instruction.find(' ')])
    if(((elements[0])not in(exceptionBI1))and((elements[0])not in(exceptionBI2))):
        elements.append(instruction[instruction.find(' ')+1:instruction.find(',')])
        elements.append(instruction[instruction.find(',')+1:instruction.rfind(',')])
        elements.append(instruction[instruction.rfind(',')+1:instruction.rfind('\n')])
    elif((elements[0])in(exceptionBI1)):
        elements.append(instruction[instruction.find(' ')+1:instruction.find(',')])
        elements.append(instruction[instruction.find(',')+1:instruction.find('(')])
        elements.append(instruction[instruction.find('(')+1:instruction.find(")")])
    elif((elements[0])in(exceptionBI2)):
        elements.append(instruction[instruction.find(' ')+1:instruction.find(',')])
        elements.append(instruction[instruction.find(',')+1:instruction.rfind('\n')])
    if ((elements[-1])in(labelIndex)):
        elements[-1]=str((labelIndex[elements[-1]]-lineIndex)*4)
    '''funct3 and funct7 for R type instructions'''  
    basicR=['add','sub','sll','slt','sltu','xor','srl','or','and']
    RinstList=[['add','000','0000000'],['sub','000','0100000'],['sll','001','0000000'],['slt','010','0000000'],['sltu','011','0000000'],['xor','100','0000000'],['srl','101','0000000'],['or','110','0000000'],['and','111','0000000']]
    RinstListFunct3_dict={item[0]: item[1] for item in RinstList}
    RinstListFunct7_dict={item[0]: item[2] for item in RinstList}
    '''opcode and funct3 for I type instructions'''
    basicI=['addi','lw','sltiu','jalr']
    IinstList=[['addi','0010011','000'],['lw','0000011','010'],['sltiu','0010011','011'],['jalr','1100111','000']]
    IinstListOpcode_dict={item[0]: item[1] for item in IinstList}
    IinstListFunct3_dict={item[0]: item[2] for item in IinstList}
    '''opcode and funct3 for S type instructions'''
    basicS=['sw']
    SinstList=[['sw','0100011','010']]
    SinstListOpcode_dict={item[0]: item[1] for item in SinstList}
    SinstListFunct3_dict={item[0]: item[2] for item in SinstList}
    '''funct3 for B type instructions'''
    basicB=['beq','bne','blt','bge','bltu','bgeu']
    BinstList=[['beq','000'],['bne','001'],['blt','100'],['bge','101'],['bltu','110'],['bgeu','111']]
    BinstListFunct3_dict={item[0]: item[1] for item in BinstList}
    '''opcode for U type instructions'''
    basicU=['lui','auipc']
    UinstList=[['lui','0110111'],['auipc','0010111']]
    UinstListOpcode_dict={item[0]: item[1] for item in UinstList}
    '''opcode for J type instructions'''
    basicJ=['jal']
    JinstList=[['jal','1101111']]
    JinstListOpcode_dict={item[0]: item[1] for item in JinstList}
    '''Register Encoding'''
    regEncoding=[['zero','00000'],['ra','00001'],['sp','00010'],['gp','00011'],['tp','00100'],['t0','00101'],['t1','00110'],['t2','00111'],['s0','01000'],['fp','01000'],['s1','01001'],['a0','01010'],['a1','01011'],['a2','01100'],['a3','01101'],['a4','01110'],['a5','01111'],['a6','10000'],['a7','10001'],['s2','10010'],['s3','10011'],['s4','10100'],['s5','10101'],['s6','10110'],['s7','10111'],['s8','11000'],['s9','11001'],['s10','11010'],['s11','11011'],['t3','11100'],['t4','11101'],['t5','11110'],['t6','11111']]
    regEncoding_dict={item[0]: item[1] for item in regEncoding}
    '''I S B==12; U==32; J==20'''
    if((elements[-1]).isdigit()==True):
        if(((elements[0])in(basicI))or((elements[0])in(basicS))or((elements[0])in(basicB))):
            if((elements[0] == 'lw')or(elements[0]=='sw')):
                if((int(elements[-2])) > 2047)or(int(elements[-2])<-2048):
                    return("Error: Immediate value out of range"+'\n')
            if((int(elements[-1]) > 2047)or(int(elements[-1])<-2048)):
                    return("Error: Immediate value out of range"+'\n')
        elif((elements[0])in(basicU)):
            if((int(elements[-1])>1048575)or(int(elements[-1]) < 0)):
                return("Error: Immediate value out of range"+'\n')
        elif((elements[0])in(basicJ)):
            if((int(elements[-1])>1048575)or(int(elements[-1])<-1048576)):
                return("Error: Immediate value out of range"+'\n')
    try:
        if((elements[0])in(basicR)):
            outputStr=RinstListFunct7_dict[elements[0]]+str(regEncoding_dict[elements[3]])+str(regEncoding_dict[elements[2]])+RinstListFunct3_dict[elements[0]]+str(regEncoding_dict[elements[1]])+'0110011'
            return(outputStr+'\n')
        elif((elements[0])in(basicB)):
            binaryNumber=immediateConverter(int(elements[3]),12)
            binaryNumber=binaryNumber[::-1]
            outputStr=binaryNumber[11]+binaryNumber[5:11][::-1]+str(regEncoding_dict[elements[2]])+str(regEncoding_dict[elements[1]])+str(BinstListFunct3_dict[elements[0]])+binaryNumber[1:5][::-1]+binaryNumber[10]+'1100011'
            return(outputStr+'\n')
        elif((elements[0])in(basicI)):
            if(elements[0]=='lw'):
                binaryNumber=immediateConverter(int(elements[2]),12)
                outputStr=binaryNumber+str(regEncoding_dict[elements[3]])+IinstListFunct3_dict[elements[0]]+regEncoding_dict[elements[1]]+IinstListOpcode_dict[elements[0]]
                return(outputStr+'\n')
            else:
                binaryNumber=immediateConverter(int(elements[3]),12)
                outputStr=binaryNumber+str(regEncoding_dict[elements[2]])+IinstListFunct3_dict[elements[0]]+regEncoding_dict[elements[1]]+IinstListOpcode_dict[elements[0]]
                return(outputStr+'\n')
        elif((elements[0])in(basicS)):
            binaryNumber=immediateConverter(int(elements[2]),12)
            outputStr=binaryNumber[0:7]+str(regEncoding_dict[elements[1]])+str(regEncoding_dict[elements[3]])+SinstListFunct3_dict[elements[0]]+binaryNumber[7:12]+'0100011'
            return(outputStr+'\n')
        elif((elements[0])in(basicU)):
            binaryNumber=immediateConverter(int(elements[2]),32)
            binaryNumber=binaryNumber[::-1]
            outputStr=binaryNumber[12:32]+str(regEncoding_dict[elements[1]])+UinstListOpcode_dict[elements[0]]
            return(outputStr+'\n')
        elif((elements[0])in(basicJ)):          
            binaryNumber=immediateConverter(int(elements[2]),20)
            outputStr=binaryNumber[0]+binaryNumber[9:19]+binaryNumber[9]+binaryNumber[1:9]+str(regEncoding_dict[elements[1]])+JinstListOpcode_dict[elements[0]]
            return(outputStr+'\n')
        else :
            return("Error: Instruction not found"+'\n')
    except(KeyError):
        return("Pls enter a valid assembly code")
    except(ValueError):
        return("Pls enter a valid assembly code")
def main():
    input_file_path=sys.argv[1]
    inputFile=open(input_file_path,'r')
    inputList=[]
    for line in inputFile:
        inputList.append(line)
    inputFile.close() 
    for i in range(inputList.count('\n')):
        inputList.remove('\n')
    output_file_path=sys.argv[2]
    output=open(output_file_path,'a')
    outputList=[]
    for i in range(len(inputList)):
        inputList[i]=inputList[i].lstrip()
        if(inputList[i].find(':')!=-1):
            labelIndex[inputList[i][0:inputList[i].find(':')]]=i
            inputList[i]=inputList[i][inputList[i].find(' ')+1:]
    if(check(inputList)=="Error: Virtual Hault is missing"):
        output.write("Error: Virtual Hault is missing")
        return
    elif(check(inputList)=="Virtual Hault is not being used as the last instruction"):
        output.write("Virtual Hault is not being used as the last instruction")
        return
    elif(check(inputList)==1):
        for i in range(len(inputList)-1):
            str1=lineSolver(str(inputList[i]),i)
            outputList.append(str1)
    outputList.append('00000000000000000000000001100011')
    for i in range(outputList.count(None)):
        outputList.remove(None)
    for i in range(len(outputList)):
        if(outputList[i]=="Error: Instruction not found"+'\n'):
            output.write("Error: Instruction not found on "+"line "+str(i+1)+".")
            return
    for i in range(len(outputList)):
        if(outputList[i]=="Error: Immediate value out of range"+'\n'):
            output.write("Error: Immediate value out of range"+'\n')
            return
    for i in outputList:
        if(i=="Pls enter a valid assembly code"):
            output.write("Pls enter a valid assembly code")
            return
    for i in outputList:
        output.write(i)
    output.close()
main()
