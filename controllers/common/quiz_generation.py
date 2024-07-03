import vertexai
from vertexai.generative_models import GenerativeModel


def get_quiz(prompt:str, system_instrtuction, GLOBAL_APP_CONFIG):

    vertexai.init(project=GLOBAL_APP_CONFIG['PROJECT_ID'], location=GLOBAL_APP_CONFIG['LOCATION'])

    model = GenerativeModel(GLOBAL_APP_CONFIG['LLM']['MODEL'],
                            system_instruction=system_instrtuction,
                            generation_config={
                                'temperature':GLOBAL_APP_CONFIG['LLM']['TEMPERATURE']
                            })

    
    print("Processing document...")
    chat = model.start_chat(response_validation=False)
    response = chat.send_message(prompt)
    # response = model.generate_content(prompt)
    print("Response: ")
    print(response)
    response_txt = response.text

    return response_txt, chat

def ask_for_missing_questions(chat):
    prompt = """I will need more questions with the same structure you used in your previous answer.
    Continue the question count starting with the last question_id you provided. 
    IMPORTANT: Create totally different questions from the ones in your previous answer.
    IMPORTANT: Keep using the JSON Structure I provided in my first prompt.
    IMPORTANT: Always summarize the answers to keep them the most short and concise possible.
"""
    response = chat.send_message(prompt)
    response_txt = response.text
    return response_txt