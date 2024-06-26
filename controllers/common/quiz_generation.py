import vertexai
from vertexai.generative_models import GenerativeModel


def get_quiz(prompt:str, system_instrtuction, GLOBAL_APP_CONFIG):

    vertexai.init(project=GLOBAL_APP_CONFIG['PROJECT_ID'], location=GLOBAL_APP_CONFIG['LOCATION'])

    model = GenerativeModel(GLOBAL_APP_CONFIG['LLM']['MODEL'],
                            system_instruction=system_instrtuction,
                            generation_config={
                                'temperature':GLOBAL_APP_CONFIG['LLM']['TEMPERATURE']
                            })

    #chat = model.start_chat(response_validation=False)
    #response = chat.send_message(prompt)
    print("Processing document...")
    response = model.generate_content(prompt)
    print("Response: ")
    print(response)
    response_txt = response.text

    return response_txt