import threading
import script
import time

# examples of real requests
# url = 'http://kristall.by/catalog/goods_loader?cat_id=2&offset=40&limit=20&'
# url = 'http://kristall.by/catalog/goods_loader?cat_id=25&offset=40&limit=20&'

url = 'http://kristall.by/catalog/goods_loader'

if __name__ == '__main__':
    begin_list = 0
    len_list = 100
    catalog_id = 28

    params = {
        'cat_id': catalog_id,
        'offset': begin_list,
        'limit': len_list,
    }

    time_start = time.time()
    # get list items to scrape
    list_items = script.get_list_items(url, params)
    print("Items", len(list_items))
    data = []
    threads = []
    # Each item we sent to a thread with index for sort them after getting all data
    for i in range(len(list_items)):
        t = threading.Thread(target=script.generate_desc, args=[list_items[i], i, data, 'Обручальные кольца'])

        t.start()
        if ((i % 8) == 0) and i != 0:
            print(i, 'sleep')
            time.sleep(0.8)
        threads.append(t)

    # join to each thread because we need to all threads ended before going to the next step
    for t in threads:
        t.join()

    data.sort(key=lambda row: row[0])
    # print(data)
    print(f'Time {time.time() - time_start}')

    script.prnt_to_csv(data, filename='ignore/_wedding_rings.csv')
