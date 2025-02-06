import ollama
import requests
import duckduckgo_search
import json
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import re 


text_shortener_prompt = '''You are not an AI LLm model, you'r work is to shorten the text that I provide you. and do not say anything else, just shorten the text. DD NOT ADD ANYTHING BY YOURSELF, DO NOT GIVE ANY EXPLENATION!, Just shorten the text ''' 
def text_shortener(text, model='deepseek-r1:1.5b'):
    text_shortened = ollama.chat(
                model=model,
                messages=[{'role': 'system', 'content':text_shortener_prompt},{'role': 'user', 'content': text}]
            )
    result = re.sub(r'<think>.*?</think>', '', text_shortened['message']['content'], flags=re.DOTALL)

    return result



def search_needed(query, model='deepseek-r1:8b'):
    data_file_path = '/home/tahmid/programming file/virtual assistant/data.json'  # Store path as variable

    try:
        with open(data_file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # Handle the case where the file doesn't exist yet
        data = {"messages_needed": []}

    data["messages_needed"].append({'role': 'user', 'content': query})

    user_indices = [i for i, x in enumerate(data["messages_needed"]) if x['role'] == 'user']

    if len(user_indices) >= 5:
        # Remove the oldest user message and its corresponding response (if any)
        oldest_user_index = user_indices[0]
        del data["messages_needed"][oldest_user_index]

        #remove the response after the deleted user message if it exists
        if oldest_user_index < len(data["messages_needed"]) and data["messages_needed"][oldest_user_index]['role'] == 'assistant':
            del data["messages_needed"][oldest_user_index]


    try:
        model_response = ollama.chat(model=model, messages=data["messages_needed"])
        response_content = re.sub(r"<think>.*?</think>\s*", "", model_response['message']['content'], flags=re.DOTALL)

        #Store the assistant's response
        data["messages_needed"].append({'role':'assistant','content': response_content})

    except Exception as e: #Catch potential Ollama errors
        print(f"Error communicating with Ollama: {e}")
        return "Sorry, I encountered an error."

    with open(data_file_path, "w") as f:
        json.dump(data, f, indent=4)

    return response_content



# chat_history = []

# def search_web(query):
#     headers = {
#         "User-Agent": (
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#             "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#         )
#     }

#     search_url = f'https://duckduckgo.com/html/?q={query}'
    
#     try:
#         response = requests.get(search_url, headers=headers)
#         response.raise_for_status()  # Check for HTTP errors
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching search results: {e}")
#         return []
    
#     soup = BeautifulSoup(response.text, 'html.parser')
#     links = []

#     for a_tag in soup.find_all('a', href=True):
#         link = a_tag['href']
#         if link.startswith('/l/?kh='):
#             link = link.split('uddg=')[1]  # Extract actual URL
#         if link.startswith('http'):
#             links.append(link)
    
#     return links

def Get_text_from_web(url):
    # Get the responce from the web 
    response = requests.get(url)
    html_content = response.text
    
    # get the html content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get fetch the text
    text = soup.get_text()

    # Return text 
    return text

def Ollama(message, model="deepseek-r1:8b"):
    data_file_path = '/home/tahmid/programming file/virtual assistant/data.json'  # Store path as variable

    try:
        with open(data_file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # Handle the case where the file doesn't exist yet
        data = {"messages_main_AI": []}

    data["messages_main_AI"].append({'role': 'user', 'content': message})
    data["messages_needed"].append({'role': 'user', 'content': message})

    user_indices = [i for i, x in enumerate(data["messages_main_AI"]) if x['role'] == 'user']

    if len(user_indices) >= 5:
        # Remove the oldest user message and its corresponding response (if any)
        oldest_user_index = user_indices[0]
        del data["messages_main_AI"][oldest_user_index]

        #remove the response after the deleted user message if it exists
        if oldest_user_index < len(data["messages_main_AI"]) and data["messages_main_AI"][oldest_user_index]['role'] == 'assistant':
            del data["messages_main_AI"][oldest_user_index]


    try:
        model_response = ollama.chat(model=model, messages=data["messages_main_AI"])
        response_content = model_response['message']['content']

        #Store the assistant's response
        data["messages_main_AI"].append({'role':'assistant','content': response_content})

    except Exception as e: #Catch potential Ollama errors
        print(f"Error communicating with Ollama: {e}")
        return "Sorry, I encountered an error."

    with open(data_file_path, "w") as f:
        json.dump(data, f, indent=4)

    return re.sub(r"<think>.*?</think>\s*", "", response_content, flags=re.DOTALL)




def scrap_text(query):
    results = DDGS().text(query,region='bd.en', max_results=3)
    context = []
    for result in results:
        print('-'*50)
        print(f"Getting_information from: {result['href']}")
        print('-'*50)
        info = Get_text_from_web(result['href'])
        print("Information fetched.....\n\n")

        print("Shortninig the text")
        shorten_text = text_shortener(info)
        print("Text shortened")
        print('-'*60)
        
        context.append(shorten_text)
 
    return context
