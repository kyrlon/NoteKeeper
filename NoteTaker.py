import gkeepapi
import keyring
import json
import getpass

#token = kee
#with open("cred.json",) as cred:
#credentials = json.load(cred)
config = dict()
config["username"] =#input("email: ")
config["password"] = #getpass.getpass("password: ")
keep = gkeepapi.Keep()
example = keep.login(config["username"], config["password"])
token = keep.getMasterToken()
#keyring.set_password("google-keep-token",username, token)
""" 
logged_in = False
if not logged_in and token:
    logger.info("Authenticating with token")
    state = util.load(args.config_dir, config["username"])

    try:
        keep.resume(config["username"], token, state=state, sync=False)
        logged_in = True
        logger.info("Success")
    except gkeepapi.exception.LoginException:
        print(8)


if logged_in:
    password = getpass.getpass()
    try:
        keep.login(config["username"], password, sync=False)
        logged_in = True
        del password
        token = keep.getMasterToken()
        keyring.set_password("google-keep-token", config["username"], token)
        #logger.info("Success")
    except gkeepapi.exception.LoginException:
        pass """
note = keep.createNote('Todo', 'Eat breakfast')
note.pinned = True
note.color = gkeepapi.node.ColorValue.Red

keep.sync()

print(note.title)
print(note.text)

Merchandise = keep.get("1R4lilvk5kmHpNIMqQG5Go3FYnWr5Gk_mslkJ2IzamZpnl6W8_mW4IBdsqZnW3OIvpl7Q")
Groceries = keep.get("1Y_H6kCujK2r0NfhBK7tlQGPON8iMXqW3Pi7ot4BB0jT2vz0Ti_SGhdZIm2QBPTxKw705RWK2Mg")