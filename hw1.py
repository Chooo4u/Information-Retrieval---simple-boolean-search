# homework 1
# goal: tokenize, index, boolean query
# exports: 
#   student - a populated and instantiated ir4320.Student object
#   Index - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents


# ########################################
# first, create a student object
# ########################################

import cs525
import PorterStemmer
import glob
import re

MY_NAME = "Chuchen Dai"
MY_ANUM  = 326054096 # put your WPI numerical ID here
MY_EMAIL = "cdai2@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = [     ]

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "I do not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs525.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# ########################################
# now, write some code
# ########################################

# our index class definition will hold all logic necessary to create and search
# an index created from a directory of text files 
class Index(object):
    def __init__(self):
        # _inverted_index contains terms as keys, with the values as a list of
        # document indexes containing that term
        self._inverted_index = {}
        # _documents contains file names of documents
        self._documents = []
        # example:
        #   given the following documents:
        #     doc1 = "the dog ran"
        #     doc2 = "the cat slept"
        #   _documents = ['doc1', 'doc2']
        #   _inverted_index = {
        #      'the': [0,1],
        #      'dog': [0],
        #      'ran': [0],
        #      'cat': [1],
        #      'slept': [1]
        #      }


    # index_dir( base_path )
    # purpose: crawl through a nested directory of text files and generate an
    #   inverted index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: glob.glob()
    # parameters:
    #   base_path - a string containing a relative or direct path to a
    #     directory of text files to be indexed
    def index_dir(self, base_path):
        files=glob.glob(base_path+'*')
        num_files_indexed = len(files) # number of files in the folder

        position = []
        diction = {}
        for i in range(len(files)):
            fidx = str(files[i]).strip('.txt').strip('data/')
            self._documents.append(fidx) # list the collection

            outfile = open(files[i])
            textlines=outfile.read().splitlines()
            stemmed_tokens = Index.stemming(self, Index.tokenize(self, textlines))
            for s in stemmed_tokens:
                if s in diction:
                    diction[s].append(i)
                else:
                    diction[s] = [i]
        self._inverted_index = diction # create the inverted index
        # print(diction)
        # print(self._documents)
        return num_files_indexed

    # tokenize( text )
    # purpose: convert a string of terms into a list of tokens.        
    # convert the string of terms in text to lower case and replace each character in text, 
    # which is not an English alphabet (a-z) and a numerical digit (0-9), with whitespace.
    # preconditions: none
    # returns: list of tokens contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self,text):
        wordlst=[]
        for s in text:
            if s != "":
                wordlst.append(s.split(" "))
        words = eval('[%s]' % repr(wordlst).replace('[', ' ').replace(']', ' '))

        tokens = []
        for w in words:
            if re.match("^[A-Za-z0-9]*$", w):
                # if w not in tokens:
                tokens.append(w)
            else:
                    # print(w)
                    for i in range(len(w)):
                        if str(w[i]).isalnum() is False:
                            w = w.replace(w[i],' ')
                            # w = re.sub(str(w[i]), ' ', w)
                            # print(w)
                    tokens.extend(w.split(' '))

        tokens = list(set(tokens))
        tokens =  [t.lower() for t in tokens]
        while '' in tokens:
            tokens.remove('')

        return tokens

    # purpose: convert a string of terms into a list of tokens.        
    # convert a list of tokens to a list of stemmed tokens,     
    # preconditions: tokenize a string of terms
    # returns: list of stemmed tokens
    # parameters:
    #   tokens - a list of tokens
    def stemming(self, tokens):
        if __name__ == '__main__':
            stemmed_tokens = []
            for i in tokens:
                stemmed_i = PorterStemmer.PorterStemmer().stem(i,0,(len(i)-1))
                stemmed_tokens.append(stemmed_i)
        files = self._documents
        return stemmed_tokens
    
    # boolean_search( text )
    # purpose: searches for the terms in "text" in our corpus using logical OR or logical AND. 
    # If "text" contains only single term, search it from the inverted index. If "text" contains three terms including "or" or "and", 
    # do OR or AND search depending on the second term ("or" or "and") in the "text".  
    # preconditions: _inverted_index and _documents have been populated from
    #   the corpus.
    # returns: list of document names containing relevant search results
    # parameters:
    #   text - a string of terms
    def boolean_search(self, text):
        results = []
        if " " not in text:
            stemmed_text = Index.stemming(self, Index.tokenize(self, [text]))[0]
            resultsIdx = self._inverted_index[stemmed_text]
            for i in resultsIdx:
                results.append(self._documents[i])
        else:
            txtlst = text.split(' ')
            stemmed_text1 = Index.stemming(self, Index.tokenize(self, [txtlst[0]]))[0]
            stemmed_textBoo = Index.stemming(self, Index.tokenize(self, [txtlst[1]]))[0]
            stemmed_text2 = Index.stemming(self, Index.tokenize(self, [txtlst[2]]))[0]
            # print(stemmed_textBoo)
            resulutsidx1 = self._inverted_index[stemmed_text1]
            resulutsidx2 = self._inverted_index[stemmed_text2]
            # print(resulutsidx1,resulutsidx2)
            if stemmed_textBoo == 'and':
                # resultsAnd = [i for i in resulutsidx1 if i in resulutsidx2]
                resultsAnd = set(resulutsidx1) & set(resulutsidx2)

                for i in resultsAnd:
                    results.append(self._documents[i])

            elif stemmed_textBoo == 'or':
                # resultsOr = list(set(resulutsidx1).union(set(resulutsidx2)))
                resultsOr = set(resulutsidx1) | set(resulutsidx2)
                for i in resultsOr:
                    results.append(self._documents[i])

        return results
    

# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = Index()
    print("starting indexer")
    num_files = index.index_dir('data/')
    print("indexed %d files" % num_files)
    for term in ('football', 'mike', 'sherman', 'mike OR sherman', 'mike AND sherman'):
        results = index.boolean_search(term)
        print("searching: %s -- results: %s" % (term, ", ".join(results)))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

