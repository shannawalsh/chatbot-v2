from openai import OpenAI
import tiktoken
import logging
import datetime

log = logging.getLogger("token_count")
logger = logging.getLogger(__name__)
logging.basicConfig(filename='token_count.log', level= logging.INFO, encoding='utf-8')


client = OpenAI()


# accepts a preferred model and a list of messages
# makes chat completions API call
# returns the response message content
def get_api_chat_response_message(model, messages):
    # make the API call
    api_response = client.chat.completions.create(
        model = model,
        messages = messages,
    )
    # return the response
    return api_response

# extract & return response text
def get_response_message(response):
    return response.choices[0].message.content

#extract & return the total number of tokens
def get_response_total_tokens(response):
    return response.usage.total_tokens  

#extract & return the total number of input tokens
def get_response_total_input_tokens(response):
    return response.usage.prompt_tokens

#extract & return the total number of output tokens
def get_response_total_output_tokens(response):
    return response.usage.completion_tokens

model = "gpt-3.5-turbo"
encoding = tiktoken.encoding_for_model(model)
token_input_limit = 12289
total_token_count = 0
total_input_token_count = 0
total_output_token_count = 0

chat_history = []

user_input = ""

while True:
    if (user_input == ""):
        user_input = input("Chatbot: Hey there, I'm here to help. Type exit to end our chat. Otherwise, nice to meet you. What is your name? ")
    else:
        user_input = input("You: ")
    if user_input.lower() == "exit":
        log.info("\nDate: " + str(datetime.datetime.now()) + "\nTotal tokens: " + str(total_token_count) + "\nTotal Input tokens: " + str(total_input_token_count) + "\nTotal Output tokens: " + str(total_output_token_count) + "\n\n")
        exit()
    
    token_count = len(encoding.encode(user_input))
             
    if (token_count > token_input_limit):
        print("Your prompt is too long. Please try again.")
        continue
    
    chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = get_api_chat_response_message(model, chat_history)
    response_message = get_response_message(response)
    
    response_total_tokens = get_response_total_tokens(response)
    total_token_count += response_total_tokens
    
    print("Chatbot: ", response)

    chat_history.append({
        "role": "assistant",
        "content": user_input
    })