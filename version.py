path = "version.txt"

with open(path, "r", encoding="utf-8") as f:
    content = f.read().strip()

print(content, end="")
