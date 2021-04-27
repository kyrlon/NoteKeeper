import gkeepapi
#import keyring
import json
import getpass
from collections import defaultdict

with open("credz/cred.json",) as cred:
    config = json.load(cred)
keep = gkeepapi.Keep()
example = keep.login(config["username"], config["password"])
token = keep.getMasterToken()

keep.sync()



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
            broken_dashes.append(new_entry)
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
    keep.sync()

def g_keep_backup():
    backup_dict = dict()
    for num,shopping_item in enumerate(Groceries.items):
        backup_dict[str(num)] = [shopping_item.checked, shopping_item.text]
    with open("backup_json.txt", "w") as file_t:
        file_t.write(json.dumps(backup_dict, sort_keys=True, indent=4))
    
    #Human Readable
    with open("human_readable.txt", "w", encoding='utf-8') as f:
        f.write(Groceries.text)

def g_keep_restore():
    gnote = keep.createList('Title')
    gnote.delete()
    with open("backup_json.txt","r") as f:
        data = json.load(f)
    #print(data)
    gnote = keep.createList('Title')
    for key, value in enumerate(data.items()):
        _, food_item = value
        gnote.add(food_item[1],food_item[0])
    print(1)

class GoogleKeepLog:
    def __init__(self):
        self.Groceries_list = None
        self.Merchandise_list = None
        self.g_keep_login()

    
    def g_keep_check_loop(self):
        while True:
            self.fix_list(self.Groceries_list)
            self.fix_list(self.Merchandise_list)
            self.g_keep_backup
            self.g_keep_restore()

    def g_keep_login(self):
        with open("credz/cred.json",) as cred:
            config = json.load(cred)
        self.keep = gkeepapi.Keep()
        example = self.keep.login(config["username"], config["password"])
        token = self.keep.getMasterToken()
        self.Merchandise_list = keep.get("1R4lilvk5kmHpNIMqQG5Go3FYnWr5Gk_mslkJ2IzamZpnl6W8_mW4IBdsqZnW3OIvpl7Q")
        self.Groceries_list = keep.get("1Y_H6kCujK2r0NfhBK7tlQGPON8iMXqW3Pi7ot4BB0jT2vz0Ti_SGhdZIm2QBPTxKw705RWK2Mg")
        self.keep.sync()



    def fix_list(self, store_incremental_lists):
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
                broken_dashes.append(new_entry)
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
        keep.sync()

    def g_keep_backup(self):
        backup_note_list = list()
        if self.Groceries_list:
            backup_note_list.append(self.Groceries_list)
        if self.Merchandise_list:
            backup_note_list.append(self.Merchandise_list)
        for B_checklist in backup_note_list:
            backup_dict = dict()
            note_name = B_checklist.title
            for num,shopping_item in enumerate(B_checklist.items):
                backup_dict[str(num)] = [shopping_item.checked, shopping_item.text]
            with open(note_name + "_json.txt", "w") as file_t:
                file_t.write(json.dumps(backup_dict, sort_keys=True, indent=4))
            
            #Human Readable
            with open(note_name + ".txt", "w", encoding='utf-8') as f:
                f.write(B_checklist.text)

    def g_keep_restore(self):
        #method to search notes
        ###################

        if "Groceries" in some_search_method:
            pass
        else:
            gnote = keep.createList('Title')
            gnote.delete()
            with open("backup_json.txt","r") as f:
                data = json.load(f)
            #print(data)
            gnote = keep.createList('Title')
            for key, value in enumerate(data.items()):
                _, food_item = value
                gnote.add(food_item[1],food_item[0])
            print(1)
        if "Merchandise" in some_search_method:
            pass         
        else:
            gnote = keep.createList('Title')
            gnote.delete()
            with open("backup_json.txt","r") as f:
                data = json.load(f)
            #print(data)
            gnote = keep.createList('Title')
            for key, value in enumerate(data.items()):
                _, food_item = value
                gnote.add(food_item[1],food_item[0])
            print(1)

    def g_keep_search(self):
        pass

    


if __name__ == "__main__":
    #fix_list(Groceries)
    #g_keep_backup()
    #g_keep_restore()
    ex = GoogleKeepLog()
    ex.fix_list(ex.Groceries_list)
    ex.fix_list(ex.Merchandise_list)
    ex.g_keep_backup()
    print(2)
    