import requests
import os

# 0dbc904a-ffe9-41c4-866c-7a66434972c1 is the uuid for 哈佛燕京 collection
# 750 is a random number for avoiding the limitation of pagination
resources = requests.get("https://rise.mpiwg-berlin.mpg.de/api/collections/d8008b85-c4f1-47c8-9f4e-3c02c510307b/resources?per_page=6000")

corpus_path = './corpus'
if not os.path.exists(corpus_path):
      os.makedirs(corpus_path)

for resource in resources.json():
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