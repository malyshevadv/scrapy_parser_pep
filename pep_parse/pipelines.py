import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counter = defaultdict(int)
        self.total = 0
    
    def process_item(self, item, spider):
        item_status = item['status']
        self.status_counter[item_status] = self.status_counter.get(item_status, 0) + 1
        self.total += 1
        return item

    def close_spider(self, spider):
        results = [('Статус', 'Количество')]
        results.extend(self.status_counter.items())
        results.append(('Total', self.total))
        filename = Path(__file__).parent.parent / 'results' / f'status_summary_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
        with open(filename, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(results)