import difflib
import filecmp

file1 = "sample_simulation.txt"
file2 = "simulation.txt"

# Check if the two files are identical
are_identical = filecmp.cmp(file1, file2)

if are_identical:
    print("The files are identical.")
else:
    print("The files are not identical.")

print(are_identical)


with open(file1, 'r') as file1, open(file2, 'r') as file2:
    file1_lines = file1.readlines()
    file2_lines = file2.readlines()

# Calculate the differences between the two files
differ = difflib.Differ()
diff = list(differ.compare(file1_lines, file2_lines))

# Print the differences
for line in diff:
    print(line)
