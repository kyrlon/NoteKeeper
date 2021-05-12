

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
from httplib2 import Http
from oauth2client import file, client, tools
import time, json
from tempfile import TemporaryDirectory
from pathlib import Path



class GoogleKeepDriveInterface:
    _temp_dir = TemporaryDirectory()
    SCOPES = ['https://www.googleapis.com/auth/drive', 
                    'https://www.googleapis.com/auth/drive.file', 
                    'https://www.googleapis.com/auth/drive.appdata',
                    'https://www.googleapis.com/auth/drive.metadata', 
                    'https://www.googleapis.com/auth/drive.activity']


    store = file.Storage('credz/storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credz/client.json', SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http())) #might have to be authorized???

    def __init__(self):
        
        self.gkeep_drive_dir_id = self.notekeeper_log()
        self.g_drive_folder_query()

    def notekeeper_log(self):
        #Check if NoteKeeper_log folder exists
        notekeeper_folder_metadata = {
            'name': 'NoteFolder',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        query = "name contains '{}' and mimeType='{}' and trashed=false".format(notekeeper_folder_metadata["name"],notekeeper_folder_metadata["mimeType"])
        notekeeper_response = self.DRIVE.files().list(q=query, pageSize=100, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute().get('files', [])
        if notekeeper_response.__len__() == 1 and notekeeper_response[0].get("name") == notekeeper_folder_metadata["name"]:
            notekeeper_folder_id = notekeeper_response[0].get("id")
        else:
            #creates NoteKeeper_log folder
            note_gfolder = self.DRIVE.files().create(body=notekeeper_folder_metadata,
                                            fields='id').execute()
            notekeeper_folder_id = note_gfolder.get('id')
        
        return notekeeper_folder_id

    def g_drive_folder_query(self):
        folder_query = "'%s' in parents" % self.gkeep_drive_dir_id 
        files_response = self.DRIVE.files().list(q=folder_query, pageSize=100, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute().get('files', [])
        self.file_names = dict()
        for log_file in files_response:
            self.file_names[log_file.get("name")] = log_file.get("id")

    def txt_backup(self, filename, data):
        #notekeeper_folder_id = notekeeper_log()
        #checks if json and humanreadable exists

        text_file_name = "test1"
        text_file_name = filename
        temp_txt_filepath = Path(self._temp_dir.name) / (str(time.time()) + 'human.txt')
        
        with open(str(temp_txt_filepath), "w", encoding='utf-8') as f:
            f.write(data)        

        #checks if the text.txt exists
        if text_file_name in list(self.file_names.keys()):
            file_id = self.file_names[text_file_name]
            media = MediaFileUpload(temp_txt_filepath,
                                    mimetype='text/plain',
                                    resumable=True)
            file = self.DRIVE.files().update(fileId=file_id,body=None,
                                                media_body=media).execute()
            #print('File ID: %s' % file.get('id'))

        else:
            file_metadata = {
                'name': text_file_name,
                'mimeType': 'application/vnd.google-apps.script',
                'parents':[self.gkeep_drive_dir_id]
            }
            media = MediaFileUpload(temp_txt_filepath,
                                    mimetype='text/plain',
                                    resumable=True)
            file = self.DRIVE.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
    
    def json_backup(self, filename, data):
        #checks if the json exists
        json_file_name = "jtest2"
        json_file_name = filename

        temp_json_filepath = str(Path(self._temp_dir.name) / (str(time.time())+'json.txt'))
        with open(str(temp_json_filepath),"w") as file_t:
            file_t.write(json.dumps(data, sort_keys=True, indent=4))
               
        if json_file_name in list(self.file_names.keys()):
            file_id = self.file_names[json_file_name]
            media = MediaFileUpload(temp_json_filepath,
                                    mimetype='text/plain',
                                    resumable=True)
            file = self.DRIVE.files().update(fileId=file_id,body=None,
                                                media_body=media).execute()

        else:
            file_metadata = {
                'name': json_file_name,
                'mimeType': 'application/vnd.google-apps.script',
                'parents':[self.gkeep_drive_dir_id]
            }
            media = MediaFileUpload(temp_json_filepath,
                                    mimetype='text/plain',
                                    resumable=True)
            file = self.DRIVE.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()



def blah():

    print(2)


    """ files = DRIVE.files().list().execute().get('files', [])
    for f in files:
        print(f['name'], f['mimeType']) """

    #checks if 


    #create file in that folder
    #folder_id_notes = note_gfolder.get('id')
    folder_id_notes = "1GWMxde9YSL3IirrcQ1Q7-MLBZdCxI8w9"
    file_metadata = {
        'name': 'My Report',
        'mimeType': 'application/vnd.google-apps.script',
        'parents':[folder_id_notes]
    }
    media = MediaFileUpload('human_readable.txt',
                            mimetype='text/plain',
                            resumable=True)
    file = DRIVE.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

    time.sleep(30)



    #update that same file later....
    file_id = file.get('id')
    media = MediaFileUpload('human_readable.txt',
                            mimetype='text/plain',
                            resumable=True)
    file = DRIVE.files().update(fileId=file_id,body=None,
                                        media_body=media).execute()
    print('File ID: %s' % file.get('id'))


def downloader():
    ###########################
    #download select file
    file_id = file.get("id")
    request = DRIVE.files().export_media(fileId=file_id,
                                                mimeType='text/plain')
    fh = io.FileIO("ex2.txt","wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    print(2)

if __name__ == "__main__":
    #notekeeper_log()
    #check_exist(55555)

    ex = GoogleKeepDriveInterface()

    string = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    d = {"abc": 123, "baby": "you know me"}
    ex.txt_backup("string", string)
    ex.json_backup("json_crap", d)