import gkeepapi
import keyring
import json
import getpass
from collections import defaultdict

with open("cred.json",) as cred:
    config = json.load(cred)
#config = dict()
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
#note = keep.createNote('Todo', 'Eat breakfast')
#note.pinned = True
#note.color = gkeepapi.node.ColorValue.Red

keep.sync()

#print(note.title)
#print(note.text)

Merchandise = keep.get("1R4lilvk5kmHpNIMqQG5Go3FYnWr5Gk_mslkJ2IzamZpnl6W8_mW4IBdsqZnW3OIvpl7Q")
Groceries = keep.get("1Y_H6kCujK2r0NfhBK7tlQGPON8iMXqW3Pi7ot4BB0jT2vz0Ti_SGhdZIm2QBPTxKw705RWK2Mg")


def fix_list(store_incremental_lists):
    num_on_shopping_list = 0
    shopping_list_dict = defaultdict(list)
    for num,shopping_item in enumerate(store_incremental_lists.unchecked):
        if shopping_item.text.startswith("-"):
            shopping_list_dict[num_on_shopping_list].append(num)
        else:
            num_on_shopping_list = num
    if shopping_list_dict:
        broken_dashes = list()
        for key, values in shopping_list_dict.items():
            new_entry = store_incremental_lists.unchecked[key].text
            broken_dashes.append(store_incremental_lists.unchecked[key].text)
            for i, vxx in enumerate(values):
                new_entry = new_entry + "\n"+ store_incremental_lists.unchecked[vxx].text
                broken_dashes.append(store_incremental_lists.unchecked[vxx].text)
        flag = True
        while flag:
            for i, val in enumerate(store_incremental_lists.unchecked):
                if not broken_dashes:
                    flag = False
                if val.text in broken_dashes:
                    store_incremental_lists.unchecked[i].delete()
                    broken_dashes.remove(val.text)
                    break
        store_incremental_lists.add(new_entry, False)
    #keep.sync()

def g_keep_backup():
    backup_dict = dict()
    for num,shopping_item in enumerate(Groceries.items):
        backup_dict[str(num)] = [shopping_item.checked, shopping_item.text]
    with open("backup_.txt", "w") as file_t:
        file_t.write(json.dumps(backup_dict, sort_keys=True, indent=4))
    
    #Human Readable
    with open("human_readable.txt", "w") as back_up:
        back_up.write(Groceries.text)

def g_keep_restore():
    pass


if __name__ == "__main__":
    fix_list(Groceries)