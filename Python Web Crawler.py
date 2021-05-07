import queue
import requests
import threading
import time
from bs4 import BeautifulSoup
import csv
        

def search_links(q, urls, seen):
    while 1:
        try:
            url, level = q.get()
        except queue.Empty:
            continue
        if level <= 0:
            break
        try:
            soup = BeautifulSoup(requests.get(url).text, "lxml")
            for x in soup.find_all("a", href=True):
                link = x["href"]
                
                

                if link and link[0] in "#/":
                    link = url + link[1:]
                    
                if link not in seen:
                    seen.add(link)
                    urls.append(link)
                    q.put((link, level - 1))

            csv_file = open('Links.csv', 'w')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Links', 'Title'])

            for links in seen:
                soup_2 = BeautifulSoup(requests.get(links).text, "lxml")
                title = soup_2.find('title')
                # print(links, title)

                csv_writer.writerow([links, title])

            csv_file.close()


        except (requests.exceptions.InvalidSchema,
                requests.exceptions.ConnectionError):
            pass



        
   
if __name__ == "__main__":
    levels = int(input("How many levels of the website do you want to scrape through? (EX: 1/2/3..) "))
    workers = 15
    # workers_i = 2
    start_url = input("Enter the url that you want to scrape through [It should be in https:// format] ")
    seen = set()
    urls = []
    threads = []
    # titles = []
    q = queue.Queue()
    q.put((start_url, levels))
    start = time.time()

   

    for _ in range(workers):
        t = threading.Thread(target=search_links, args=(q, urls, seen))
        threads.append(t)
        t.daemon = True
        t.start()

    for thread in threads:
        thread.join()

    print(f"Found {len(urls)} URLs using {workers} workers "

          f"{levels} levels deep in {time.time() - start}s")




    

    