# S-H4CK13@Maptnh

from lxml import html
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import re
from tqdm  import tqdm


LOGO = '''
 /$$    /$$           /$$           /$$                 /$$             /$$      /$$ /$$$$$$$
| $$   | $$          | $$          | $$                | $$            | $$  /$ | $$| $$__  $$
| $$   | $$ /$$   /$$| $$ /$$$$$$$ | $$$$$$$  /$$   /$$| $$$$$$$       | $$ /$$$| $$| $$  \ $$
|  $$ / $$/| $$  | $$| $$| $$__  $$| $$__  $$| $$  | $$| $$__  $$      | $$/$$ $$ $$| $$$$$$$/
 \  $$ $$/ | $$  | $$| $$| $$  \ $$| $$  \ $$| $$  | $$| $$  \ $$      | $$$$_  $$$$| $$____/
  \  $$$/  | $$  | $$| $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$      | $$$/ \  $$$| $$
   \  $/   |  $$$$$$/| $$| $$  | $$| $$  | $$|  $$$$$$/| $$$$$$$/      | $$/   \  $$| $$
    \_/     \______/ |__/|__/  |__/|__/  |__/ \______/ |_______//$$$$$$|__/     \__/|__/
                                                               |______/
                                                                S-H4CK13@Maptnh
                                                            https://github.com/MartinxMax
                                                               '''
class Main:


    def __init__(self):
        self.results = dict()

    def query_mechines(self,query):
        urlsq=list()
        try:
            stat = requests.get("https://www.vulnhub.com?q="+query,verify=False)
        except TimeoutError:
            print("[!] Time out")
        except Exception as e:
            print("[!] Get mechines Error!")
        else:
            if stat.status_code == 200:
                xpath = "//div[@class='card-title']/a/@href"
                href_contents = html.fromstring(stat.content).xpath(xpath)
                for href in tqdm(href_contents):
                    urlsq.append("https://www.vulnhub.com"+href)
                for index, url in enumerate(urlsq):
                    print(f"[{index+1}] URL: {url}")
                index = int(input("[+] Choice options: "))
                urls_u = self.get_urls(urlsq[index-1])
                if len(urls_u) >0 :
                    for url in tqdm(urls_u):
                        self.verify_website(url)
                    else:
                        self.display()
                else:
                    print("[!] No Walkthough...")


    def get_urls(self,url):
        urls = list()
        xpath = "//ul[@class='list-inline list-group']/li/a[@rel='nofollow']/@href"
        response = requests.get(url,verify=False)
        tree = html.fromstring(response.content)
        href_contents = tree.xpath(xpath)
        for href in tqdm(href_contents):
            urls.append(href)
        return urls

    def verify_website(self,url):
        try:
            stat = requests.get(url,verify=False,timeout=3)
        except TimeoutError:
            print("[Time Out]: ",url)
        except Exception as e:
            pass
        else:
            if stat.status_code == 200:
                match = re.search(r'<title>(.*?)</title>', stat.text)
                title = match.group(1)
                self.results[title]=url


    def display(self):

        max_key_length = max(len(k) for k in self.results.keys())
        print('-' * (max_key_length + 64))
        print('{:<{width}} | {:<60}'.format('Title', 'URL', width=max_key_length))
        print('-' * (max_key_length + 64))
        for k, v in self.results.items():
            print('{:<{width}} | {:<60}'.format(k, v, width=max_key_length))
        print('-' * (max_key_length + 64))



def main():
    print(LOGO)
    query = input("[+] Query: ")
    Main().query_mechines(query)


if __name__ == '__main__':
    main()
