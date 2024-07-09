from openai import OpenAI

client = OpenAI()

# accepts a preferred model and a list of messages
# makes chat completions API call
# returns the response message content
def get_api_chat_response_message(model, messages):
    # make the API call
    api_response = client.chat.completions.create(
        model = model,
        messages = messages
    )

    # extract the response text
    response_content = api_response.choices[0].message.content

    # return the response text
    return response_content

model = "gpt-3.5-turbo"

chat_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = get_api_chat_response_message(model, chat_history)
    
    print("Chatbot: ", response)

    chat_history.append({
        "role": "assistant",
        "content": user_input
    })