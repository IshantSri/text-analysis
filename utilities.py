import re

"""
function to remove urls

"""

def remove_url_txt(text):
    pattern = re.compile(r"https?://\S+www\.\S+")
    return pattern.sub(r"",text)

"""
Function to remove unwented tags

"""

def remove_tags(soup):
    # parse html content
    # soup = BeautifulSoup(html, "html.parser")

    for data in soup(["pre"]):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

"""
read files from file location

"""
def read_text_file(file_path):
    with open(file_path, "r") as f:
        g = f.read()
        return g
def read_text_file2(file_path):
    with open(file_path, encoding='ISO-8859-1') as f:
        g = f.read()
        return g
"""
Function to remove special characters

"""
def mapping(data):
    try:
        cust_data = str()
        for i in data:
            i = re.sub(r"http\S+", "", i)
            i = re.sub(r"Surnames from 1990 census > .002%.  www.census.gov.genealogy/names/dist.all.last,", "", i)

            cust_data = cust_data + i.replace("\n", ",").replace("|", ",").replace(" , ", ",").replace(" ,", ",")
        return cust_data
    except Exception as e:
        print(e)

"""

function to every word in text data

"""
def wordcount(text):
    # Regex to match all words, hyphenated words count as a compound words
    return len(re.findall("[a-zA-Z-]+", text))


"""

function to every sentence in text data

"""
def sentencecount(sentence):
    # regex to count sentences
    sentence = re.sub(r'(?<=\d)[,\.]', '', sentence)  # regex to remove decimals from sentences
    return (len(re.split("[.!?]+", sentence)))

"""

function to every syllable word in text data

"""
def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiou"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith( "es"):
        count -= 1
    elif word.endswith("ed"):
        count -= 1
    elif count == 0:
        count += 1
    return count