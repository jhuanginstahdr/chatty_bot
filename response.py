import queue
import openai

"""
Aggregate the texts in text_queue and get a response
"""
def consume_text(text_q : queue.Queue):
    if not isinstance(text_q, queue.Queue):
        raise Exception(f'{text_q} is not type of {queue.Queue}')

    if text_q.empty():
        return
    
    print(f'aggregating {text_q.qsize()} number of messages')
    texts = []
    while not text_q.empty():
        texts.append(text_q.get())
    
    prompt = " ".join(texts)
    if not prompt:
        return
    
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "user", "content": prompt}])
    message = response["choices"][0]["message"]["content"]
    print(message)