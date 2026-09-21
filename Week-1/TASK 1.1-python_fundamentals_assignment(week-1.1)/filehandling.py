# file_handling.py
with open("unknownfile.txt", "w") as file:
    file.write("adventure \nmountain \nRainfall\n")

with open("unknownfile.txt", "r") as file:
    content = file.read()
    print("File Content:\n", content)
