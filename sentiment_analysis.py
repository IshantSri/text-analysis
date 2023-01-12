from nltk.tokenize import  word_tokenize
import nltk
nltk.download('punkt')
import string
import os
from utilities import read_text_file,read_text_file2,mapping,remove_url_txt


"""

SUPPORTING FUNCTIONS FOR SENTIMENT ANALYSIS

"""

class sentiment_analysis:
    #def __init__(self):
        #self.log_file = 'logging_/text_Analysis_log.txt'

    """
    Cleaning The Stopwords

    """
    def stop_word_pre(self,sw_path):


        # Folder Path
        path = sw_path
        # Change the directory
        os.chdir(path)
        custom_data = []
        try:
            for file in os.listdir():
                file_path = f"{path}\\{file}"
                # call read text file function
                sw = read_text_file(file_path)
                sw = sw.lower()
                custom_data.append(sw)
            custom_data = mapping(custom_data)
            custom_data = custom_data.split(",")

            return(custom_data[:-1])
        except Exception as e:
            print(str(e))


    """
    Building up a dictionary for positive and negative words
    
    """
    def dicti(self,loc,stop_words):

        # Folder Path
        path = loc
        # Change the directory
        os.chdir(path)
        try:
            # Read text File containing positive words
            file_path = f"{path}\\positive-words.txt"
            pos = read_text_file(file_path)
            pos = pos.split("\n")
            for i in pos:
                if i in stop_words:
                    pos.remove(i)
            positive_wds = set(pos[:-1])

            # Read text File containing negative words
            file_path = f"{path}\\negative-words.txt"
            neg = read_text_file2(file_path)
            neg = neg.split("\n")
            for i in neg:
                if i in stop_words:
                    neg.remove(i)
            negative_wds = set(neg[:-1])

            #storing negative and positive words in dictionary
            p_n_dict ={"positive":positive_wds,"negative":negative_wds}

            return p_n_dict
        except Exception as e:
            print(str(e))


    """
    Cleaning The Text Scraped
    
    """

    def text_preprocess(self,articles,stopwords):#scraped data location

        try:
            text = articles
            text = text.lower()
            text = remove_url_txt(text)
            text = text.translate(str.maketrans('', '', string.punctuation))
            text = word_tokenize(text)

            for i in text:
                if i in stopwords:
                    text.remove(i)
            return text
        except Exception as e:
            print(str(e))

