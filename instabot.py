from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import bs4, os, argparse, getpass
import requests as req

url = []
counter = 1
class InstaBot:
    """Class for instagram bot login and some bypasses"""
    def __init__(self,email,password,target):
        """Init for obj"""
        self.browser = webdriver.Chrome()
        self.browserTwo = webdriver.Chrome()
        self.email = email
        self.password = password
        self.target = target
        self.browser.get('https://instagram.com')
        sleep(2)
        self.browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(self.email)
        self.browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(self.password)
        self.browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()
        sleep(5)
        try:
            """Clicking not save in save login info"""
            self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()
        except:
            print('Exception in first try bypassing store login info')
        sleep(5)
        try:
            """Clicking Not show notification"""
            self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except:
            print('Exception in second try bypassing Notification')
        sleep(2)
        os.makedirs(self.target,exist_ok=True)
        os.chdir(self.target)


    def downloader(self):
        """This will open the new url in webbrowser and then scrape the scr to the media and scrapp it"""
        global url
        global counter
        # print((url))
        for u in url:
            self.browserTwo.get(u)
            try:
                """First we look if the media is video"""
                srcTags = self.browserTwo.find_elements_by_tag_name("video")
                ext = '.mp4'
                srcTags[0].get_attribute('src')
            except:
                """If not then picture"""
                srcTags = self.browserTwo.find_elements_by_tag_name("div > img")
                ext = '.jpg'
                print('Pic')
                src = srcTags[0].get_attribute('src')
                pass
            for tag in srcTags:
                src = tag.get_attribute('src')
                if 'https://instagram.fdel17-1.fna.fbcdn.net/' in src:
                    print(src)
                    res = req.get(src)
            # while True:
            
            name = str(counter)+ext
                # if not os.path.exists(name):
                    # break
            counter += 1
            with open(name,'wb') as fil:
                for chunk in res.iter_content(100000):
                    fil.write(chunk)
        url = []

    def scrool(self):
        """Just scrolling to get new media and sleeping to let it load"""
        html = self.browser.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        sleep(3)
            

    def scrapp(self):
        """If new media has loaded and new links are and are proper then scrapp those links for downloader"""
        sleep(5)
        self.browser.get(f'https://www.instagram.com/{self.target}/')
        while True:
            self.scrool()
            rows = self.browser.find_elements_by_tag_name('div > div > a')
            # sleep(5)
            for link in rows:
                new_url = link.get_attribute('href')
                if 'https://www.instagram.com/p/' in new_url:
                    if new_url not in url:     
                        # new_url = link.get_attribute('href')
                        # print(new_url)
                        url.append(new_url)
                        self.downloader()       

def arguments():
    parser = argparse.ArgumentParser(description='Scrapp instagram pictures')
    parser.add_argument('-u','--username',help='username eg. ..gram.com/username/')
    parser.add_argument('-t','--target',help='target username eg. ..gram.com/targetusername/')
    # parser.add_argument('-d',)
    args = parser.parse_args()
    return args


args = arguments()
print(args.username,args.target)
password = getpass.getpass('IG paswword: ')
instabot = InstaBot(args.username,password,args.target)
instabot.scrapp()