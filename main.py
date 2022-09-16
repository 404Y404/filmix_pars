from selenium import webdriver
from selenium.webdriver.common.by import By
import wget
import time
import os

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/yura/selenium/adblock")
# options.add_argument('headless')
browser = webdriver.Chrome(chrome_options=options)
selector_right = '[style="position: absolute; display: inline-block; width: 40px; height: 100%; text-align: left; background: linear-gradient(to left, rgb(0, 0, 0), rgba(0, 0, 0, 0)); cursor: pointer; top: 0px; right: 0px; padding-top: 15px; visibility: visible; opacity: 1;"]'
selector_left = 'style="position: absolute; display: inline-block; width: 40px; height: 100%; text-align: left; background: linear-gradient(to right, rgb(0, 0, 0), rgba(0, 0, 0, 0)); cursor: pointer; top: 0px; left: 0px; padding-top: 15px; visibility: visible; opacity: 1;"'
selector_quit = '[style="position: relative; right: 0px; top: 0px; cursor: pointer; height: 50px; width: 170px; overflow: hidden; display: inline-block; line-height: 1.5em; vertical-align: top; white-space: normal; border-right: 1px solid rgb(136, 136, 136);"]'
download_list={0:[0]}
download_links={0:[0]}
#selector = '[style="position: relative; right: 0px; top: 0px; cursor: pointer; height: 50px; width: 170px; overflow: hidden; display: inline-block; line-height: 1.5em; vertical-align: top; white-space: normal;"]'
def parse():
    video = str(browser.find_element(
        By.CSS_SELECTOR, "video").get_attribute("src"))
    return video


def get_button(number):
    selector = '[fid="{number}"][style="position: relative; right: 0px; top: 0px; cursor: pointer; height: 50px; width: 170px; overflow: hidden; display: inline-block; line-height: 1.5em; vertical-align: top; white-space: normal;"]'
    return browser.find_element(By.CSS_SELECTOR, selector.format(number=number - 1))


def get_links(season, numbers):
    time.sleep(0.7)
    season=get_button(season)
    season.click()
    time.sleep(0.5)
    episodes = []
    for episode in numbers:
        try:
            time.sleep(1)
            get_button(int(episode)).click()
            get_button(episode).click()
            get_button(episode).click()
            time.sleep(1)
        except:
            time.sleep(3)
            try:
                get_button(episode).click()
                get_button(episode).click()
                get_button(episode).click()
            except:
                try:
                    time.sleep(2)
                    get_button(episode).click()
                    get_button(episode).click()
                    get_button(episode).click()
                except:
                    pass
        print(episodes)
        episodes.append(parse())
    try:
        time.sleep(0.7)
        browser.find_element(By.CSS_SELECTOR, selector_quit).click()
        time.sleep(0.3)
    except:
        pass
    print(episodes)
    return episodes

def get_all_episode():
    selector = '[style="position: relative; right: 0px; top: 0px; cursor: pointer; height: 50px; width: 170px; overflow: hidden; display: inline-block; line-height: 1.5em; vertical-align: top; white-space: normal;"]'
    return [i for i in range(1,len(browser.find_elements(By.CSS_SELECTOR ,selector)) + 1)]


def get_all():
    selector = '[style="position: relative; right: 0px; top: 0px; cursor: pointer; height: 50px; width: 170px; overflow: hidden; display: inline-block; line-height: 1.5em; vertical-align: top; white-space: normal;"]'
    seasons = browser.find_elements(By.CSS_SELECTOR, selector)
    for i in range(1,len(seasons)+1):
        if i%3!=0:
            print(i)
            season=seasons[i-1]
            season.click()
            download_list.update({i:get_all_episode()})
        else:
            browser.find_element(By.CSS_SELECTOR, selector_right).click()
            season=seasons[i-1]
            print(i)
            time.sleep(0.5)
            season.click()
            download_list.update({i:get_all_episode()})
        browser.find_element(By.CSS_SELECTOR, selector_quit).click()
        seasons = browser.find_elements(By.CSS_SELECTOR, selector)


def get_list_links():
    for season in download_list:
        if season != 0:
            download_links.update({season:get_links(season, download_list[season])})

def download(path):
    for season in download_links:
        if season != 0:
            new_path = f"{path}{season}_сезон"
            try:
                os.mkdir(new_path)
            except:
                pass
            for link in range(len(download_links[season])):
                wget.download(download_links[season][link], out=f"{new_path}/{download_list[season][link]}.mp4")





def main():
    try:
        browser.get(input("Введите ссылку на фильм   "))
        path=input("Введите путь сохранения   ")
        seasons = input("Введите номера сезонов через - или all для скачивания всего сериала   ")
        if seasons == "all":
            get_all()
        else:
            start_season, stop_season = map(int, seasons.split("-"))
            for season in range(start_season, stop_season + 1):
                start_episode = int(input("Введите от какой серии   "))
                stop_episode = int(input("Введите до какой серии   "))
                download_list.update({season:[i for i in range(start_episode, stop_episode+1)]})

        get_list_links()
        download(path)

        
    finally:
        browser.quit()

if __name__ == '__main__':
    main()
    