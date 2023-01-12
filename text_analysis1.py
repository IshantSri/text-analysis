from  utilities import read_text_file,wordcount,sentencecount,syllable_count
import os
import re
from data_getter.data_loading import datagetter
from data_getter.web_scraping import webscraper
from sentiment_analysis import sentiment_analysis


path = "C:\\Users\\ishan\\PycharmProjects\\text_analysis" # setting up our working directory
os.chdir(path)


"""
Using webscraper function to scrape data from site

"""
scraped = webscraper("C:\\Users\\ishan\\PycharmProjects\\text_analysis\\input.xlsx")
bad_data = scraped.scraping() #getting list of id of all the bad_data


#getting the output schema using datagetter function

output_data = datagetter("C:\\Users\\ishan\\PycharmProjects\\text_analysis\\Output_Data_Structure.xlsx")
output_data = output_data.readfile()

"""
Importing all txt file from scraped_data folder

"""

path = "C:\\Users\\ishan\\PycharmProjects\\text_analysis\\scraped_data" #scraped data path
# Change the directory
os.chdir(path)

"""
iterate through all files 
read the .txt docs and apply the analysis

"""

for file in os.listdir():
    if file.endswith(".txt"):
        file_path = f"{path}\\{file}"
        name = float(file[:-4])

        with open(file_path, encoding='utf-8') as f:
            article  = f.read()


        """
        Average Number of Words Per Sentence
        The formula for calculating is:
        Average Number of Words Per Sentence = the total number of words / the total number of sentences
        """

        word_c = wordcount(article)
        sen_c = sentencecount(article)
        av = word_c / sen_c

        ''''
         syllable per word
         
        '''''
        sypw = syllable_count(article) / wordcount(article)


        """
        complex_words
        
        """
        allwords = re.findall("[a-zA-Z-]+", article)
        count_complex = 0
        wer = []
        for i in allwords:
            if syllable_count(i) > 2:
                wer.append(i)
                count_complex += 1

        """ 
        Analysis of Readability is calculated using the Gunning Fox index formula described below.
        Average Sentence Length = the number of words / the number of sentences
        Percentage of Complex words = the number of complex words / the number of words 
        Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
        """
        Avg_Sen_Len = word_c / sen_c
        percent_comp = 100 * count_complex / word_c
        fog_index = 0.4 * (Avg_Sen_Len + percent_comp)

        """
        Average Word Length
        """
        no_char = 0
        for i in allwords:
            for j in i:
                no_char += 1
        avgwordlen = no_char / len(allwords)

        """
        personal_pronoun
        """
        pp_count = 0
        p_pron = ['I', 'we', "We", 'my', "My", 'ours', 'Ours', "us"]
        for i in allwords:
            if i in p_pron:
                pp_count += 1

        """
        Sentimental Analysis
        """
        analysis = sentiment_analysis()
        stop_words = analysis.stop_word_pre("C:\\Users\\ishan\\PycharmProjects\\text_analysis\\stopword_directory")
        pos_neg_dict = analysis.dicti("C:\\Users\\ishan\\PycharmProjects\\text_analysis\\MasterDictionary",stop_words)
        clean_text = analysis.text_preprocess(article,stop_words)
        total_words_after_cleaning = len(clean_text)
        positive_count = 0
        negative_count = 0
        for i in clean_text:
            if i in pos_neg_dict["positive"]:
                positive_count += 1
            if i in pos_neg_dict["negative"]:
                negative_count -= 1
        negative_count = (negative_count)*-1
        polarity_score =  (positive_count-negative_count)/((positive_count + negative_count) + 0.000001)
        SubjectivityScore = (positive_count + negative_count) / ((total_words_after_cleaning) + 0.000001)
        """
        output
        """
        for i in range(len(output_data)):
            if output_data['URL_ID'][i] == name:
                output_data["POSITIVE SCORE"][i] = round(positive_count, 2)
                output_data["NEGATIVE SCORE"][i] = round(negative_count, 2)
                output_data["POLARITY SCORE"][i] = round(polarity_score, 2)
                output_data["SUBJECTIVITY SCORE"][i] = round(SubjectivityScore, 2)
                output_data["AVG SENTENCE LENGTH"][i] = round(Avg_Sen_Len,2)
                output_data["PERCENTAGE OF COMPLEX WORDS"][i] = round(percent_comp,2)
                output_data["FOG INDEX"][i] = round(fog_index,2)
                output_data["AVG NUMBER OF WORDS PER SENTENCE"][i] = round(av,2)
                output_data["COMPLEX WORD COUNT"][i] = round(count_complex,2)
                output_data["WORD COUNT"][i] = round(total_words_after_cleaning, 2)
                output_data["SYLLABLE PER WORD"][i] = round(sypw,2)
                output_data["PERSONAL PRONOUNS"][i] = round(pp_count,2)
                output_data["AVG WORD LENGTH"][i] = round(avgwordlen,2)

path = "C:\\Users\\ishan\\PycharmProjects\\text_analysis"
# Change the directory
os.chdir(path)
output_data = output_data.fillna("NA") #filling NA for nan values in bad data's scores
output_data.to_excel("Output_Data.xlsx",index=False)


