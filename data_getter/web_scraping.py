from logging_.log import logging
import requests
from bs4 import BeautifulSoup as bs
from data_getter.data_loading import datagetter
from utilities import remove_tags

"""
CLASS FOR SCRAPING DATA FROM WEBSITE USING BeutifulSooup.

"""

class webscraper:
    def __init__(self,data_loc):
        self.data_loc = data_loc
        self.log_file = 'logging_/webscraper_log.txt'
        self.logobj = logging(self.log_file, 'ENTERED TO DATA SCRAPER')
        self.logobj.log()
        self.data = datagetter(self.data_loc)
    def scraping(self):

        url_sheet = self.data.readfile() #reading .xlsx file which contains url_id and urls for article

        urls= url_sheet["URL"] #urls for article

        url_id = url_sheet["URL_ID"]


        headers = {
            "user-agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'
        }

        # search and scrape data for every url link
        a = 0
        bad_data = []  #stores url_id of links which are expired or not working
        while a <= len(url_id) - 1:
            url = urls[a]
            try:
                r = requests.get(url, headers=headers)
                html_content = r.content
                soup = bs(html_content, "html.parser")


                title = soup.find("h1", class_="entry-title") #getting articles title from h1 tag
                title = title.text



                soup = soup.find("div", class_="td-post-content") #main cntent scraped
                article = remove_tags(soup)

                #opening URL_ID.txt file to store the above scraped data
                with open(f"C:\\Users\\ishan\\PycharmProjects\\text_analysis\\scraped_data\\{url_id[a]}.txt", "w", encoding="utf-8") as f:
                    # converting the whole text into lower case and saving into a text file
                    f.write(title)
                    f.write(article)
                self.logobj.appnd_log("DATA SCRAPED SUCCESSFULLY")
            except Exception as e:
                bad_data.append(url_id[a])
                self.logobj.appnd_log(f"{url_id[a]} EXCEPTION MESSAGE>>>>>> " + str(e))
            a += 1

        #stored bad data for future reference
        with open("C:\\Users\\ishan\\PycharmProjects\\text_analysis\\bad_data_info.txt", "a", encoding="utf-8") as f:
            f.write("bad_Data_Url_id" + "\n" + str(bad_data)+"\n")
        return bad_data


