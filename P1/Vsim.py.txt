# On my honor, I have neither given nor received any unauthorized aid on this assignment.
import sys
import os

inputFileName = sys.argv[-1]

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

cycle, i, encountered = 1, 256, False
while encountered == False:
    simulation.write("\n--------------------\n")
    operation = ""

    if i in registerIns:
        instructionArr = registerIns[i].split(" ")
        operation = instructionArr[0]

        if operation in category1.values():
            rs1, rs2, offset = int(instructionArr[1]), int(
                instructionArr[2]), int(instructionArr[3])

            if operation == "beq":
                simulation.write(
                    f"Cycle {cycle}:\t{i}\t{operation} x{rs1}, x{rs2}, #{offset}\n")

                if registerData[rs1] == registerData[rs2]:
                    offset = int(offset) << 1
                    print(offset)
                    i += offset - 4
            elif operation == "bne":
                simulation.write(
                    f"Cycle {cycle}:\t{i}\t{operation} x{rs1}, x{rs2}, #{offset}\n")

                if registerData[rs1] != registerData[rs2]:
                    offset = int(offset) << 1
                    i += offset - 4
            elif operation == "blt":
                simulation.write(
                    f"Cycle {cycle}:\t{i}\t{operation} x{rs1}, x{rs2}, #{offset}\n")

                if registerData[rs1] < registerData[rs2]:
                    offset = int(offset) << 1
                    i += offset - 4
            elif operation == "sw":
                memoryData[offset+registerData[rs2]] = registerData[rs1]
                simulation.write(
                    f"Cycle {cycle}:\t{i}\t{operation} x{rs1}, {offset}(x{rs2})\n")

        if operation in category2.values():
            rd, rs1, rs2 = int(instructionArr[1]), int(
                instructionArr[2]), int(instructionArr[3])

            if operation == "add":
                registerData[rd] = registerData[rs1]+registerData[rs2]
            elif operation == "sub":
                registerData[rd] = registerData[rs1]-registerData[rs2]
            elif operation == "or":
                registerData[rd] = registerData[rs1] | registerData[rs2]
            elif operation == "and":
                registerData[rd] = registerData[rs1] & registerData[rs2]

            simulation.write(
                f"Cycle {cycle}:\t{i}\t{operation} x{rd}, x{rs1}, x{rs2}\n")

        if operation in category3.values():
            rd, rs1, immVal = int(instructionArr[1]), int(
                instructionArr[2]), int(instructionArr[3])

            if operation == "addi":
                registerData[rd] = registerData[rs1]+(immVal)
            elif operation == "andi":
                registerData[rd] = registerData[rs1] & (immVal)
            elif operation == "ori":
                registerData[rd] = registerData[rs1] | (immVal)
            elif operation == "sll":
                registerData[rd] = registerData[rs1] << immVal
            elif operation == "sra":
                registerData[rd] = registerData[rs1] >> immVal
            elif operation == "lw":
                registerData[rd] = memoryData[immVal+registerData[rs1]]
                simulation.write(
                    f"Cycle {cycle}:\t{i}\t{operation} x{rd}, {immVal}(x{rs1})\n")

            if operation != "lw":
                simulation.write(
                    f"Cycle {cycle}:\t{i}\t{operation} x{rd}, x{rs1}, #{immVal}\n")

        if operation in category4.values():

            if operation == "jal":
                rd, immVal = int(instructionArr[1]), int(
                    instructionArr[2])
                simulation.write(
                    f"Cycle {cycle}:\t{i}\t{operation} x{rd}, #{immVal}\n"
                )
                registerData[rd] = i+4
                i += (immVal << 1)-4

            if operation == "break":
                simulation.write(
                    f"Cycle {cycle}:\t{i}\tbreak\n"
                )
                encountered = True

    simulation.write(
        f'Registers\nx00:\t{registerData[0]}\t{registerData[1]}\t{registerData[2]}\t{registerData[3]}\t{registerData[4]}\t{registerData[5]}\t{registerData[6]}\t{registerData[7]}\nx08:\t{registerData[8]}\t{registerData[9]}\t{registerData[10]}\t{registerData[11]}\t{registerData[12]}\t{registerData[13]}\t{registerData[14]}\t{registerData[15]}\nx16:\t{registerData[16]}\t{registerData[17]}\t{registerData[18]}\t{registerData[19]}\t{registerData[20]}\t{registerData[21]}\t{registerData[22]}\t{registerData[23]}\nx24:\t{registerData[24]}\t{registerData[25]}\t{registerData[26]}\t{registerData[27]}\t{registerData[28]}\t{registerData[29]}\t{registerData[30]}\t{registerData[31]}\nData\n'
    )

    j, k = 0, 0
    registers = list(memoryData.keys())
    simulation.write(f"{registers[0]}:\t")
    while j < len(registers):
        if j > 0 and (j == 7 or j % 7 == 0):
            simulation.write(
                f"{memoryData[registers[j]]}\n{registers[j+1]}:\t")
        else:
            if j+1 == len(registers):
                simulation.write(f"{memoryData[registers[j]]}")
            else:
                simulation.write(f"{memoryData[registers[j]]}\t")
        # if j > 0 and j % 8 == 0:
        #     simulation.write(f"\n{registers[k]}:\t{registerVals[j]}")
        # else:
        #     simulation.write(f"{registerVals[j]}\t")

        j += 1
        k += 1

    cycle += 1
    i += 4

    if encountered:
        break

# simulation.seek(0)
# lines = simulation.readlines()
# lines.pop(0)
# simulation.close()
# disassembly.close()
# os.remove("./sample_simulation1.txt")
# simulation = open("./sample_simulation1.txt", "w+")
# simulation.writelines(lines)
# simulation.close()
