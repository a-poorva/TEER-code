data = open("voltagevalues.txt", "r")
lines = data.readlines()
print(lines)
text_file.close()


for line in lines:
    print(line)
