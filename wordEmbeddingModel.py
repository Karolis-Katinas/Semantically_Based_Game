import gensim
import pandas as pd


file_paths = ('AMAZON_FASHION_5.json','Automotive.json',
'Arts_Crafts_and_Sewing_5.json', 'All_Beauty_5.json','Appliances.json', 
'CDs_and_Vinyl.json', 'Cell_Phones_and_Accessories_5.json','Books_5.json',
'Clothing_Shoes_and_Jewelry_5.json', 'Digital_Music_5.json', 'Electronics_5.json',
'Electronics_5.json', 'Grocery_and_Gourmet_Food.json', 'Home_and_Kitchen_5.json',
'Industrial_and_Scientific_5.json', 'Kindle_Store.json', 'Luxury_Beauty.json',
'Magazine_Subscriptions.json', 'Movies_and_TV.json', 
'Office_Products.json', 'Patio_Lawn_and_Garden.json', 'Pet_Supplies.json',
'Prime_Pantry.json', 'Software.json', 'Sports_and_Outdoors.json',
'Tools_and_Home_Improvement.json', 'Toys_and_Games.json', 'Video_Games.json')
df = pd.read_json('D:/Data/Musical_Instruments.json', lines=True)
  
df
review_text = df.reviewText.astype(str).apply(gensim.utils.simple_preprocess)


model = gensim.models.Word2Vec(
    window=5,
    vector_size=300,
    min_count=10,
    workers=4,
)
model.build_vocab(review_text, progress_per=1000)
model.train(review_text, total_examples=model.corpus_count, epochs=model.epochs)
model.save("./model")

for file in file_paths:
    ChunkSize = 500000
    print(file)
    for chunk in pd.read_json(file, lines=True, chunksize=ChunkSize):
        review_text = chunk.reviewText.astype(str).apply(gensim.utils.simple_preprocess)
        model.build_vocab(review_text, update=True)
        model.train(review_text, total_examples=model.corpus_count, epochs=1)
        model.save("./model")
