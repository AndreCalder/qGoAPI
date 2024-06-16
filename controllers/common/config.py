# single_file_basic()

SINGLE_FILE_BASIC_PROMPT = """
<REQUEST>
CREATE {n_questions} {q_type} TYPE QUESTIONS, ALL OF {difficulty} DIFFICULTY AND ONLY USING THE GIVEN CONTENT:
</REQUEST>

<CONTENT>
{content}
</CONTENT>


THE EXPECTED OUTPUT SHOULD BE A JSON OBJECT WITH THE FOLLOWING STRUCTURE:
<OUTPUT STRUCTURE>
{json_structure}
</OUTPUT STRUCTURE>

HERE IS AN EXAMPLE OF HOW THE JSON OBJECT SHOULD LOOK LIKE:
<OUTPUT EXAMPLE>
{json_example}
</OUTPUT EXAMPLE>
"""

SINGLE_FILE_BASIC_JSON_STRUCTURE_OPEN_Q = """
{
"quiz":

    [

        {
        "question_id":1,
        "question":str,
        "answer":str,
        "justification":str
        },

        {
        "question_id":2,
        "question":str,
        "answer":str,
        "justification":str
        },

        {
        "question_id":3,
        "question":str,
        "answer":str,
        "justification":str
        }

    ]
}
"""

SINGLE_FILE_BASIC_JSON_EXAMPLE_OPEN_Q = """
{
"quiz":

    [

        {
        "question_id":1,
        "question":"What is the difference between Artificial Intelligence (AI) and Machine Learning (ML)?",
        "answer":"AI aims to create intelligent machines, while ML enables machines to learn from data without explicit programming.",
        "justification":"AI: The broader field of computer science concerned with creating intelligent machines that can perform tasks typically requiring human intelligence.
ML: A subset of AI that focuses on enabling machines to learn from data without explicit programming."
        },

        {
        "question_id":2,
        "question":"What are the potential benefits of AI in healthcare?",
        "answer":"AI can assist in early disease detection, improve diagnosis accuracy, personalize treatment plans, and automate administrative tasks.",
        "justification":"Early Disease Detection: AI can analyze medical images and data to identify abnormalities and predict disease risk, enabling earlier intervention and improved outcomes.
Improved Diagnosis Accuracy: AI can assist doctors in making more accurate diagnoses by analyzing complex medical data and providing insights that may not be apparent to humans.
Personalized Treatment Plans: AI can analyze patient data to develop personalized treatment plans that are tailored to individual needs and preferences.
Automated Administrative Tasks: AI can automate administrative tasks such as scheduling appointments, managing patient records, and processing insurance claims, freeing up healthcare professionals to focus on patient care."
        },

        {
        "question_id":3,
        "question":"What are some of the ethical concerns surrounding AI development and deployment?",
        "answer":"AI development raises concerns about potential bias, lack of transparency, and job displacement. Responsible development is crucial.",
        "justification":"Potential Bias: AI algorithms can be biased based on the data they are trained on, leading to unfair or discriminatory outcomes.
Lack of Transparency: The decision-making processes of some AI systems can be opaque, making it difficult to understand how they arrive at their conclusions.
Job Displacement: As AI automates tasks, it may lead to job displacement in certain sectors, raising concerns about economic and social implications."
        }

    ]
}
"""

SINGLE_FILE_BASIC_JSON_STRUCTURE_MULTI_CHOICE = """
{
"quiz":

    [

        {
        "question_id":1,
        "question":str,
        "answers":[
        
                {
                "answer_id":1,
                "answer":str,
                "is_correct":bool
                },

                {
                "answer_id":2,
                "answer":str,
                "is_correct":bool
                },

                {
                "answer_id":3,
                "answer":str,
                "is_correct":bool
                }

                ]
        },

        {
        "question_id":2,
        "question":str,
        "answers":[
        
                {
                "answer_id":1,
                "answer":str,
                "is_correct":bool
                },

                {
                "answer_id":2,
                "answer":str,
                "is_correct":bool
                },

                {
                "answer_id":3,
                "answer":str,
                "is_correct":bool
                }

                ]
        },

        {
        "question_id":3,
        "question":str,
        "answers":[
        
                {
                "answer_id":1,
                "answer":str,
                "is_correct":bool
                },

                {
                "answer_id":2,
                "answer":str,
                "is_correct":bool
                },

                {
                "answer_id":3,
                "answer":str,
                "is_correct":bool
                }

                ]
        }

    ]
}
"""

SINGLE_FILE_BASIC_JSON_EXAMPLE_MULTI_CHOICE = """
{

"quiz":

    [

        {
        "question_id":1,
        "question":"What is 1 + 1?",
        "answers":[
        
                {
                "answer_id":1,
                "answer":"1",
                "is_correct":false
                },

                {
                "answer_id":2,
                "answer":"2",
                "is_correct":true
                },

                {
                "answer_id":3,
                "answer":"4",
                "is_correct":false
                }

                ]
        },

        {
        "question_id":2,
        "question":"Wath is 2 + 2?",
        "answers":[
        
                {
                "answer_id":1,
                "answer":"4",
                "is_correct":true
                },

                {
                "answer_id":2,
                "answer":"5",
                "is_correct":false
                },

                {
                "answer_id":3,
                "answer":"6",
                "is_correct":false
                }

                ]
        },

        {
        "question_id":3,
        "question":"What is 3 + 3?",
        "answers":[
        
                {
                "answer_id":1,
                "answer":"3",
                "is_correct":false
                },

                {
                "answer_id":2,
                "answer":"7",
                "is_correct":false
                },

                {
                "answer_id":3,
                "answer":"6",
                "is_correct":true
                }

                ]
        }

    ]
}
"""

SINGLE_FILE_BASIC_SYSTEM_INSTRUCTION = ["""You are a scholar assistant responsible to create quizzes from the given contents.""",
                                        """For each question, you will need to add the correct answer.""",
                                        #"""For each answer to a OPEN ENDED question, you will need to add a justification.""",
                                        """You must return a valid JSON Object with the output structure requested on the prompt.""",
                                        """Use the Output Example as template to create valid JSON Objects."""]



# Configurations

GLOBAL_APP_CONFIG = {"PROJECT_ID":"qgo-playground",
                     "LOCATION":"us-central1",
                     "LLM":{"MODEL":"gemini-1.0-pro",
                            "TEMPERATURE":0.5,
                            "MAX_TOKENS":2048}}

CONFIG = {"SINGLE_FILE_BASIC":{
                                "PROMPT":SINGLE_FILE_BASIC_PROMPT,
                                "SYSTEM_INSTRUCTION":SINGLE_FILE_BASIC_SYSTEM_INSTRUCTION,
                                "JSON_STRUCTURE_OPEN_Q":SINGLE_FILE_BASIC_JSON_STRUCTURE_OPEN_Q,
                                "JSON_EXAMPLE_OPEN_Q":SINGLE_FILE_BASIC_JSON_EXAMPLE_OPEN_Q,
                                "JSON_STRUCTURE_MULTI_CHOICE":SINGLE_FILE_BASIC_JSON_STRUCTURE_MULTI_CHOICE,
                                "JSON_EXAMPLE_MULTI_CHOICE":SINGLE_FILE_BASIC_JSON_EXAMPLE_MULTI_CHOICE,
},
"MAX_RETRY_COUNT":2
}