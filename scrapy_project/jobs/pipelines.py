import json
import os

class JobsPipeline:
    def open_spider(self, spider):
        os.makedirs('../../data/final', exist_ok=True)
        self.file = open('../../data/final/jobs.json', 'w')
        self.file.write('[\n')
        self.first_item = True
    
    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()
    
    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        else:
            self.first_item = False
        
        line = json.dumps(dict(item), indent=4)
        self.file.write(line)
        return item