# A-Music-Search-Engine
The aim is to build a music search engine by scraping song lyrics data from genius.com using BeautifulSoup library and then using PyLucene and Bert to index the lyrics data. This will allow users to search for artist names and songs based on matching lyrics.

## Crawling Strategy
For Crawling we are taking the Artist name as an input and get the artist info from the Genius.com website. From this artist info object we acquire all the related URLs of the song sung by that artist. Lyrics and artist names are stored as a dictionary, which are then appended to an array one by one. Lyrics are then stored in a json file - scraped_songs.json.

## Libraries used
The following libraries have been used other than basic python standard libraries such as string, List etc.,

● BeautifulSoup: It is a Python library for pulling data out of HTML and XML files. It supports HTML parser. It transforms a HTML document into a tree of Python objects.

● Mapping: Specialized container data types called "collections-mapping" offer key-value mapping objects that resemble dicts.

● JSON and RE: It is used to search and manipulate strings from the JSON file provided as input.

● PyTorch: Open Source Library that forms the basis of AutoModel.

● StandardAnalyzer: Used for text data indexing and searching in general.

● Faiss: Used to quickly locate the most comparable songs by comparing the lyrics of a vast collection of songs that is represented as high-dimensional vectors. The similarity scores between the query vector and the vectors in the database can be calculated using the cosine similarity function.

● AutoTokenizer: NLP Library that supports a wide range of transformer based models like BERT.

● AutoModel: It offers a variety of tools and utilities for automating the process of creating and refining machine learning models and is built on top of the well-known PyTorch library.

● Lucene: Indexing and Retrieval of useful docs.

● IndexWriter: Builds and maintains the index of searchable documents.

● QueryParser: Accepts a user query as input and transforms it into a structured form that the search engine may use to retrieve pertinent documents.

● BM25Similarity: Used in information retrieval to rate how relevant a set of documents are to a given search query.

## EXECUTION INSTRUCTIONS –
a) For Web App –

     python3 app.py
     
b) For CMD –

BERT – python3 bert_index.py 

PYLUCENE – python3 pylucene.py
