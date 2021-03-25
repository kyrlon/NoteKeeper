import gkeepapi
import keyring
import json
token = kee
with open("cred.json",) as cred:
    credentials = json.load(cred)
keep = gkeepapi.Keep()
keep.login(credentials["email"], credentials["password"])

note = gkeepapi.createNote('Todo', 'Eat breakfast')
note.pinned = True
note.color = gkeepapi.node.ColorValue.Red

keep.sync()

print(note.title)
print(note.text)