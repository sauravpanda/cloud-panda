CREATE_FLASK_APP = 'Create a detailed documentation for python3 flask application based on following info: {content} '

REVIEW_CODE = '''Given the Context, Instruction and CODE: Review the code as a expert python developer giving feedback for updates:\
CONTEXT:
{context}

INSTRUCTION / Tips:
{inst}

CODE:
{code}

Structure the response in specific categories and make it pretty. Make sure to check for vulnerabilites because of code logic.

Respond as a json with the feedback in a list; example: {{"review": {{"Testing missing": ["details"], "Security Vulnerability": ["details"]}} }}
'''


DOC_CODE = ''' Given the CODE, write inline comments and make it explainable.

CODE:
{code}

'''