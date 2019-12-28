import os
import json
import sys
import pickle
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from math import log10, sqrt
from nltk.tokenize import word_tokenize
from collections import defaultdict


def main():
    word_dict = {}
    bookkeeping = defaultdict(lambda: defaultdict(int))  # location of word to use seek
    comp_book=defaultdict(int) #complete bookkeeping file
    file_name_number = 1
    len_counter = 0
    calculation_dict = defaultdict(list)  # url mapped to list of tfs, squared
    url_counter_dict = defaultdict(int)  # word mapped to amount of links

    url_square = defaultdict(float)
    counter = 0
    file_counter = 0
    for sub_dirs in os.listdir("DEV"):
        dev = "DEV/"
        for json_file in os.listdir(dev + sub_dirs):
            file_counter += 1

    for sub_dirs in os.listdir("DEV"):
        dev = "DEV/"
        for json_file in os.listdir(dev + sub_dirs):
            file_path = dev + sub_dirs + "/" + json_file
            f = open(file_path)
            data = json.load(f)
            dict_of_words = content_reader(data)
            url = data["url"]
            url_splitter_check = url.split("/")
            while "" in url_splitter_check:
                url_splitter_check.remove("")
            if len(url_splitter_check) > 0: #fragment checker
                if url_splitter_check[-1][0] == "#":
                    url_flag = url.find("#")
                    url = url[0:url_flag]
            if counter % 1000 == 0:
                print(counter)
            for word in dict_of_words:
                if len(word) > 0:
                    if not word in word_dict:
                        word_dict[word] = [[url, dict_of_words[word]]]
                    else:
                        word_dict[word].append([url, dict_of_words[word]])

            counter += 1
            # MAKE SURE EVEN THE LAST ONES THAT ARENT MODULO 15K ARE LOADED IN
            if counter % 15000 == 0 or counter % file_counter == 0:
                file_name = f'{file_name_number}.txt'

                new_file = open(file_name, "a+", encoding='utf8')
                for word in word_dict:
                    text_to_write = word + ":" + str(word_dict[word]) + '\n'
                    offset = len(text_to_write.encode('utf-8'))
                    original_len = len_counter
                    len_counter += offset
                    new_file.write(text_to_write)
                    bookkeeping[file_name_number][word] = (original_len, len_counter)
                    url = word_dict[word][0][0]
                    num = word_dict[word][0][1]
                    calculation_dict[url].append(num * num)

                new_file.close()

                file_name_number += 1
                word_dict = dict()

    for file_number in bookkeeping:
        pickle_dict = {}
        file_name = str(file_number) + ".txt"
        pickle_file_name = str(file_number) + ".pickle"
        file1 = open(file_name, "r", encoding='utf8')
        contents = file1.readlines()
        for line in contents:
            colon_break = line.find(":")
            word = line[:colon_break]
            word_info = line[colon_break+1:]





            pickle_dict[word] = word_info
        pickle_out = open(pickle_file_name, "wb")
        pickle.dump(pickle_dict, pickle_out)
        pickle_out.close()

    pickleAG = {}
    pickleHO = {}
    picklePZ = {}
    pickle_out = open("pickleAG.pickle", "wb")
    pickle.dump(pickleAG, pickle_out)
    pickle_out.close()

    pickle_out = open("pickleHO.pickle", "wb")
    pickle.dump(pickleHO, pickle_out)
    pickle_out.close()

    pickle_out = open("picklePZ.pickle", "wb")
    pickle.dump(picklePZ, pickle_out)
    pickle_out.close()

    term_url_count = defaultdict(int) #holds the num of docs that a term appears in

    for file_number in bookkeeping:
        pickle_file_name = str(file_number) + ".pickle"
        infile = open(pickle_file_name, "rb")
        temp_pickle = pickle.load(infile)
        infile.close()
        AG = {}
        HO = {}
        PZ = {}
        for i in sorted(temp_pickle.keys()):
            if i.strip():
                if i[0] <= "g":
                    try:
                        url_tf_list = eval(temp_pickle[i])
                    except:
                        continue
                    term_url_count[i] += len(url_tf_list)
               #     AG[i] = temp_pickle[i]
                    AG[i] = url_tf_list
                elif i[0] <= "o":
                    try:
                        url_tf_list = eval(temp_pickle[i])
                    except:
                        continue
                    term_url_count[i] += len(url_tf_list)
                  #  HO[i] = temp_pickle[i]
                    HO[i] = url_tf_list
                else:
                    try:
                        url_tf_list = eval(temp_pickle[i])
                    except:
                        continue
                    term_url_count[i] += len(url_tf_list)
                    #PZ[i] = temp_pickle[i]
                    PZ[i] = url_tf_list
        infile = open("pickleAG.pickle", "rb")
        temp_pickleAG = pickle.load(infile)
        infile.close()
        for i in AG:
            if i in temp_pickleAG:
                if i.strip():
            #        key = i
                    value = AG[i]
        #            value = value[1:-1]
         #           temp_pickleAG[i] += "," + value
                    for url in value:
                        temp_pickleAG[i].append(url)
            else:
                if i.strip():
               #     key = i
                    value = AG[i]
                #    value = value[1:-1]
                    temp_pickleAG[i] = value
        pickle_out = open("pickleAG.pickle", "wb")
        pickle.dump(temp_pickleAG, pickle_out)
        pickle_out.close()

        infile = open("pickleHO.pickle", "rb")
        temp_pickleHO = pickle.load(infile)
        infile.close()
        for i in HO:
            if i in temp_pickleHO:
                if i.strip():
                 #   key = i
                    value = HO[i]
                  #  value = value[1:-1]
                   # temp_pickleHO[i] += "," + value
                    for url in value:
                        temp_pickleHO[i].append(url)
            else:
                if i.strip():
          #          key = i
                    value = HO[i]
           #         value = value[1:-1]
                    temp_pickleHO[i] = value
        pickle_out = open("pickleHO.pickle", "wb")
        pickle.dump(temp_pickleHO, pickle_out)
        pickle_out.close()

        infile = open("picklePZ.pickle", "rb")
        temp_picklePZ = pickle.load(infile)
        infile.close()
        for i in PZ:
            if i in temp_picklePZ:
                if i.strip():
             #       key = i
                    value = PZ[i]
            #        value = value[1:-1]
              #      temp_picklePZ[i] += "," + value
                    for url in value:
                        temp_picklePZ[i].append(url)
            else:
                if i.strip():
               #     key = i
                    value = PZ[i]
                #    value = value[1:-1]
                    temp_picklePZ[i] = value
        pickle_out = open("picklePZ.pickle", "wb")
        pickle.dump(temp_picklePZ, pickle_out)
        pickle_out.close()

    complete_index = open("complete_index.txt", "a+", encoding='utf8')

    infile = open("pickleAG.pickle", "rb")
    temp_pickleAG = pickle.load(infile)

    infile.close()

    term_idf = {}

    for i in sorted(temp_pickleAG.keys()):
        key = i
        value = temp_pickleAG[i]
        idf = idf_calculator(term_url_count[key], file_counter)
        term_idf[key] = idf
        for url in value:
        #    idf = idf_calculator(url[0], term_url_count[key])
       #     term_idf[key] = idf
            url[1] = url[1] * term_idf[key] #turns tf into tf-idf by mult url[1](tf) by idf
            tf_idf=url[1]
            url_square[url[0]] += tf_idf**2

        string_line = key + ":" + str(value) + "\n"
        complete_index.write(string_line)

    infile = open("pickleHO.pickle", "rb")


    temp_pickleHO = pickle.load(infile)

    infile.close()

    for i in sorted(temp_pickleHO.keys()):
        key = i
        value = temp_pickleHO[i]
        idf = idf_calculator(term_url_count[key], file_counter)
        term_idf[key] = idf
        for url in value:
      #      idf = idf_calculator(term_url_count[key])
            url[1] = url[1] * idf  # turns tf into tf-idf by mult url[1](tf) by idf
            url_square[url[0]] += url[1] ** 2
        string_line = key + ":" + str(value) + "\n"
        complete_index.write(string_line)

    infile = open("picklePZ.pickle", "rb")
    temp_picklePZ = pickle.load(infile)

    infile.close()

    for i in sorted(temp_picklePZ.keys()):
        key = i
        value = temp_picklePZ[i]
        idf = idf_calculator(term_url_count[key], file_counter)
        term_idf[key] = idf
        for url in value:
#            idf = idf_calculator(url[0], term_url_count[key])
            url[1] = url[1] * idf  # turns tf into tf-idf by mult url[1](tf) by idf
            url_square[url[0]] += url[1] ** 2

        string_line = key + ":" + str(value) + "\n"
        complete_index.write(string_line)

    pickle_out = open("term_idf.pickle", "wb")
    pickle.dump(term_idf, pickle_out)
    pickle_out.close()


    complete_index.close()
    for url in url_square:
        url_square[url] = sqrt(url_square[url])

    pickle_out = open("url_square.pickle", "wb")
    pickle.dump(url_square, pickle_out)
    pickle_out.close()

    #read file
    position_counter = 0
    complete_index=open("complete_index.txt",'r', encoding='utf8')
    for line in complete_index.readlines():  # make bookkeeping file for complete index that tracks the position of each word so that seek can be used to later find it in searcher
        index_of_term = line.find(":")
        term = line[:index_of_term]

        comp_book[term] = position_counter #this gets the last position found per word only rn
        position_counter += (len(line.encode('utf-8'))+1)

    complete_index.close()
    comp_book_pickle=open('complete_index_bookkeeping.pickle','wb') #write comp book to pickle file
    pickle.dump(comp_book,comp_book_pickle)
    comp_book_pickle.close()


    # MAKE BOOKKEEPING FOR INDEX AS IT IS ADDED TO COMPLETE_INDEX.TXT
    # MAKE PICKLE FILE FOR THE BOOKKEEPING
    # MAKE PICKLE FILE FOR SUMMATION SQUARE ROOT 
    # MAKE PICKLE FILE FOR THE URL COUNTS

    # for url_tf in word_dict[term]:
    # idf_score = idf_calculator(url_tf[0], url_count)
    # tf_idf = idf_score * url_tf[1]
    # url_tf[1] = tf_idf

    dict_size = str(sys.getsizeof(word_dict))
    dict_len = str(len(word_dict))

    print("size of index: " + dict_size)
    print("number of files: " + str(counter))
    print("number of unique words: " + dict_len)


def idf_calculator(url_count, file_counter):
    idf = log10(file_counter / url_count)
    return idf


def content_reader(data):
    dict_of_words = {}
    content = data["content"]
    soup = BeautifulSoup(content, "html.parser")
    text = soup.find_all(text=True)

    output = ''
    output2 = ''
    blacklist = [
        # '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'style',
        'div',
        'a',
        'img',
        'head',
        'input',
        'container',
        'script',
    ]

    important_list = ['h1', 'h2', 'h3', 'strong', 'title']
    for t in text:
        if t.parent.name not in blacklist:
            if t.parent.name in important_list:
                output += '{} '.format(t)
                output2 += '{} '.format(t)
            else:
                output2 += '{} '.format(t)
    ps = PorterStemmer()
    list_of_impt_words = output.split()
    list_of_all_words = output2.split()
    list_of_all_words = [x for x in list_of_all_words if  not x.isdigit()] 
    biword = ""
    biword_count = 0
    for w in list_of_all_words:
        w = ps.stem(w)
        w = w.lower()
        #if w.isalnum():
        if w.isalpha():
            if biword == "":
                biword = w
            else:
                biword = biword + " " + w
            if w in dict_of_words:
                if w in list_of_impt_words:
                    dict_of_words[w] += 5
                else:
                    dict_of_words[w] += 1
            else:
                if w in list_of_impt_words:
                    dict_of_words[w] = 5
                else:
                    dict_of_words[w] = 1
            if len(biword.split()) == 2:
                biword_count += 1
                if biword in dict_of_words:
                    dict_of_words[biword] += 1
                else:
                    dict_of_words[biword] = 1
        biword = w    
    for w in dict_of_words:
        log_value = dict_of_words[w] / (len(list_of_all_words) + biword_count)
        # print(f'{dict_of_words[w]}: {log_value}' )

        dict_of_words[w] = 1 + log10(dict_of_words[w])
    
    return dict_of_words


if __name__ == "__main__":
    main()




