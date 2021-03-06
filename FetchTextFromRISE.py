# -*- coding: utf-8 -*-
import requests
import os

# 6000 is a large number to make sure we get all the components of a collection. Please do note that RISE also has a pagination feature,
# which can be implemented by clients if they wish.
per_page = 6000

# getting the list of collections that the user has access to:
collections_response = requests.get(f'https://rise.mpiwg-berlin.mpg.de/api/collections?per_page={per_page}')

collections = collections_response.json()
# each accessible collections has a name, a uuid, and a number of resources.
# print(collections)
idx = 1
for collection in collections:
      print(f'collection at index: {idx}')
      idx += 1
      print(collection)

# picking a collection by its index
# collection_index = 1
# collection = collections[collection_index]

results = list(filter(lambda collection: collection['name'] == 'MPIWG - 哈佛燕京圖書館藏珍稀方志', collections))
collection = results[0]
print(collection['uuid'])
collection_uuid = collection['uuid']

# we grab all resources for this collection
resources_response = requests.get(f'https://rise.mpiwg-berlin.mpg.de/api/collections/{collection_uuid}/resources?per_page={per_page}')

corpus_path = './corpus'
if not os.path.exists(corpus_path):
      os.makedirs(corpus_path)

for resource in resources_response.json():
      uuid = resource['uuid']
      resource_name = resource['name']
      print(resource_name)

      if not os.path.exists(corpus_path + "/" + resource_name):
            os.makedirs(corpus_path + "/" + resource_name)
      sections = requests.get("https://rise.mpiwg-berlin.mpg.de/api/resources/"+ resource['uuid'] +"/sections")
      
      for section in sections.json():
            print(section)
            print(section['uuid'])
            section_name = section['name']
            section_path = corpus_path + "/" + resource_name + "/" + section_name
            file = open(section_path +".txt", "w") 
            content_units = requests.get("https://rise.mpiwg-berlin.mpg.de/api/sections/"+ section['uuid'] +"/content_units?per_page=6000")
            for content_unit in content_units.json():
                  print(content_unit)
                  file.write(content_unit['content']) 
            file.close()