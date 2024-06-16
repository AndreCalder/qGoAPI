import json


def get_file_ext(uploaded_file_filename:str) -> str:
    return uploaded_file_filename.split('.')[-1]


def extract_json(response:str) -> dict:
  """""
  Extract the json object from the 
  """""

  if "```json\n" in response:

    start = "```json\n"
    end = "\n```"

    _string = response[response.find(start)+len(start):response.rfind(end,0)]
    #_string = _string[:_string.find(end)]
    #_string = _string.replace('\n',' ')

  else: _string = response

  try:
    return json.loads(rf'{_string}')
  except Exception as e:
    return f'ERROR WHEN TRYING TO EXTRACT JSON QUIZ FROM LLM RESPONSE. // {e} // \n\n_string:\n\n{_string}'