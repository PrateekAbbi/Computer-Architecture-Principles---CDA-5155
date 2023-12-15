# On my honor, I have neither given nor received any unauthorized aid on this assignment.
import sys
import os

inputFileName = sys.argv[-1]

print(inputFileName)

simulation = open("simulation.txt", "w+")
disassembly = open("disassembly.txt", "w+")

# S-Type
category1 = {
    "00000": "beq",  # branch equal
    "00001": "bne",  # branch not equal
    "00010": "blt",  # branch less than
    "00011": "sw"  # Store Word
}

# R-Type
category2 = {
    "00000": "add",  # add Arithmetic Unit
    "00001": "sub",  # Subtract Arithmetic Unit
    "00010": "and",  # AND register-register
    "00011": "or"  # OR register-register
}

# I-Type
category3 = {
    "00000": "addi",  # Add immediate
    "00001": "andi",  # AND register-immediate
    "00010": "ori",  # OR register-immediate
    "00011": "sll",  # Shift Logical Left
    "00100": "sra",  # Shift Arithmetic Right
    "00101": "lw"  # Load Word
}

# U-Type
category4 = {
    "00000": "jal",  # Jump and Link address
    "11111": "break"  # Break
}

memoryData, registerIns = {}, {}

# Disassembly
with open(inputFileName, "r") as input_file:
    i = 256
    breakEncountered = False
    for line in input_file:
        line = line.strip()

        categoryCode = line[-2:]
        opCode = line[-7:-2]

        if breakEncountered == False:
            if categoryCode == "00":  # Category 1
                operation = category1[opCode]
                offset = line[0:7]+line[20:25]
                rs2 = int(line[7:12], 2)
                rs1 = int(line[12:17], 2)
                if offset[0] == "1":
                    newOffSet = ""
                    for j in range(0, 12):
                        if offset[j] == "0":
                            newOffSet += "1"
                        else:
                            newOffSet += "0"

                    offset = bin(int(newOffSet, 2)+1)[2:]
                if operation == "sw":
                    if offset[0] == "1":
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rs1}, {-1*int(offset, 2)}(x{rs2})\n"
                        )
                        registerIns[i] = f"{operation} {rs1} {rs2} {-1*int(offset,2)}"
                    else:
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rs1}, {int(offset, 2)}(x{rs2})\n"
                        )
                        registerIns[i] = f"{operation} {rs1} {rs2} {int(offset, 2)}"

                else:
                    if offset[0] == "1":
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rs1}, x{rs2}, #{-1*int(offset, 2)}\n"
                        )
                        registerIns[i] = f"{operation} {rs1} {rs2} {-1*int(offset, 2)}"
                    else:
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rs1}, x{rs2}, #{int(offset, 2)}\n"
                        )
                        registerIns[i] = f"{operation} {rs1} {rs2} {int(offset, 2)}"

            if categoryCode == "01":  # Category 2
                operation = category2[opCode]
                rs1 = int(line[12:17], 2)
                rs2 = int(line[7:12], 2)
                rd = int(line[20:25], 2)

                disassembly.write(
                    f"{line}\t{i}\t{operation} x{rd}, x{rs1}, x{rs2}\n"
                )
                registerIns[i] = f"{operation} {rd} {rs1} {rs2}"

            if categoryCode == "10":  # Category 3
                operation = category3[opCode]
                immediateVal = line[0:12]

                if immediateVal[0] == "1":
                    newImmVal = ""
                    for j in range(0, 12):
                        if immediateVal[j] == "0":
                            newImmVal += "1"
                        else:
                            newImmVal += "0"

                    immediateVal = bin(int(newImmVal, 2)+1)[2:]

                rs1 = int(line[12:17], 2)
                rd = int(line[20:25], 2)

                if immediateVal[0] == "1":
                    if operation == "lw":
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rd}, {-1*int(immediateVal, 2)}(x{rs1})\n"
                        )
                        # registerIns[i] = f"{operation} {rd} {rs1} {int(immediateVal, 2)}"
                    else:
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rd}, x{rs1}, #{-1*int(immediateVal, 2)}\n"
                        )
                    registerIns[i] = f"{operation} {rd} {rs1} {-1*int(immediateVal, 2)}"
                else:
                    if operation == "lw":
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rd}, {int(immediateVal, 2)}(x{rs1})\n"
                        )
                        # registerIns[i] = f"{operation} {rd} {rs1} {int(immediateVal, 2)}"
                    else:
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rd}, x{rs1}, #{int(immediateVal, 2)}\n"
                        )
                    registerIns[i] = f"{operation} {rd} {rs1} {int(immediateVal, 2)}"

            if categoryCode == "11":  # Category 4
                operation = category4[opCode]
                immediateVal, rd = line[0:20], int(line[20:25], 2)

                if immediateVal[0] == "1":
                    newImmediateVal = ""
                    for j in range(0, 20):
                        if immediateVal[j] == "0":
                            newImmediateVal += "1"
                        else:
                            newImmediateVal += "0"

                    immediateVal = -1 * \
                        int(bin(int(newImmediateVal, 2)+1)[2:], 2)

                    if operation == "jal":
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rd}, #{immediateVal}\n"
                        )
                        registerIns[i] = f"{operation} {rd} {immediateVal}"
                else:
                    if operation == "jal":
                        disassembly.write(
                            f"{line}\t{i}\t{operation} x{rd}, #{int(immediateVal, 2)}\n"
                        )
                        registerIns[i] = f"{operation} {rd} {int(immediateVal, 2)}"

                if operation == "break":
                    disassembly.write(
                        f"{line}\t{i}\tbreak\n"
                    )
                    registerIns[i] = "break"
                    breakEncountered = True
        else:
            if line[0] == "1":
                newLine = ""
                for j in range(0, 32):
                    if (line[j] == "0"):
                        newLine += "1"
                    else:
                        newLine += "0"
                newLine = bin(int(newLine, 2)+1)[2:]

                disassembly.write(
                    f"{line}\t{i}\t{-1*int(newLine, 2)}\n"
                )
                memoryData[i] = -1*int(newLine, 2)
            else:
                disassembly.write(
                    f"{line}\t{i}\t{int(line, 2)}\n"
                )
                memoryData[i] = int(line, 2)
        i += 4

registerData = [0]*32
iF = {"waiting": "", "executed": ""}
preIssueQueue = []
preAlu1Queue = []  # load or store
preMEMQueue = ""
postMEMQueue = ""
preAlu2Queue = ""  # Arithmetic
postAlu2Queue = ""
preAlu3Queue = ""  # Logical
postAlu3Queue = ""

registerResultStatus = {0: 'Available', 1: 'Available', 2: 'Available', 3: 'Available', 4: 'Available', 5: 'Available', 6: 'Available', 7: 'Available', 8: 'Available', 9: 'Available', 10: 'Available', 11: 'Available', 12: 'Available', 13: 'Available', 14: 'Available', 15: 'Available',
                        16: 'Available', 17: 'Available', 18: 'Available', 19: 'Available', 20: 'Available', 21: 'Available', 22: 'Available', 23: 'Available', 24: 'Available', 25: 'Available', 26: 'Available', 27: 'Available', 28: 'Available', 29: 'Available', 30: 'Available', 31: 'Available', 32: 'Available'}
activeRegisters = {0: 'not active', 1: 'not active', 2: 'not active', 3: 'not active', 4: 'not active', 5: 'not active', 6: 'not active', 7: 'not active', 8: 'not active', 9: 'not active', 10: 'not active', 11: 'not active', 12: 'not active', 13: 'not active', 14: 'not active', 15: 'not active',
                   16: 'not active', 17: 'not active', 18: 'not active', 19: 'not active', 20: 'not active', 21: 'not active', 22: 'not active', 23: 'not active', 24: 'not active', 25: 'not active', 26: 'not active', 27: 'not active', 28: 'not active', 29: 'not active', 30: 'not active', 31: 'not active', 32: 'not active'}
functionalUnitStatus = {"ALU1": [0]*9, "ALU2": [0]*9, "ALU3": [0]*9}
readingReg, writingReg = [], []
locks = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: '',
         17: '', 18: '', 19: '', 20: '', 21: '', 22: '', 23: '', 24: '', 25: '', 26: '', 27: '', 28: '', 29: '', 30: '', 31: '', 32: ''}

cycle, i, encountered = 1, 256, False
issuedIn = ""
while encountered == False:
    clock, writeBackHalt, preIssueFullHalt = 0, False, False
    simulation.write(f"\n--------------------\nCycle {cycle}:\n\n")
    # operation = ""

    # print("225 cycle", cycle, "\nReading", readingReg, "\nWriting", writingReg, "\nLocks", locks, "\nregisterResultStatus",
    #       registerResultStatus, "\nActive", activeRegisters, "\n----------------------------------------------\n")
    # if cycle > 30:
    #     break
    if i in registerIns:

        # checking for the branch instructions
        if iF["executed"] != "":  # This means that in previous cycle, branch got executed
            iF["executed"] = ""

        # This means that in previous cycle, branch got stuck in waiting state because one of the registers on which branch wants to operate is not free.
        if iF["waiting"] != "":
            instruction = iF["waiting"].split(" ")
            operation = instruction[0]

            if operation == "jal":
                rd, offset = int(
                    instruction[1][1:-1]), int(instruction[2][1:])

                if activeRegisters[rd] == "not active" and registerResultStatus[rd] == "Available":
                    registerData[rd] = i+4
                    i += (offset << 1)

                    iF["executed"] = f"{operation} x{rd}, #{offset>>1}"
                    iF["waiting"] = ""

            else:
                rs1, rs2, offset = int(
                    instruction[1][1:-1]), int(instruction[2][1:-1]), int(instruction[3][1:])

                if activeRegisters[rs1] == "not active" and activeRegisters[rs2] == "not active" and registerResultStatus[rs1] == "Available" and registerResultStatus[rs2] == "Available":

                    if operation == "beq":
                        if registerData[rs1] == registerData[rs2]:
                            updatedOffset = offset << 1
                            i += updatedOffset-4
                    if operation == "bne":
                        if registerData[rs1] != registerData[rs2]:
                            updatedOffset = offset << 1
                            i += updatedOffset-4
                    if operation == "blt":
                        if registerData[rs1] < registerData[rs2]:
                            updatedOffset = offset << 1
                            i += updatedOffset-4

                    iF["executed"] = f"{operation} x{rs1}, x{rs2}, #{offset}"
                    iF["waiting"] = ""

        # from postALU to execution and writeback
        if postMEMQueue != "":
            instruction = postMEMQueue.split(" ")
            operation = instruction[0]

            if operation == "lw":
                rd, rs1, immVal = int(
                    instruction[1][1:-1]), int(instruction[2][5:-1]), int(instruction[2][0:3])

                registerData[rd] = memoryData[immVal+registerData[rs1]]

                registerResultStatus[rd] = "Available"
                activeRegisters[rd], activeRegisters[rs1] = "not active", "not active"
                locks[rd] = ""
                writingReg.remove(rd)
                readingReg.remove(rs1)

                if rd in readingReg:
                    writeBackHalt = True

            postMEMQueue = ""

        if preMEMQueue != "":
            instruction = preMEMQueue.split(" ")
            operation = instruction[0]

            if operation == "sw":
                rs1, rs2, offset = int(instruction[1][1:-1]), int(
                    instruction[2][5:-1]), int(instruction[2][0:3])
                memoryData[offset+registerData[rs2]] = registerData[rs1]
                registerResultStatus[rs1], registerResultStatus[rs2] = "Available", "Available"
                activeRegisters[rs1], activeRegisters[rs2] = "not active", "not active"
                locks[rs1], locks[rs2] = "", ""
                readingReg.remove(rs1)
                readingReg.remove(rs2)

                preMEMQueue = ""

                if rs1 in readingReg or rs2 in readingReg:
                    writeBackHalt = True
            else:
                postMEMQueue = preMEMQueue
                preMEMQueue = ""

        if postAlu2Queue != "":
            instruction = postAlu2Queue.split(" ")
            operation = instruction[0]
            rd, rs1, rs2ORImm = int(
                instruction[1][1:-1]), int(instruction[2][1:-1]), int(instruction[3][1:])

            if operation == "add":
                registerData[rd] = registerData[rs1] + registerData[rs2ORImm]
            elif operation == "addi":
                registerData[rd] = registerData[rs1] + rs2ORImm
            elif operation == "sub":
                registerData[rd] = registerData[rs1] - registerData[rs2ORImm]

            registerResultStatus[rd], registerResultStatus[rs1] = "Available", "Available"
            activeRegisters[rd], activeRegisters[rs1] = "not active", "not active"
            locks[rd], locks[rs1] = "", ""
            writingReg.remove(rd)
            readingReg.remove(rs1)

            if instruction[3][0] == "x":
                registerResultStatus[rs2ORImm] = "Available"
                activeRegisters[rs2ORImm] = "not active"
                locks[rs2ORImm] = ""
                readingReg.remove(rs2ORImm)

            # checking RAW or WAR Dependency of any instruction
            if rd in readingReg or rs1 in writingReg or (instruction[3][0] == "x" and rs2ORImm in writingReg):
                writeBackHalt = True

            postAlu2Queue = ""

        if postAlu3Queue != "":
            instruction = postAlu3Queue.split(" ")
            operation = instruction[0]
            rd, rs1, rs2ORImm = int(instruction[1][1:-
                                                   1]), int(instruction[2][1:-1]), int(instruction[3][1:])

            if operation == "or":
                registerData[rd] = registerData[rs1] | registerData[rs2ORImm]
            elif operation == "and":
                registerData[rd] = registerData[rs1] & registerData[rs2ORImm]
            elif operation == "andi":
                registerData[rd] = registerData[rs1] & (rs2ORImm)
            elif operation == "ori":
                registerData[rd] = registerData[rs1] | (rs2ORImm)
            elif operation == "sll":
                registerData[rd] = registerData[rs1] << (rs2ORImm)
            elif operation == "sra":
                registerData[rd] = registerData[rs1] >> (rs2ORImm)

            registerResultStatus[rd], registerResultStatus[rs1] = "Available", "Available"
            activeRegisters[rd], activeRegisters[rs1] = "not active", "not active"
            locks[rd], locks[rs1] = "", ""
            writingReg.remove(rd)
            readingReg.remove(rs1)

            if instruction[3][0] == "x":
                registerResultStatus[rs2ORImm] = "Available"
                activeRegisters[rs2ORImm] = "not active"
                locks[rs2ORImm] = ""
                readingReg.remove(rs2ORImm)

            if rd in readingReg or rs1 in writingReg or (instruction[3][0] == "x" and rs2ORImm in writingReg):
                writeBackHalt = True

            postAlu3Queue = ""

        if writeBackHalt == False:
            # from preALU to postALU
            if len(preAlu1Queue) > 0:
                preMEMQueue = preAlu1Queue.pop(0)

            if preAlu2Queue != "":
                postAlu2Queue = preAlu2Queue
                preAlu2Queue = ""

            if preAlu3Queue != "":
                postAlu3Queue = preAlu3Queue
                preAlu3Queue = ""

            # from pre-issue queue to respective preALU
            instInd = 0
            if len(preIssueQueue) == 4:
                preIssueFullHalt = True

            for instruction in preIssueQueue[:]:
                # if len(preIssueQueue) > 0:
                instruction = instruction.split(" ")
                operation = instruction[0]

                Available = True

                if instInd == 0:
                    if operation == "sw":
                        rs1, rs2, offset = int(instruction[1][1:-1]), int(
                            instruction[2][5:-1]), int(instruction[2][0:3])

                        if registerResultStatus[rs1] == "not Available" or registerResultStatus[rs2] == "not Available" or locks[rs2] == "writingLock" or locks[rs1] == "writingLock":
                            # if rd in readingReg or rs1 in writingReg:
                            Available = False

                        if Available and len(preAlu1Queue) < 2 and issuedIn != "ALU1":
                            preAlu1Queue.append(
                                f"{operation} x{rs1}, {offset}(x{rs2})")
                            # registerResultStatus[rd], registerResultStatus[rs1] = "not Available", "not Available"
                            registerResultStatus[rs1], registerResultStatus[rs2] = "not Available", "not Available"
                            locks[rs1], locks[rs2] = "writingLock", "writingLock"
                            # if rs1 not in readingReg:
                            #     locks[rs1] = "writingLock"
                            preIssueQueue.remove(preAlu1Queue[0])
                            len([preAlu1Queue]) > 1 and preIssueQueue.remove(
                                preAlu1Queue[1])
                            issuedIn = "ALU1"

                    if operation in category2.values():
                        rd, rs1, rs2 = int(
                            instruction[1][1:-1]), int(instruction[2][1:-1]), int(instruction[3][1:])

                        # send to preAlu2 Queue after checking the registerResultStatus
                        if operation == "add" or operation == "sub":
                            # or rd in readingReg or rs1 in writingReg or rs2 in writingReg:
                            if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or registerResultStatus[rs2] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock" or locks[rs2] == "writingLock":
                                # if rd in readingReg or rs1 in writingReg or rs2 in writingReg:
                                Available = False

                            if Available and preAlu2Queue == "" and postAlu2Queue == "" and issuedIn != "ALU2":
                                preAlu2Queue = f"{operation} x{rd}, x{rs1}, x{rs2}"
                                registerResultStatus[rd], registerResultStatus[rs1], registerResultStatus[
                                    rs2] = "not Available", "not Available", "not Available"
                                locks[rd] = "writingLock"
                                locks[rs1] = "writingLock"
                                locks[rs2] = "writingLock"
                                preIssueQueue.remove(preAlu2Queue)
                                issuedIn = "ALU2"
                        # send to preAlu3 (for and or instructions) Queue after checking the registerResultStatus
                        else:
                            # or rd in readingReg or rs1 in writingReg or rs2 in writingReg:
                            if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or registerResultStatus[rs2] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock" or locks[rs2] == "writingLock":
                                # if rd in readingReg or rs1 in writingReg or rs2 in writingReg:
                                Available = False

                            if Available and preAlu3Queue == "" and postAlu3Queue == "" and issuedIn != "ALU3":
                                preAlu3Queue = f"{operation} x{rd}, x{rs1}, x{rs2}"
                                registerResultStatus[rd], registerResultStatus[rs1], registerResultStatus[
                                    rs2] = "not Available", "not Available", "not Available"
                                locks[rd] = "writingLock"
                                locks[rs1] = "writingLock"
                                locks[rs2] = "writingLock"
                                preIssueQueue.remove(preAlu3Queue)
                                issuedIn = "ALU3"

                    if operation in category3.values():
                        if operation == "lw":
                            rd, rs1, imm = int(
                                instruction[1][1:-1]), int(instruction[2][5:-1]), int(instruction[2][:3])

                            if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock":
                                # if rd in readingReg or rs1 in writingReg:
                                Available = False

                            if Available and len(preAlu1Queue) < 2 and issuedIn != "ALU1":
                                preAlu1Queue.append(
                                    f"{operation} x{rd}, {imm}(x{rs1})")
                                # registerResultStatus[rd], registerResultStatus[rs1] = "not Available", "not Available"
                                registerResultStatus[rd] = "not Available"
                                # registerResultStatus[rs1] = "not Available"
                                locks[rd] = "writingLock"
                                # locks[rs1] = "writingLock"
                                # if rs1 not in readingReg:
                                #     locks[rs1] = "writingLock"

                                preIssueQueue.remove(preAlu1Queue[0])
                                len(preAlu1Queue) > 1 and preIssueQueue.remove(
                                    preAlu1Queue[1])
                                issuedIn = "ALU1"
                        else:
                            rd, rs1, imm = int(
                                instruction[1][1:-1]), int(instruction[2][1:-1]), int(instruction[3][1:])

                            if operation == "addi":  # send to preAlu2 Queue after checking the registerResultStatus
                                if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock":
                                    # if rd in readingReg or rs1 in writingReg:
                                    Available = False

                                if Available and preAlu2Queue == "" and postAlu2Queue == "" and issuedIn != "ALU2":
                                    preAlu2Queue = f"{operation} x{rd}, x{rs1}, #{imm}"
                                    registerResultStatus[rd] = "not Available"
                                    registerResultStatus[rs1] = "not Available"
                                    locks[rd] = "writingLock"
                                    locks[rs1] = "writingLock"
                                    preIssueQueue.remove(preAlu2Queue)
                                    issuedIn = "ALU2"

                            else:  # send to preAlu3 Queue after checking the registerResultStatus
                                if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock":
                                    # if rd in readingReg or rs1 in writingReg:
                                    Available = False

                                if Available and preAlu3Queue == "" and postAlu3Queue == "" and issuedIn != "ALU3":
                                    preAlu3Queue = f"{operation} x{rd}, x{rs1}, #{imm}"
                                    registerResultStatus[rd] = "not Available"
                                    registerResultStatus[rs1] = "not Available"
                                    locks[rd] = "writingLock"
                                    locks[rs1] = "writingLock"
                                    preIssueQueue.remove(preAlu3Queue)
                                    issuedIn = "ALU3"

                else:

                    if operation == "sw":
                        rs1, rs2, offset = int(instruction[1][1:-1]), int(
                            instruction[2][5:-1]), int(instruction[2][0:3])

                        if registerResultStatus[rs1] == "not Available" or registerResultStatus[rs2] == "not Available" or locks[rs2] == "writingLock" or locks[rs1] == "writingLock":
                            # if rd in readingReg or rs1 in writingReg:
                            Available = False

                        if Available and len(preAlu1Queue) < 2 and issuedIn != "ALU1":
                            preAlu1Queue.append(
                                f"{operation} x{rs1}, {offset}(x{rs2})")
                            # registerResultStatus[rd], registerResultStatus[rs1] = "not Available", "not Available"
                            registerResultStatus[rs1], registerResultStatus[rs2] = "not Available", "not Available"
                            locks[rs1], locks[rs2] = "writingLock", "writingLock"
                            # if rs1 not in readingReg:
                            #     locks[rs1] = "writingLock"
                            preIssueQueue.remove(preAlu1Queue[0])
                            len([preAlu1Queue]) > 1 and preIssueQueue.remove(
                                preAlu1Queue[1])
                            issuedIn = "ALU1"

                    if operation in category2.values():
                        rd, rs1, rs2 = int(
                            instruction[1][1:-1]), int(instruction[2][1:-1]), int(instruction[3][1:])

                        # send to preAlu2 Queue after checking the registerResultStatus
                        if operation == "add" or operation == "sub":
                            if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or registerResultStatus[rs2] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock" or locks[rs2] == "writingLock" or rd in readingReg or rs1 in writingReg or rs2 in writingReg:
                                # if rd in readingReg or rs1 in writingReg or rs2 in writingReg:
                                Available = False

                            if Available and preAlu2Queue == "" and postAlu2Queue == "" and issuedIn != "ALU2":
                                preAlu2Queue = f"{operation} x{rd}, x{rs1}, x{rs2}"
                                registerResultStatus[rd], registerResultStatus[rs1], registerResultStatus[
                                    rs2] = "not Available", "not Available", "not Available"
                                locks[rd] = "writingLock"
                                locks[rs1] = "writingLock"
                                locks[rs2] = "writingLock"
                                preIssueQueue.remove(preAlu2Queue)
                                issuedIn = "ALU2"
                        # send to preAlu3 (for and or instructions) Queue after checking the registerResultStatus
                        else:
                            if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or registerResultStatus[rs2] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock" or locks[rs2] == "writingLock" or rd in readingReg or rs1 in writingReg or rs2 in writingReg:
                                # if rd in readingReg or rs1 in writingReg or rs2 in writingReg:
                                Available = False

                            if Available and preAlu3Queue == "" and postAlu3Queue == "" and issuedIn != "ALU3":
                                preAlu3Queue = f"{operation} x{rd}, x{rs1}, x{rs2}"
                                registerResultStatus[rd], registerResultStatus[rs1], registerResultStatus[
                                    rs2] = "not Available", "not Available", "not Available"
                                locks[rd] = "writingLock"
                                locks[rs1] = "writingLock"
                                locks[rs2] = "writingLock"
                                preIssueQueue.remove(preAlu3Queue)
                                issuedIn = "ALU3"

                    if operation in category3.values():
                        if operation == "lw":
                            rd, rs1, imm = int(
                                instruction[1][1:-1]), int(instruction[2][5:-1]), int(instruction[2][:3])

                            if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock":
                                # if rd in readingReg or rs1 in writingReg:
                                Available = False

                            if Available and len(preAlu1Queue) < 2 and issuedIn != "ALU1":
                                preAlu1Queue.append(
                                    f"{operation} x{rd}, {imm}(x{rs1})")
                                # registerResultStatus[rd], registerResultStatus[rs1] = "not Available", "not Available"
                                registerResultStatus[rd] = "not Available"
                                # registerResultStatus[rs1] = "not Available"
                                locks[rd] = "writingLock"
                                # locks[rs1] = "writingLock"
                                # if rs1 not in readingReg:
                                #     locks[rs1] = "writingLock"

                                preIssueQueue.remove(preAlu1Queue[0])
                                len(preAlu1Queue) > 1 and preIssueQueue.remove(
                                    preAlu1Queue[1])
                                issuedIn = "ALU1"
                        else:
                            rd, rs1, imm = int(
                                instruction[1][1:-1]), int(instruction[2][1:-1]), int(instruction[3][1:])

                            if operation == "addi":  # send to preAlu2 Queue after checking the registerResultStatus
                                if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock":
                                    # if rd in readingReg or rs1 in writingReg:
                                    Available = False

                                if Available and preAlu2Queue == "" and postAlu2Queue == "" and issuedIn != "ALU2":
                                    preAlu2Queue = f"{operation} x{rd}, x{rs1}, #{imm}"
                                    registerResultStatus[rd] = "not Available"
                                    registerResultStatus[rs1] = "not Available"
                                    locks[rd] = "writingLock"
                                    locks[rs1] = "writingLock"
                                    preIssueQueue.remove(preAlu2Queue)
                                    issuedIn = "ALU2"

                            else:  # send to preAlu3 Queue after checking the registerResultStatus
                                if registerResultStatus[rd] == "not Available" or registerResultStatus[rs1] == "not Available" or locks[rd] == "writingLock" or locks[rs1] == "writingLock":
                                    # if rd in readingReg or rs1 in writingReg:
                                    Available = False

                                if Available and preAlu3Queue == "" and postAlu3Queue == "" and issuedIn != "ALU3":
                                    preAlu3Queue = f"{operation} x{rd}, x{rs1}, #{imm}"
                                    registerResultStatus[rd] = "not Available"
                                    registerResultStatus[rs1] = "not Available"
                                    locks[rd] = "writingLock"
                                    locks[rs1] = "writingLock"
                                    preIssueQueue.remove(preAlu3Queue)
                                    issuedIn = "ALU3"

                instInd += 1

            issuedIn = ""

            # Fetching Instruction
            if iF["waiting"] == "" and iF["executed"] == "" and preIssueFullHalt == False:
                # if len(preIssueQueue) < 4:
                while clock < 2:
                    instructionArr = registerIns[i].split(" ")
                    operation = instructionArr[0]

                    if operation in category1.values():
                        rs1, rs2, offset = int(instructionArr[1]), int(
                            instructionArr[2]), int(instructionArr[3])
                        if operation == "sw":
                            if len(preIssueQueue) < 4:
                                activeRegisters[rs1] = "active"
                                activeRegisters[rs2] = "active"
                                locks[rs1] = "readingLock"
                                locks[rs2] = "readingLock"
                                readingReg.append(rs1)
                                readingReg.append(rs2)
                                preIssueQueue.append(
                                    f"{operation} x{rs1}, {offset}(x{rs2})")
                        else:
                            if activeRegisters[rs1] == "not active" and activeRegisters[rs2] == "not active" and registerResultStatus[rs1] == "Available" and registerResultStatus[rs2] == "Available":

                                if operation == "beq":
                                    if registerData[rs1] == registerData[rs2]:
                                        offset = offset << 1
                                        i += offset - 4
                                if operation == "bne":
                                    if registerData[rs1] != registerData[rs2]:
                                        offset = offset << 1
                                        i += offset - 4
                                if operation == "blt":
                                    if registerData[rs1] < registerData[rs2]:
                                        offset = offset << 1
                                        i += offset - 4

                                iF["executed"] = f"{operation} x{rs1}, x{rs2}, #{offset}"
                            else:
                                iF["waiting"] = f"{operation} x{rs1}, x{rs2}, #{offset}"

                            clock = 2

                    elif operation in category2.values():
                        rd, rs1, rs2 = int(instructionArr[1]), int(
                            instructionArr[2]), int(instructionArr[3])

                        if len(preIssueQueue) < 4:
                            activeRegisters[rd] = "active"
                            activeRegisters[rs1] = "active"
                            activeRegisters[rs2] = "active"
                            locks[rd] = "readingLock"
                            locks[rs1] = "readingLock"
                            locks[rs2] = "readingLock"
                            writingReg.append(rd)
                            readingReg.append(rs1)
                            readingReg.append(rs2)
                            preIssueQueue.append(
                                f"{operation} x{rd}, x{rs1}, x{rs2}")

                    elif operation in category3.values():
                        rd, rs1, imm = int(instructionArr[1]), int(
                            instructionArr[2]), int(instructionArr[3])

                        if operation == "lw":
                            if len(preIssueQueue) < 4:
                                activeRegisters[rd] = "active"
                                activeRegisters[rs1] = "active"
                                locks[rd] = "readingLock"
                                locks[rs1] = "readingLock"
                                writingReg.append(rd)
                                readingReg.append(rs1)
                                preIssueQueue.append(
                                    f"{operation} x{rd}, {imm}(x{rs1})")
                        else:
                            if len(preIssueQueue) < 4:
                                activeRegisters[rd] = "active"
                                activeRegisters[rs1] = "active"
                                locks[rd] = "readingLock"
                                locks[rs1] = "readingLock"
                                writingReg.append(rd)
                                readingReg.append(rs1)
                                preIssueQueue.append(
                                    f"{operation} x{rd}, x{rs1}, #{imm}")

                    elif operation in category4.values():
                        if operation == "jal":
                            rd, offset = int(instructionArr[1]), int(
                                instructionArr[2])

                            if activeRegisters[rd] == "not active" and registerResultStatus[rd] == "Available":
                                registerData[rd] = i+4
                                i += (offset << 1)-4
                                iF["executed"] = f"{operation} x{rd}, #{offset}"
                            else:
                                iF["waiting"] = f"{operation} x{rd}, #{offset}"
                            clock = 2

                        if operation == "break":
                            encountered = True
                            iF["executed"] = f"break"
                            break

                    i += 4
                    clock += 1

        # Writing IF Unit to the file
        simulation.write(
            f"IF Unit:\n\tWaiting: {('['+iF['waiting']+']') if iF['waiting'] != '' else ''}\n\tExecuted: {('['+iF['executed']+']') if iF['executed'] != '' else ''}\n")

        # Writing Pre-Issue Queue to the file
        simulation.write(
            f"Pre-Issue Queue:\n\tEntry 0: {('['+preIssueQueue[0]+']') if len(preIssueQueue) > 0 else ''}\n\tEntry 1: {('['+preIssueQueue[1]+']') if len(preIssueQueue) > 1 else ''}\n\tEntry 2: {('['+preIssueQueue[2]+']') if len(preIssueQueue) > 2 else ''}\n\tEntry 3: {('['+preIssueQueue[3]+']') if len(preIssueQueue) == 4 else ''}\n")

        # Writing ALU To the file:
        simulation.write(
            f"Pre-ALU1 Queue:\n\tEntry 0: {('['+preAlu1Queue[0]+']') if len(preAlu1Queue) > 0 else ''}\n\tEntry 1: {('['+preAlu1Queue[1]+']') if len(preAlu1Queue) > 1 else ''}\n"
        )
        simulation.write(
            f"Pre-MEM Queue: {('['+preMEMQueue+']') if preMEMQueue != '' else ''}\nPost-MEM Queue: {('['+postMEMQueue+']') if postMEMQueue != '' else ''}\n"
        )
        simulation.write(
            f"Pre-ALU2 Queue: {('['+preAlu2Queue+']') if preAlu2Queue != '' else ''}\nPost-ALU2 Queue: {('['+postAlu2Queue+']') if postAlu2Queue != '' else ''}\n"
        )
        simulation.write(
            f"Pre-ALU3 Queue: {('['+preAlu3Queue+']') if preAlu3Queue != '' else ''}\nPost-ALU3 Queue: {('['+postAlu3Queue+']') if postAlu3Queue != '' else ''}\n"
        )

        # Writing Registers to the file
        simulation.write(
            f'\nRegisters\nx00:\t{registerData[0]}\t{registerData[1]}\t{registerData[2]}\t{registerData[3]}\t{registerData[4]}\t{registerData[5]}\t{registerData[6]}\t{registerData[7]}\nx08:\t{registerData[8]}\t{registerData[9]}\t{registerData[10]}\t{registerData[11]}\t{registerData[12]}\t{registerData[13]}\t{registerData[14]}\t{registerData[15]}\nx16:\t{registerData[16]}\t{registerData[17]}\t{registerData[18]}\t{registerData[19]}\t{registerData[20]}\t{registerData[21]}\t{registerData[22]}\t{registerData[23]}\nx24:\t{registerData[24]}\t{registerData[25]}\t{registerData[26]}\t{registerData[27]}\t{registerData[28]}\t{registerData[29]}\t{registerData[30]}\t{registerData[31]}\n'
        )

    # Writing Data to the file
    simulation.write(f"Data\n")

    j, k = 0, 0
    registers = list(memoryData.keys())
    simulation.write(f"{registers[0]}:\t")
    while j < len(registers):
        # if j > 0 and (j == 7 or j % 7 == 0):
        simulation.write(
            f"{memoryData[registers[j]]}")

        if j+1 < len(registers) and (j+1) % 8 == 0:
            simulation.write(f"\n{registers[j+1]}:\t")
        elif j+1 < len(registers):
            simulation.write(f"\t")
        # if j > 0 and j % 8 == 0:
        #     simulation.write(f"\n{registers[k]}:\t{registerVals[j]}")
        # else:
        #     simulation.write(f"{registerVals[j]}\t")

        j += 1
        k += 1

    cycle += 1
