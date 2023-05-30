# In order to print results on Command Prompt, Use this File!
import json
import faiss
import torch
from transformers import AutoTokenizer, AutoModel

# load song lyrics from JSON file
with open('scraped_songs.json', 'r') as f:
    data = json.load(f)

# initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-distilroberta-v1')
model = AutoModel.from_pretrained('sentence-transformers/all-distilroberta-v1')

query = input("Enter your query: ")

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
    summed = torch. sum(masked_embeddings, 1)
    summed_mask = torch.clamp(mask.sum(1), min=1e-9)
    mean_pooled = summed / summed_mask
    return mean_pooled[0] 


# Load the pre-trained index from disk
index = faiss.read_index("song_index.index")

# Convert the query to an embedding
query_embedding = convert_to_embedding(query, tokenizer, model)

# Search for similar songs
scores, indices = index.search(query_embedding.numpy()[None, :], 10)

# Print the most similar songs
for score, index in zip(scores[0], indices[0]):
    # if score<0:
    #     print('No match found')
    # else:
    song = data[index]
    print('Song:', song['lyrics'])
    print('Artist:', song['artist'])
    print('Title:', song['title'])
    print('URL:', song['url'])
    print('Similarity score:', score)
    print('-------------------------')
