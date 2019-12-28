import os
import json
import sys
import pickle
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from math import log10
from math import sqrt
from nltk.tokenize import word_tokenize
import datetime
from collections import defaultdict


def main():
    ps = PorterStemmer()
 #   search_list = []
    searcher = []
    comp_sets_list = []
    init_set = set()
    results = {}
    bookkeeping = pickle.load(open("complete_index_bookkeeping.pickle", "rb"))
    index=open('complete_index.txt','r', encoding='utf8')
    query_dict=defaultdict(list)

    infile = open("url_square.pickle", "rb")  # opens a file with the idf score of each term {term:idf}
    pickledenomsquare = pickle.load(infile)
    infile.close()

    infile = open("term_idf.pickle", "rb") #opens a file with the idf score of each term {term:idf}
    pickleidf = pickle.load(infile)
    infile.close()

    #put in while loop
    while True:
        search_list = []
        search = input("Enter Your Search ('quit' to exit): ")
        print(datetime.datetime.now().time())
        search = search.lower()
        if search == "quit":
            break
        search = search.split()
        biword = ""
        first_word = ""
        temp_search = search
        for i in temp_search:
            word = ps.stem(i)
            if biword == "":
                biword = word
                first_word = i
            else:
                biword += " " + word
                if biword in bookkeeping:
                    if len(get_list(biword,index,bookkeeping)) > 10:
                        search.append(biword)
                        try:
                            search.remove(first_word)
                        except:
                            continue
                        try:
                            search.remove(i)
                        except:
                            continue
            first_word = i
        for i in search:
            word = i
            if len(word.split()) == 1:
                word = ps.stem(word)
            if word in bookkeeping:
                query_dict[word]=get_list(word,index,bookkeeping)
                search_list.append(word)
        doc_list = cos_sim(search_list, query_dict, pickledenomsquare, pickleidf)

        count = 0
        for i in doc_list:
            if count < 10:
                    print(i[0])
                    count += 1
            else:
                break

        # if len(search_list) == 1:
        #
        # else:
        #     doc_list = cos_sim(search_list, word_dict, pickledenomsquare, pickleidf)

        print(datetime.datetime.now().time())


def get_list(word:str,complete_index,comp_book):

    pos = comp_book[word]

    complete_index.seek(pos)
    line=complete_index.readline()
    line_to_eval=line[line.find(":")+1:]
    return eval(line_to_eval)

def cos_sim(query_terms, word_dict, temp_pickledenomsquare, pickleidf):
 #  term_list = query_terms.split()
    cos_scores = defaultdict(float) #cos score for each doc with the query stuffs   --numerator for each doc
    query_term_tfidf = calc_query_tfidf(query_terms, pickleidf) #dict of query terms w/ value of term tfidf
    query_term_denom = calc_query_term_denom(query_term_tfidf)


    # infile = open("url_square.pickle", "rb")  # opens a file with the idf score of each term {term:idf}
    # temp_pickledenomsquare = pickle.load(infile)
    # infile.close()

    for query_term in query_terms: #go through each query term
        for doc in word_dict[query_term]:
            cos_scores[doc[0]] += query_term_tfidf[query_term] * doc[1]

    for doc in cos_scores:
        cos_scores[doc] = cos_scores[doc]/ (query_term_denom * temp_pickledenomsquare[doc])#length denom

    return sorted(cos_scores.items(), key = lambda x : x[1], reverse = True)
    #return a list of docs sorted by highest cos_sim to lowest

def calc_query_tfidf(term_list, temp_pickleidf):  #, word_dict): gives us W(t,q)
    term_tfidf = defaultdict(float)

    # infile = open("term_idf.pickle", "rb") #opens a file with the idf score of each term {term:idf}
    # temp_pickleidf = pickle.load(infile)
    # infile.close()

    for term_count in term_list:
        term_tfidf[term_count] += 1 #holds a count of each word in the query

    for term_count in term_tfidf: #calc tf idf of each term in the query
        term_tfidf[term_count] = (1 + log10(term_tfidf[term_count])) * temp_pickleidf[term_count]  #mistake: / len(term_list))

 #   for term_tf in term_tfidf: #calc tfidf from the term tf and the idf from word_dict
  #      term_tfidf[term_tf] = term_tfidf[term_tf] * temp_pickleidf[term_tf]

    return term_tfidf #a dict of the query terms with its tfidf of query as

def calc_query_term_denom(term_tfidf):
    square_sum = 0.0
    for term in term_tfidf:
        square_sum += (term_tfidf[term] ** 2)
    square_sum = sqrt(square_sum)
    return square_sum


if __name__ == "__main__":
    main()
