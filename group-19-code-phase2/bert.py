# In order to print results on Web Page, Use this File!
import json
import faiss
import torch
from transformers import AutoTokenizer, AutoModel

# load song lyrics from JSON file
with open('scraped_songs.json', 'r',encoding='utf-8') as f:
    data = json.load(f)

# initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-distilroberta-v1')
model = AutoModel.from_pretrained('sentence-transformers/all-distilroberta-v1')

# query = input("Enter your query: ")

# Define a function to convert text to embeddings
def convert_to_embedding (text,tokenizer,model):

    # Tokenize the text and convert to PyTorch tensors
    tokens = {'input_ids': [], 'attention_mask': []}
    new_tokens = tokenizer.encode_plus (text, max_length=512,truncation=True, padding='max_length', return_tensors='pt')
    tokens ['input_ids'].append(new_tokens ['input_ids'] [0])
    tokens ['attention_mask'].append(new_tokens ['attention_mask'][0])
    tokens ['input_ids'] = torch.stack(tokens ['input_ids'])
    tokens ['attention_mask'] = torch. stack(tokens ['attention_mask'])
    
    # Generate embeddings from the model output
    with torch.no_grad():
        outputs = model (**tokens)
    embeddings = outputs. last_hidden_state
    attention_mask = tokens['attention_mask']
    mask = attention_mask.unsqueeze (-1) .expand(embeddings.size()). float ()
    masked_embeddings = embeddings * mask
    summed = torch.sum(masked_embeddings, 1)
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)
    mean_pooled = summed / summed_mask
    return mean_pooled[0] 

#COMMENTED as pretrained the model once and created the son_index.html file.
# Convert the lyrics to embeddings and add them to the FAISS index
# index = faiss.IndexFlatIP(768)
# for song in data:
#     lyrics = song['lyrics']
#     embedding = convert_to_embedding(lyrics, tokenizer, model)
#     embedding = embedding.numpy().reshape(1, -1) # Reshape to have two dimensions
#     index.add(embedding)

# # Save the index to disk
# faiss.write_index(index, "song_index.index")

# For running on command prompt
# index = faiss.read_index("song_index.index")

# query_embedding = convert_to_embedding(query, tokenizer, model)
# scores, indices = index.search(query_embedding.numpy()[None, :], 5)

# Print the most similar songs
# for score, index in zip(scores[0], indices[0]):
#     song = data[index]
#     print('Song:', song['lyrics'])
#     print('Artist:', song['artist'])
#     print('Title:', song['title'])
#     print('URL:', song['url'])
#     print('Similarity score:', score)
#     print('-------------------------')

# Define a function to perform a search using the pre-trained index
def bert_search(query):
    
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-distilroberta-v1')
    model = AutoModel.from_pretrained('sentence-transformers/all-distilroberta-v1')
    
    # Load the pre-trained index from disk
    index = faiss.read_index("song_index.index")

    # Convert the query to an embedding
    query_embedding = convert_to_embedding(query, tokenizer, model)
    
    # Search for similar songs
    scores, indices = index.search(query_embedding.numpy()[None, :], 8)
    res = []
    res1=[]
    
    # Collect the search results and their scores
    for score, index in zip(scores[0], indices[0]):
        res.append(data[index])
        res1.append(score)
    return res,res1