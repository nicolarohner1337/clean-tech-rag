
# %% [markdown]
# # Check if all  Prerequisites are satisfied

# %%
# check if .venv is present if not run poetry install
import os

if not os.path.exists(".venv"):
    os.system("poetry install")
    print("poetry install ran")

# now check if .venv is activated
if not os.getenv("VIRTUAL_ENV"):
    os.system("source .venv/bin/activate")
    print("venv activated")

# %%
import os

if not os.path.exists(".env"):
    print("The .env file does not exist")
    # Use raise Exception("The .env file does not exist") if you want to raise an error instead
else:
    from dotenv import load_dotenv

    load_dotenv()  # take environment variables from .env.
    print("Loaded .env file")

# %%
import os

# check if data folder exists
if not os.path.exists("./data/"):
    import kaggle

    try:
        kaggle.api.authenticate()
    except:
        print(
            "Kaggle API not authenticated. Please add KAGGLE_username and KAGGLE_key to .env file"
        )
        exit()

    os.makedirs("./data/", exist_ok=True)
    kaggle.api.dataset_download_files(
        "jannalipenkova/cleantech-media-dataset", path="./data/", unzip=True
    )

# %% [markdown]
# # Import Libraries
# %%
import pandas as pd
from llama_index.core.evaluation import generate_question_context_pairs
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.evaluation import generate_question_context_pairs
from llama_index.core.evaluation import RetrieverEvaluator
from llama_index.llms.openai import OpenAI

# %% [markdown]
# # Load Data

# %%
# read the data
df = pd.read_csv("./data/cleantech_media_dataset_v2_2024-02-23.csv", index_col=0)
df_eval = pd.read_csv("./data/cleantech_rag_evaluation_data_2024-02-23.csv", index_col=0)
#  %% 
#column content is a list of Nodes so we need to parse it and explode it
# change the column content to a list of strings
df["content"] = df["content"].apply(eval)
df = df.explode("content").reset_index(drop=True)

# %%
#select where title The Power of Science and Innovation
df[df["title"] == "The Power of Science and Innovation"]

# %%
df_eval.head()

# %%
# parse dataframe 
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.file import CSVReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.schema import TextNode
import chromadb
import asyncio

# loads BAAI/bge-small-en-v1.5
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model

COLLECTION_NAME = "bge-small-en"
# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")
# create collection
chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# %%
#check if chroma_collection is empty
if chroma_collection.count() == 0:
    #create nodes from the dataframe the content is a list of strings so the content of nodes is predefined
    nodes = [
        TextNode(
            id=index,
            text=row.content,
            metadata={"title": row.title, "domain": row.domain, "date": row.date, "url": row.url},
        )
        for index, row in df.iterrows()
    ]
    #Only use for saving the vectors
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    print("Nodes created and saved", len(nodes))


# load your index from stored vectors
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context
)
# %%

# create a query engine
# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,
)
#test the retriever
chunks = retriever.retrieve("What is the EU’s Green Deal Industrial Plan?")
for node in chunks:
    print(node) 
# %%
from llama_index.core.evaluation import RetrieverEvaluator


retriever_evaluator = RetrieverEvaluator.from_metric_names(
    metric_names=["hit_rate", "mrr"],
    retriever=retriever
)
#TODO: fix this wont work in jupyter probably works with %autoawait asyncio
retriever_evaluator.aevaluate_dataset()
