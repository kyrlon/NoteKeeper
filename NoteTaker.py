#!/env/bin/python3

import gkeepapi
import json, time
import getpass
from collections import defaultdict


class GoogleKeepLog:
    def __init__(self, verbose=False):
        self.Groceries_list = None
        self.Merchandise_list = None
        self.note_search_collection = dict()
        self.g_keep_login()

    
    def g_keep_check_loop(self):
        n = 0
        while True:
            n+=1
            self.fix_list(self.Groceries_list)
            self.fix_list(self.Merchandise_list)
            self.g_keep_backup()
            print("waiting....")
            time.sleep(10)
            self.g_keep_restore()
            print("Loop %s done" % n)
        print("Done!")

    def g_keep_login(self):
        with open("credz/cred.json",) as cred:
            self.config = json.load(cred)
        self.keep = gkeepapi.Keep()
        example = self.keep.login(self.config["username"], self.config["password"])
        token = self.keep.getMasterToken()
        self.g_keep_search()
        self.keep.sync()



    def fix_list(self, store_incremental_lists):
        if not store_incremental_lists:
            self.g_keep_restore()
            print("Need to restore %s List" %store_incremental_lists)
            return 
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
        self.keep.sync()

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
        self.g_keep_search()
        dropping_groceries = "del G"
        dropping_merchandise = "del M"
        if any("Groceries" in stuff for stuff in self.note_search_collection.keys()):
            if any(dropping_groceries in stuff for stuff in self.note_search_collection.keys()) and self.Groceries_list:
                self.__clear_shopping_list(self.Groceries_list)
                with open("Groceries_json.txt","r") as f:
                    data = json.load(f)
                for key, value in enumerate(data.items()):
                    _, food_item = value
                    self.Groceries_list.add(food_item[1],food_item[0])
                self.Groceries_list.pinned = True
                indicator = self.keep.get(self.__dict_key_from_str(dropping_groceries, self.note_search_collection))
                indicator.trash()
                self.keep.sync()
        else:
            with open("Groceries_json.txt","r") as f:
                data = json.load(f)
            gnote = self.keep.createList('Groceries')
            for key, value in enumerate(data.items()):
                _, food_item = value
                gnote.add(food_item[1],food_item[0])
            gnote.pinned = True
            gnote.collaborators.add(self.config["sheabutterbaby"])
            self.keep.sync()
        
        if any("Merchandise" in stuff for stuff in self.note_search_collection.keys()):
            if any(dropping_merchandise in stuff for stuff in self.note_search_collection.keys()) and self.Merchandise_list:
                self.__clear_shopping_list(self.Merchandise_list)
                with open("Merchandise (Misc., etc.)_json.txt","r") as f:
                    data = json.load(f)
                for key, value in enumerate(data.items()):
                    _, food_item = value
                    self.Merchandise_list.add(food_item[1],food_item[0])
                self.Merchandise_list.pinned = True
                indicator = self.keep.get(self.__dict_key_from_str(dropping_merchandise, self.note_search_collection))
                indicator.trash()    
                self.keep.sync()
        else:
            with open("Merchandise (Misc., etc.)_json.txt","r") as f:
                data = json.load(f)
            gnote = self.keep.createList('Merchandise (Misc., etc.)')
            for key, value in enumerate(data.items()):
                _, food_item = value
                gnote.add(food_item[1],food_item[0])
            gnote.pinned = True
            gnote.collaborators.add(self.config["sheabutterbaby"])
            self.keep.sync()

    def g_keep_search(self):
        search_list = list(self.keep.find(pinned=True))
        self.note_search_collection = dict()
        for note in search_list:
            self.note_search_collection[note.title] = note.id
        self.Merchandise_list = self.keep.get(self.__dict_key_from_str("Merchandise", self.note_search_collection))
        self.Groceries_list = self.keep.get(self.__dict_key_from_str("Groceries", self.note_search_collection))

    def __dict_key_from_str(self, p_string, p_dict):
        for key in p_dict:
            if p_string in key:
                return p_dict[key]

    def __clear_shopping_list(self, store_incremental_lists):
        for num,shopping_item in enumerate(store_incremental_lists.items):
            shopping_item.delete()


if __name__ == "__main__":
    ex = GoogleKeepLog()
    ex.g_keep_check_loop()
