

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
from httplib2 import Http
from oauth2client import file, client, tools
import time

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
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))



#Check if NoteKeeper_log folder exists
notekeeper_folder_metadata = {
    'name': 'NoteFolder',
    'mimeType': 'application/vnd.google-apps.folder'
}
query = "name contains '{}' and mimeType='{}' and trashed=false".format(notekeeper_folder_metadata["name"],notekeeper_folder_metadata["mimeType"])
notekeeper_response = DRIVE.files().list(q=query, pageSize=100, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute().get('files', [])
if notekeeper_response.__len__() == 1 and notekeeper_response[0].get("name") == notekeeper_folder_metadata["name"]:
    notekeeper_folder_id = notekeeper_response[0].get("id")
else:
    #creates NoteKeeper_log folder
    note_gfolder = DRIVE.files().create(body=notekeeper_folder_metadata,
                                    fields='id').execute()
    notekeeper_folder_id = note_gfolder.get('id')

#checks if json and humanreadable exists

text_file_name = "test1"
json_file_name = "jtest2"
folder_query = "'%s' in parents" % notekeeper_folder_id 
files_response = DRIVE.files().list(q=folder_query, pageSize=100, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute().get('files', [])
file_names = dict()
for log_file in files_response:
    file_names[log_file.get("name")] = log_file.get("id")

#checks if the text.txt exists
if text_file_name in list(file_names.keys()):
    file_id = file_names[text_file_name]
    media = MediaFileUpload('human_readable.txt',
                            mimetype='text/plain',
                            resumable=True)
    file = DRIVE.files().update(fileId=file_id,body=None,
                                        media_body=media).execute()
    #print('File ID: %s' % file.get('id'))

else:
    file_metadata = {
        'name': text_file_name,
        'mimeType': 'application/vnd.google-apps.script',
        'parents':[notekeeper_folder_id]
    }
    media = MediaFileUpload('human_readable.txt',
                            mimetype='text/plain',
                            resumable=True)
    file = DRIVE.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
#checks if the json exists
if json_file_name in list(file_names.keys()):
    file_id = file_names[json_file_name]
    media = MediaFileUpload('human_readable.txt',
                            mimetype='text/plain',
                            resumable=True)
    file = DRIVE.files().update(fileId=file_id,body=None,
                                        media_body=media).execute()

else:
    file_metadata = {
        'name': json_file_name,
        'mimeType': 'application/vnd.google-apps.script',
        'parents':[notekeeper_folder_id]
    }
    media = MediaFileUpload('human_readable.txt',
                            mimetype='text/plain',
                            resumable=True)
    file = DRIVE.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()




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
    pass