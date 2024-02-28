
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

# %%
import pandas as pd

# %% [markdown]
# # Load Data

# %%
# read the data
df = pd.read_csv("./data/cleantech_media_dataset_v2_2024-02-23.csv")
df_eval = pd.read_csv("./data/cleantech_rag_evaluation_data_2024-02-23.csv")

# %%
df.head()

# %%
df_eval.head()
