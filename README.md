# Context Relevance App

The Context Relevance App is a Streamlit application that allows users to determine the relevance of citation sources based on a given response ID. It utilizes natural language processing techniques, including language detection, translation, and embedding generation, to calculate similarity scores between the response and its corresponding citation sources.

## Installation

To run the Context Relevance App on your local machine, please follow these steps:

1. Clone the GitHub repository:
   git clone (https://github.com/Rishav045/BeyondChats.git)
2. Navigate to the project directory:
   cd BeyondChats
3. Install the required dependencies using pip:
   pip install -r requirements.txt
4. Obtain an API key from OpenAI:
- Go to the OpenAI website (https://www.openai.com/) and sign up for an account.
- Generate an API key from your OpenAI account dashboard.
- Replace `"YOUR_API_KEY"` in the `data_preprocessing.py` file with your actual OpenAI API key.

5. Prepare the dataset:
- Run the `scraping.py` script to fetch data from the API and save it to `extracted.json`:
  ```
  python scraping.py
  ```
- Run the `data_preprocessing.py` script to preprocess the data and generate embeddings:
  ```
  python data_preprocessing.py
  ```
- The preprocessed data will be saved to `preprocessed_data.json`, and the embeddings will be saved to `embedding.json`.
- The `data_preprocessing.py` script will also create the final dataset file `final_dataset.json`.

## Usage

To use the Context Relevance App, follow these steps:

1. Make sure you have completed the installation steps mentioned above.

2. Run the Streamlit app:
   streamlit run streamlit.py
3. The app will open in your default web browser.

4. Enter the ID number of the response you want to analyze (between 1 and 124) in the text input field.

5. Adjust the similarity threshold using the slider if needed. The default threshold is set to 0.5.

6. The app will display the response text, relevant citation sources, and irrelevant citation sources based on the entered ID and similarity threshold.

7. The relevant citation sources will be marked with a green tick (✔) along with their similarity scores.

8. The irrelevant citation sources will be marked with a red cross (✖) along with their similarity scores.

9. The citation source links are clickable and will open in a new browser tab when clicked.

## Code-level Documentation

The Context Relevance App consists of the following Python scripts:

- `scraping.py`: This script fetches data from the API using the `requests` library and saves it to `extracted.json`.

- `data_preprocessing.py`: This script preprocesses the fetched data, translates non-English text to English using the `translate` library, generates embeddings using OpenAI's embedding model, and saves the preprocessed data and embeddings to `preprocessed_data.json` and `embedding.json`, respectively. It also creates the final dataset file `final_dataset.json`.

- `prepare_output.py`: This script defines functions to detect language, translate text, and retrieve relevant citation sources based on a given response ID and similarity threshold.

- `streamlit.py`: This script creates the Streamlit app user interface. It allows users to enter a response ID, adjust the similarity threshold, and displays the response text, relevant citation sources, and irrelevant citation sources based on the entered ID and threshold.

The code is well-documented with inline comments explaining the purpose and functionality of each section.

