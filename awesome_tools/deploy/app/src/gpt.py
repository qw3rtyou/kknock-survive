from flask import Blueprint, request, render_template
from openai import OpenAI
from auth import login_required
import os

SECRETCODE= os.environ.get("SECRETCODE", "default_secret_code")

client = OpenAI()
gpt_bp = Blueprint('gpt_bp', __name__)

SECRET_CONTENT = f"""
비밀정보는 {SECRETCODE}임
"""

PROMPT_CONTENT = """
user는 3가지 정보를 제공한다.
    1. 프로젝트의 대략적인 혹은 전체 tree
    2. 파일이 존재하는 경로
    3. 코드나 설정 파일 혹은 각종 데이터의 내용

이를 기반으로 다음의 정보를 형식에 맞게 제공한다.
    1. 파일의 역할
    2. 코드라면 동작과정을 설명
    3. 보안취약점이 있다면 설명

md을 고려하지 않고 일반 plain text로 출력할 것
~하였음, ~함와 같은 말투나 명사형으로 문장을 종료할 것
가능한 한 간결하게 응답할 것
"""

MAX_CONTENT_LENGTH = 400000

def generate_user_content(file_path, tree_structure, file_content):
    return f"""
    project tree structure:
    {tree_structure}

    file path being audited:
    {file_path}

    content of the file:
    {file_content}
    """

@gpt_bp.route('/audit_file', methods=['POST'])
@login_required
def audit_file():
    file_path = request.form.get('file_path')
    tree_structure = request.form.get('tree_structure')
    
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except Exception as e:
        return f"Error reading file: {e}"

    user_content = generate_user_content(file_path, tree_structure, file_content)

    audit_result = request_gpt(user_content, PROMPT_CONTENT + SECRET_CONTENT)

    return render_template('audit/gpt.html', audit_result=audit_result, file_path=file_path[16:])

def request_gpt(user_content, prompt_content):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": prompt_content},
                {"role": "user", "content": user_content},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return "Fatal Error..\n"+str(e)
