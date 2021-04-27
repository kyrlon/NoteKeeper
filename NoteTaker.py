import gkeepapi
import json, time
import getpass
from collections import defaultdict


class GoogleKeepLog:
    def __init__(self):
        self.Groceries_list = None
        self.Merchandise_list = None
        self.note_search_collection = dict()
        self.g_keep_login()

    
    def g_keep_check_loop(self):
        while True:
            self.fix_list(self.Groceries_list)
            self.fix_list(self.Merchandise_list)
            self.g_keep_backup()
            print("waiting....")
            time.sleep(30)
            self.g_keep_restore()

    def g_keep_login(self):
        with open("credz/cred.json",) as cred:
            config = json.load(cred)
        self.keep = gkeepapi.Keep()
        example = self.keep.login(config["username"], config["password"])
        token = self.keep.getMasterToken()
        self.g_keep_search()
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
        self.g_keep_search()
        dropping_groceries = "del G"
        dropping_merchandise = "del M"
        if any("Groceries" in stuff for stuff in self.note_search_collection.keys()):
            if any(dropping_groceries in stuff for stuff in self.note_search_collection.keys()) and self.Groceries_list:
                self.Groceries_list.trash()
                self.keep.sync()
                with open("Groceries_json.txt","r") as f:
                    data = json.load(f)
                gnote = self.keep.createList('Groceries')
                for key, value in enumerate(data.items()):
                    _, food_item = value
                    gnote.add(food_item[1],food_item[0])
                gnote.pinned = True
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
            self.keep.sync()
        
        if any("Merchandise" in stuff for stuff in self.note_search_collection.keys()):
            if any(dropping_merchandise) and self.Merchandise_list:
                self.Merchandise_list.trash()
                self.keep.sync()
                with open("Merchandise (Misc., etc.)_json.txt","r") as f:
                    data = json.load(f)
                gnote = self.keep.createList('Merchandise (Misc., etc.)')
                for key, value in enumerate(data.items()):
                    _, food_item = value
                    gnote.add(food_item[1],food_item[0])
                gnote.pinned = True
                self.keep.sync()   
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
            self.keep.sync()

    def g_keep_search(self):
        search_list = list(self.keep.find(pinned=True))
        for note in search_list:
            self.note_search_collection[note.title] = note.id
        self.Merchandise_list = self.keep.get(self.__dict_key_from_str("Merchandise", self.note_search_collection))
        self.Groceries_list = self.keep.get(self.__dict_key_from_str("Groceries", self.note_search_collection))

    def __dict_key_from_str(self, p_string, p_dict):
        for key in p_dict:
            if p_string in key:
                return p_dict[key]


if __name__ == "__main__":
    #fix_list(Groceries)
    #g_keep_backup()
    #g_keep_restore()
    ex = GoogleKeepLog()
    ex.fix_list(ex.Groceries_list)
    ex.fix_list(ex.Merchandise_list)
    ex.g_keep_backup()
    print("waiting....")
    time.sleep(20)
    ex.g_keep_restore()
    print(2)
