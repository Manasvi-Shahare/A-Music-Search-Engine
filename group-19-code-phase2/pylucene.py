import logging, sys
logging.disable(sys.maxsize)

import lucene
import time
import os
import json
from org.apache.lucene.store import SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
#from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import BM25Similarity


topkdocs = []

#function to create lucene indexing
def create_index(dir):
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
            
        # create a directory, standard analyzer, index writer configuration, mode and index writer
        store = SimpleFSDirectory(Paths.get(dir)) 
        analyzer = StandardAnalyzer()
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        # define field types
        artistType = FieldType()
        artistType.setStored(True)
        artistType.setTokenized(False)

        lyricsType = FieldType()
        lyricsType.setStored(True)
        lyricsType.setTokenized(True)
        lyricsType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        urlType = FieldType()
        urlType.setStored(True)
        urlType.setTokenized(False)
        
        titleType = FieldType()
        titleType.setStored(True)
        titleType.setTokenized(False)

         # add documents to the index
        for sample in sample_doc:
            artist = sample['artist']
            lyrics = sample['lyrics']
            url = sample['url']
            title = sample['title']
            doc = Document()
            doc.add(Field('Artist', str(artist), artistType))
            doc.add(Field('Lyrics', str(lyrics), lyricsType))
            doc.add(Field('url', str(url), urlType))
            doc.add(Field('title', str(title), titleType))
            writer.addDocument(doc)
        writer.close()
    except Exception as e:
        print(f"Error creating index: {e}")


def retrieve(storedir, query):
    try:
        #create a directory for search and an index searcher
        searchDir = NIOFSDirectory(Paths.get(storedir))
        searcher = IndexSearcher(DirectoryReader.open(searchDir))

        fields = ['Lyrics', 'title']
        ## create a parser to parse the query
        #query = MultiFieldQueryParser.parse(parser, query)
        parser = MultiFieldQueryParser(fields, StandardAnalyzer())
        parsed_query = MultiFieldQueryParser.parse(parser,query)
        print(parsed_query)

         # retrieve top k documents
        topDocs = searcher.search(parsed_query, 10).scoreDocs
        #topkdocs = []
        # append document information to the topkdocs list
        for hit in topDocs:
            doc = searcher.doc(hit.doc)
            topkdocs.append({
                "score": hit.score,
                "Artist": doc.get("Artist"),
                "Title": doc.get("title"),
                "Url": doc.get("url"),
                "lyrics": doc.get("Lyrics")
                
            })
         # print the top k documents
        for doc in topkdocs:
            print("Score: ", doc['score'])
            print("Artist: ", doc['Artist'])
            print("Title: ", doc['Title'])
            print("URL: ", doc['Url'])
            print("Lyrics: ", doc['lyrics'])
            print("\n") 
        #print(topkdocs)
    except Exception as e:
        print(f"Error retrieving documents: {e}")

def pylucene_search(query):
    retrieve('sample_lucene_index/', query)
    res=[]
    res1=[]
    # print("Score: ", doc['score'])
    # print("Artist: ", doc['Artist'])
    # print("Title: ", doc['Title'])
    # print("URL: ", doc['Url'])
    # print("Lyrics: ", doc['lyrics'])
    # print("\n")
    for doc in topkdocs:
        res.append(doc)
        res1.append(doc['score'])
    return res,res1
        
  

f = open('scraped_songs.json')
sample_doc = json.load(f)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
create_index('sample_lucene_index/')
u_input = input("Enter a query: ")
retrieve('sample_lucene_index/', u_input)
