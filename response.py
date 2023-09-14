import queue
import openai

"""
Aggregate the texts in text_queue and get a response
"""
def generate_response(prompt : str):    
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": prompt}])
    message = response["choices"][0]["message"]["content"]
    print(message)