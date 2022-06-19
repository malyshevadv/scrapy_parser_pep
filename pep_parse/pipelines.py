import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_counter = defaultdict(int)

    def process_item(self, item, spider):
        item_status = item['status']
        self.status_counter[item_status] = self.status_counter.get(
            item_status, 0
        ) + 1
        return item

    def close_spider(self, spider):
        results = [('Статус', 'Количество')]
        results.extend(self.status_counter.items())
        results.append(('Total', sum(self.status_counter.values())))
        path_to_file = BASE_DIR / 'results'
        date_for_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fullfilename = path_to_file / f'status_summary_{date_for_file}.csv'
        with open(fullfilename, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(results)
