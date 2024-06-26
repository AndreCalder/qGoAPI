from controllers.common.config import *
from controllers.common.utils import *
from controllers.common.doc_loading import *
from controllers.common.quiz_generation import *

from tempfile import NamedTemporaryFile



def single_file_basic(request):
    # ---------------------------
    title           =   request.form.get('title')
    n_questions     =   request.form.get('n_questions')
    q_type          =   request.form.get('q_type')
    difficulty      =   request.form.get('difficulty')
    start_page      =   request.form.get('start')
    end_page        =   request.form.get('end')
    # uploaded_file = request.files['file'] --------------------- REMOVE COMMENT FOR API TEST
    uploaded_file   =   request.files['file'] # --------------------- COMMENT FOR API TEST
    # ---------------------------

    config = CONFIG['SINGLE_FILE_BASIC']
    #----------------------------

    prompt = config['PROMPT']
    system_instrtuction = config['SYSTEM_INSTRUCTION']

    match q_type.lower():
        case 'open_q': 
            q_type = 'OPEN ENDED'
            json_structure = config['JSON_STRUCTURE_OPEN_Q']
            json_example = config['JSON_EXAMPLE_OPEN_Q']
        case 'multi_choice':
            q_type = 'MULTIPLE CHOICE'
            json_structure = config['JSON_STRUCTURE_MULTI_CHOICE']
            json_example = config['JSON_EXAMPLE_MULTI_CHOICE']
        case 'any':
            q_type = 'OPEN ENDED AND MULTIPLE CHOICE'

    if uploaded_file and uploaded_file.filename != '':     
        file_ext = get_file_ext(uploaded_file.filename) # --------------------- REMOVE COMMENT FOR API TEST
        #file_ext = get_file_ext(rf'{uploaded_file}') # --------------------- COMMENT FOR API TEST
        with NamedTemporaryFile() as temp_file:
            uploaded_file.save(temp_file)
            temp_file.seek(0)
            doc = load_doc(file_ext, temp_file.name)

    content = ''

    for d in doc:
        page = int(d.metadata.get('page'))
        if request.form.get('content') != 'document':
            if page >= int(start_page) and page <= int(end_page):
                content+=d.page_content
            elif page > int(end_page):
                break
        else:
            content+=d.page_content
    print(content)
    prompt = prompt.format(n_questions=n_questions,
                           q_type=q_type,
                           difficulty=difficulty,
                           content=content,
                           json_structure=json_structure,
                           json_example=json_example)
    
    valid_json = False
    retry_count = 0
    while not valid_json and retry_count <= CONFIG['MAX_RETRY_COUNT']:
    
        llm_response = get_quiz(prompt, system_instrtuction, GLOBAL_APP_CONFIG)
        quiz_json = extract_json(response=llm_response)

        if isinstance(quiz_json, dict):
            quiz_json['title']  =   title
            valid_json          =   True
            status              =   'SUCCESS',
            description         =   'QUIZ SUCCESSFULLY CREATED.'
        else: 
            print("Retrying...")
            retry_count += 1
            if retry_count > CONFIG['MAX_RETRY_COUNT']:
                status = 'ERROR'
                description = f'MAX RETRY COUNT ({CONFIG['MAX_RETRY_COUNT']}) EXCIDEED.'
                break

    return {'status':status,
            'description':description,
            'llm_response':llm_response, 
            'quiz_json':quiz_json,
            'retry_count':retry_count}