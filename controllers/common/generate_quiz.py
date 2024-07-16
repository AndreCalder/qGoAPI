import math
from controllers.common.config import *
from controllers.common.grading_config import *
from controllers.common.utils import *
from controllers.common.doc_loading import *
from controllers.common.quiz_generation import *
from tempfile import NamedTemporaryFile

def chunk_text(text, chunk_size):
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]
        
def generateQuizPrompt(n_questions, q_type, difficulty, language, content, json_structure, json_example):
    config = QUIZGONFIG['SINGLE_FILE_BASIC']
    prompt = config['PROMPT']
    
    prompt = prompt.format(
            n_questions=str(n_questions),
            q_type=q_type,
            difficulty=difficulty,
            language=language,
            content=content,
            json_structure=json_structure,
            json_example=json_example)
    
    return prompt
    
def processQuizPrompt(prompt, system_instrtuction, chunk_questions):
    valid_json = False
    retry_count = 0
    print(valid_json, retry_count)
    while not valid_json and retry_count <= QUIZGONFIG['MAX_RETRY_COUNT']:
        llm_response, chat = get_quiz(prompt, system_instrtuction, GLOBAL_APP_CONFIG)
        quiz_json = extract_json(response=llm_response)

        if isinstance(quiz_json, dict):
            _correct_question_count = False
            while not _correct_question_count:
                if not correct_question_count(n_questions=int(chunk_questions), quiz_json=quiz_json):
                    if int(chunk_questions) > len(quiz_json['quiz']):
                        _llm_response = ask_for_missing_questions(chat=chat)
                        _quiz_json = extract_json(response=_llm_response)
                        if isinstance(_quiz_json, dict):
                            quiz_json['quiz'].extend(_quiz_json['quiz'])
                            llm_response += f'ASK_FOR_MISSING_QUESTIONS: {_llm_response}'
                    else: 
                        quiz_json['quiz'] = quiz_json['quiz'][:int(chunk_questions) + 1]
                else:
                    valid_json             =   True
                    status                 =   'SUCCESS',
                    description            =   'QUIZ SUCCESSFULLY CREATED.'
                    _correct_question_count =   True
                    return quiz_json['quiz']
        else: 
            retry_count += 1
            print(retry_count)
            if retry_count > QUIZGONFIG['MAX_RETRY_COUNT']:
                status = 'ERROR'
                description = f"MAX RETRY COUNT ({QUIZGONFIG['MAX_RETRY_COUNT']}) EXCEDEED."
                break

def single_file_basic(request):
    # ---------------------------
    title           =   request.form.get('title')
    n_questions     =   request.form.get('n_questions')
    q_type          =   request.form.get('q_type')
    difficulty      =   request.form.get('difficulty')
    start_page      =   request.form.get('start')
    end_page        =   request.form.get('end')
    language        =   request.form.get('language')
    # uploaded_file = request.files['file'] --------------------- REMOVE COMMENT FOR API TEST
    uploaded_file   =   request.files['file'] # --------------------- COMMENT FOR API TEST
    # ---------------------------

    config = QUIZGONFIG['SINGLE_FILE_BASIC']
    #----------------------------

    prompt = config['PROMPT']
    system_instrtuction = config['SYSTEM_INSTRUCTION']

    if q_type.lower() == 'open_q':
            q_type = 'OPEN ENDED'
            json_structure = config['JSON_STRUCTURE_OPEN_Q']
            json_example = config['JSON_EXAMPLE_OPEN_Q']
    elif q_type.lower() ==  'multi_choice':
            q_type = 'MULTIPLE CHOICE'
            json_structure = config['JSON_STRUCTURE_MULTI_CHOICE']
            json_example = config['JSON_EXAMPLE_MULTI_CHOICE']
    else:
            q_type = 'OPEN ENDED AND MULTIPLE CHOICE'
    
    if uploaded_file and uploaded_file.filename != '':     
        file_ext = get_file_ext(uploaded_file.filename) # --------------------- REMOVE COMMENT FOR API TEST
        
        #file_ext = get_file_ext(rf'{uploaded_file}') # --------------------- COMMENT FOR API TEST
        with NamedTemporaryFile() as temp_file:
            uploaded_file.save(temp_file)
            temp_file.seek(0)
            doc = load_doc(file_ext, temp_file.name)
    
    content = ''
    
    if file_ext == 'pptx':
        for d in doc:
            content+=d.page_content
    else:
        for d in doc:
            page = int(d.metadata.get('page'))
            if request.form.get('content') != 'document':
                if page >= int(start_page) and page <= int(end_page):
                    content+=d.page_content
                elif page > int(end_page):
                    break
            else:
                content+=d.page_content
                
    chunk_size = 12500
    chunks = list(chunk_text(content, chunk_size))
    chunk_questions = math.ceil(int(n_questions)/len(chunks))
    prompts = []
    
    print(language)
    
    for chunk in chunks:
        prompt = generateQuizPrompt(chunk_questions, q_type, difficulty, language, chunk, json_structure, json_example)
        prompts.append(prompt)
    quiz_parts = []
    print(len(chunks), len(prompts))
    for prompt in prompts:
        try:
            prompt_response = processQuizPrompt(prompt, system_instrtuction, chunk_questions)     
            quiz_parts = quiz_parts + prompt_response 
        except:
            print("ERROR")
    
    for i in range(0, len(quiz_parts)-1):
        quiz_parts[i]['question_id']= i+1
    
    status                 =   'SUCCESS',
    description            =   'QUIZ SUCCESSFULLY CREATED.'
    
    return {'status':status,
            'description':description,
            'quiz_json':
                {
                    'title': title,
                    'language': language,
                    'quiz': quiz_parts    
                }}
    
def grade_answers(request):

    config = GRADE_CONFIG['ANSWER_CHECK']
    #----------------------------

    prompt = config['PROMPT']
    system_instrtuction = config['SYSTEM_INSTRUCTION']
    
    json_structure = config['JSON_STRUCTURE']
    json_example = config['JSON_EXAMPLE']
    content_structure = config['CONTENT_STRUCTURE']
    
    prompt = prompt.format(
                        content=request.json['answers'],
                        content_structure=content_structure,
                        grade_json_structure=json_structure,
                        grade_json_example=json_example)
    
    valid_json = False
    retry_count = 0
    
    while not valid_json and retry_count <= QUIZGONFIG['MAX_RETRY_COUNT']:
    
        llm_response, chat = get_quiz(prompt, system_instrtuction, GLOBAL_APP_CONFIG)
        graded_answers = extract_json(response=llm_response)
        if isinstance(graded_answers, dict):
            valid_json             =   True
            status                 =   'SUCCESS',
            description            =   'ANSWERS GRADED.'
            break  
        else: 
            retry_count += 1
            if retry_count > QUIZGONFIG['MAX_RETRY_COUNT']:
                status = 'ERROR'
                description = f"MAX RETRY COUNT ({QUIZGONFIG['MAX_RETRY_COUNT']}) EXCEDEED."
                break

    return {'status':status,
            'description':description,
            'llm_response':llm_response, 
            'graded_answers':graded_answers,
            'retry_count':retry_count}