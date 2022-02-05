import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1]) 
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    
    
    
    #this code is from page rank.  DO not use make my own version!!!!!!!!!!!!!!!!!!!!!!
    
    dict_of_file_content = dict()

    # get list of all file names in the directory
    all_files_in_directory = os.listdir(directory)

    #iterate through all the file names
    for fname in all_files_in_directory:
      
        #only process text files
        if fname.endswith(".txt"):
            #construct an operating specific path to the file
            filename = os.path.join(directory, fname)
            #open the file
            f = open(filename, "r",encoding='utf-8')
            #read the whole file content into a dictionary and using the fname as the key
            dict_of_file_content[fname] = f.read()
            #close the file and loop back up and process the next file
            f.close()
            

    return dict_of_file_content    
    raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    print("inside tokenize")
    
    #function to remove punctuation from any word
    def punctuation_filter(word):
        punctuation = string.punctuation
        processed_word = word
        for character in punctuation:
            processed_word = processed_word.replace(character, "")    
        return processed_word
    
    #determine if a word is among the group of english stopword
    def check_valid_word(word):
        stopwords = nltk.corpus.stopwords.words("english")
        stopwords = set(stopwords)

        for stopword in stopwords:
            if word  in stopwords:
                return False
            else:
                return True

    
    #####stopwords = nltk.corpus.stopwords.words("english")
    
    #print(nltk.corpus.stopwords.words("english"))

    final_processed_document =""
    processed_document = document.lower()
    processed_document = processed_document.split(" ")

    #processed_word = filter(punctuationFilter, word) ##REDO REDO!!!!! #remove any punctuation
    #stopwordsSet= set(stopwords)
    
    
    # remove stopwords         # do not process any English stop words
      

    for word in processed_document:
        processed_word = punctuation_filter(word)
        #print(check_valid_word(processed_word))
        if not check_valid_word(processed_word):
            continue

        words = "".join(processed_word)
        final_processed_document += words + " "

    #print("processedWord = ",final_processed_document)
    tokenized_words = nltk.word_tokenize(final_processed_document)
    return tokenized_words


    raise NotImplementedError    
        
    """
        for test_char in word:
            if test_char in punctuation:
                processed_word = word.replace(test_char, "")

        #processed_word = filter(str.isalnum, processed_word)
        #processed_word = filter(str.isalnum, processed_word)

        words = "".join(processed_word)
        final_processed_document += words + " "

        tokenized_words = nltk.word_tokenize(final_processed_document)
        
    return tokenized_words

    """






    raise NotImplementedError


    

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    idfs = dict()
    dictionary_of_documents_containg_set_of_their_words = dict()
    set_of_all_documents_words = set()
    idflist=[]
    #tf = documents

    #print("document name = ",documents.keys())
    #print(documents['artificial_intelligence.txt'])
    tmp=""
    for document_name in documents:
        print(document_name)
        specific_words_in_document = set(documents[document_name])
        # create a set of all unique words in all files
        set_of_all_documents_words.update(documents[document_name])
        # creat dictionary of each document pointing to a set of all it's words
        dictionary_of_documents_containg_set_of_their_words[document_name]=specific_words_in_document
        tmp += document_name+ " "

        for word in set_of_all_documents_words:
            idfs[word]=0
            for document_name in dictionary_of_documents_containg_set_of_their_words:
                if word in dictionary_of_documents_containg_set_of_their_words[document_name]:
                    idfs[word] += 1


        for word in idfs:
            idfs[word] = math.log(len(documents)/idfs[word])

        '''
        for word in documents[document_name]:
            #if word == 'learning':
                #print("zzz",document_name,word)
            specific_words_in_document.add(word)

        #find word frequency    
        for word in specific_words_in_document:
            

            # create an array of all locations in the documment that matches a specific word
            matching_words_indexes=[document_word for document_word in range(len(documents[document_name])) if documents[document_name][document_word]==word]
            #if word == 'learning':
                #print(document_name,len(matching_words_indexes))            
            matching_word_count= len(matching_words_indexes)
            #print(word,matching_word_count)
            #idflist.append((word,matching_word_count))    
            '''
    
            #idfs.update({word:idf}) # almost there
            
    #print(idfs)
    #print(93939393,tmp)     
    #print(set_of_all_documents_words)     
    #print(dictionary_of_documents_containg_set_of_their_words['test2.txt'])
    #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXIDF are ======",len(idfs))
    return idfs
    raise NotImplementedError

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #print("type(files)",type(files))
    #print(100000000,type(query),query)
    tfs = dict()
    tflist=[]
    tfidfs  = dict()
    #tf = documents

    #print("document name = ",documents.keys())
    #print(documents['artificial_intelligence.txt'])

    for document_name in files:
        #creat a new set for each document
        specific_words_in_document = set()
        for word in files[document_name]:
            #if word == 'learning':
                #print("zzz",document_name,word)
            # add every word in the current document to a set
            specific_words_in_document.add(word)

        #find word frequencies for each document
        for word in specific_words_in_document:
            

            # create an array of all locations in the documment that matches a specific word
            matching_words_indexes=[document_word for document_word in range(len(files[document_name])) if files[document_name][document_word]==word]
            #if word == 'learning':
                #print(document_name,len(matching_words_indexes))            
            matching_word_count= len(matching_words_indexes)
            #print(word,matching_word_count)
            tflist.append((word,matching_word_count))    

            tfs.update({document_name:tflist}) # almost there

        #now that we found the tf's for each word in each document
    document_word_count = 0
    documents_containg_word_flag =  dict()
    for documentname in files:
        #print("====================",len(files))
        #print("====================",documentname, len(documentname))
        tfidfs[documentname] = []
        for word in files[documentname]: 
            if word in query:
            #if word == 'test':
                # keep track of the documents that contain a  each word
                documents_containg_word_flag[word] = True
                document_word_count[documentname][word] +=1
                print(word,documentname,idfs[word],query)

        #for word in files[documentname]: 

    #tfidfs[documentname].append((word, tfs[word] * idfs[word] ))
                

            
               
    
    #print("tf are ======",tfs)
    #print(idfs)
   






    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
