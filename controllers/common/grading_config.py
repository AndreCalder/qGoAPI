# single_file_basic()

SINGLE_FILE_BASIC_PROMPT = """
<REQUEST>
DETERMINE WETHER EACH OF THE ANSWERS GIVEN IN THE ARRAY PROVIDED ARE CORRECT:
</REQUEST>

THE EXCPECTED CONTENT SHOULD BE AN ARRAY WITH THE FOLLOWING STRUCTURE:
<CONTENT_STRUCTURE>
{content_structure}
</CONTENT STRUCTURE>
IMPORTANT: ONLY USE THE PROVIDED CONTENT.
<CONTENT>
{content}
</CONTENT>


THE EXPECTED OUTPUT SHOULD BE A JSON OBJECT WITH THE FOLLOWING STRUCTURE:
<OUTPUT STRUCTURE>
{grade_json_structure}
</OUTPUT STRUCTURE>

HERE IS AN EXAMPLE OF HOW THE JSON OBJECT SHOULD LOOK LIKE:
<OUTPUT EXAMPLE>
{grade_json_example}
</OUTPUT EXAMPLE>

IMPORTANT: ALWAYS KEEP MISTAKES ("mistake") SHORT AND CONCISE.
"""

CONTENT_STRUCTURE = """
[
    {
        answer: str
        answers: null
        complete_answer: str,
        justification: str,
        q_type: "open_q",
        question: str,
        _id: {
            $oid: str
            }
    },
    ...
]
"""
GRADE_JSON_STRUCTURE = """
{
    "gradedAnswers":
        [
            {
                answer: str
                answers: null
                complete_answer: str,
                justification: str,
                q_type: "open_q",
                question: str,
                is_correct: boolean,
                mistake: str,
                _id: {
                    $oid: str
                    }
            },
        ...
        ]
}
"""

GRADE_JSON_EXAMPLE = """
{
    "gradedAnswers":
        [
            {
                answer: "AI aims to create intelligent machines, while ML enables machines to learn from data without explicit programming.",
                answers: null
                complete_answer: ""AI aims to create intelligent machines, while ML enables machines to learn from data without explicit programming.",
                justification: "AI: The broader field of computer science concerned with creating intelligent machines that can perform tasks typically requiring human intelligence.
ML: A subset of AI that focuses on enabling machines to learn from data without explicit programming.",
                q_type: "open_q",
                question: "What is the difference between Artificial Intelligence (AI) and Machine Learning (ML)?",
                is_correct: true,
                mistake: "",
                _id: {
                    $oid: str
                    }
            },
                        {
                answer: "AI will deliver pizza for us and steal our money.",
                answers: null
                complete_answer: "AI development raises concerns about potential bias, lack of transparency, and job displacement. Responsible development is crucial.",
                justification: "Potential Bias: AI algorithms can be biased based on the data they are trained on, leading to unfair or discriminatory outcomes.
Lack of Transparency: The decision-making processes of some AI systems can be opaque, making it difficult to understand how they arrive at their conclusions.
Job Displacement: As AI automates tasks, it may lead to job displacement in certain sectors, raising concerns about economic and social implications.",
                q_type: "open_q",
                question: "What are some of the ethical concerns surrounding AI development and deployment?"",
                is_correct: false,
                mistake: "",
                _id: {
                    $oid: str
                    }
            },
        ...
        ]
}
"""

SYSTEM_INSTRUCTION = ["""You are a scholar assistant responsible for checking questions.""",
                                        """For each question, you will need to determinte wether the answer is correct or not by comparing the complete_answer to the answer, taking into consideration the justification for more context""",
                                        """If a question is not correct, use the complete answer to provide a short explanation as to why in the "mistake" field, using information about the question.""",
                                        """You must return a valid JSON Object with the <OUTPUT STRUCTURE> requested on the prompt.""",
                                        """Use the <OUTPUT EXAMPLE> as template to create valid JSON Objects."""]


GRADE_CONFIG = {"ANSWER_CHECK":{
                                "PROMPT":SINGLE_FILE_BASIC_PROMPT,
                                "SYSTEM_INSTRUCTION":SYSTEM_INSTRUCTION,
                                "JSON_STRUCTURE":GRADE_JSON_STRUCTURE,
                                "JSON_EXAMPLE": GRADE_JSON_EXAMPLE,
                                "CONTENT_STRUCTURE": CONTENT_STRUCTURE
},
"MAX_RETRY_COUNT":3
}