import requests

# 0dbc904a-ffe9-41c4-866c-7a66434972c1 is the uuid for 哈佛燕京 collection
# 750 is a random number for avoiding the limitation of pagination
resources = requests.get("https://rise.mpiwg-berlin.mpg.de/api/collections/0dbc904a-ffe9-41c4-866c-7a66434972c1/resources?per_page=750").json()

uuids = [ r['uuid'] for r in resources ]

# for bookId in uuids[:1]:   # for test only, observe first book.
for bookId in uuids:
      #fetch metadata of the book based on book id. metadata is not be collected well yet.
#     meta = requests.get("https://rise.mpiwg-berlin.mpg.de/api/resources/" + bookId + "/metadata").json()
#     print(meta)

    #fetch sections of the book based on book id.
    #only one section for each book of HYL collection right now, therefore hardcode first element of reponse result.
    section = requests.get("https://rise.mpiwg-berlin.mpg.de/api/resources/"+ bookId +"/sections").json()[0]

    #for avoiding pagination mechanism, get total pages first
    contentUnitCount = section['contentUnitCount']

    #get section id
    sectionId = section['uuid']

    #fetch text from RISE
    contents = requests.get("https://rise.mpiwg-berlin.mpg.de/api/sections/"+ sectionId +"/content_units?per_page=" + str(contentUnitCount) ).json()

    #put all text into a list
    texts = [c['content'] for c in contents]

    # save into a file.
    # the texts contain some special tags (such as <char> <tb> <ls> <pb>) that you need to deal with yourself.
    with open("/Users/calvinyeh/Workspaces/local-gazetteers/lang-model/all_text_ori/" + bookId + ".txt", "w+") as file:
             file.write('\n'.join(texts))

print('Done')
