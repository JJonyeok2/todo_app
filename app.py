import streamlit as st

st.title('To-do App')


# -----------------------------------------------------------------------------
# 1. 클래스 정의
# -----------------------------------------------------------------------------
class Todo:
    """
    할 일(Task)과 완료 여부(Done)를 관리하는 객체
    """

    def __init__(self, task: str, done: bool = False):
        self.__task = task
        self.__done = done

    def get_task(self):
        return self.__task

    def get_done(self):
        return self.__done

    def set_done(self, done: bool):
        self.__done = done

    # 디버깅 용도: 객체 리스트를 출력할 때 보기 좋게 표시 (__str__은 리스트 내부에서 호출 안 됨)
    def __repr__(self):
        return f'Task: {self.__task}, Done: {self.__done}'


# -----------------------------------------------------------------------------
# 2. 초기화 (Initialization) - 중요! 에러 방지 구역
# -----------------------------------------------------------------------------

# (1) 할 일 목록 리스트 초기화
if 'todos' not in st.session_state:
    st.session_state['todos'] = []

# (2) [KeyError 해결 핵심] 입력창 키('new_task') 미리 초기화
# 위젯이 그려지기 전에 콜백이 new_task를 찾으려 할 때 발생하는 에러를 막기 위해
# 미리 빈 문자열로 만들어 둡니다.
if 'new_task' not in st.session_state:
    st.session_state['new_task'] = ""

# (3) [AttributeError 해결 핵심] 데이터 정제 (안전장치)
# session_state에 Todo 객체가 아닌 옛날 데이터(딕셔너리 등)가 남아있으면 강제 초기화
# "AttributeError: ... object has no attribute 'get_done'" 방지용
if st.session_state['todos'] and len(st.session_state['todos']) > 0:
    first_item = st.session_state['todos'][0]
    if not isinstance(first_item, Todo):
        st.session_state['todos'] = []  # 리스트 비우기
        st.warning("데이터 형식이 변경되어 기존 목록을 초기화했습니다.")


# -----------------------------------------------------------------------------
# 3. 콜백 함수 (Event Handlers)
# -----------------------------------------------------------------------------

def add_todo():
    """입력창에서 엔터를 치면 실행되는 함수"""
    # st.session_state['new_task']에 사용자가 입력한 값이 들어있음
    current_input = st.session_state['new_task']

    # 빈 값 입력 방지
    if current_input.strip() != "":
        print(f'함수가 호출 될 때 값: {current_input}')
        todo = Todo(current_input)
        st.session_state['todos'].append(todo)

        # 입력 후 입력창 비우기 (session_state 값을 변경하면 위젯도 비워짐)
        st.session_state['new_task'] = ""


def toggle_done(idx):
    """체크박스를 클릭했을 때 실행되는 함수"""
    # 리스트에서 해당 인덱스의 객체를 가져와 상태 반전
    todo = st.session_state['todos'][idx]
    todo.set_done(not todo.get_done())


# -----------------------------------------------------------------------------
# 4. 화면 구성 (UI Layout)
# -----------------------------------------------------------------------------

# 텍스트 입력 위젯
# key='new_task': 이 위젯의 값은 st.session_state['new_task']와 연동됨
# on_change=add_todo: 엔터를 누르면 add_todo 함수 실행
st.text_input('새로운 할일 추가', key='new_task', on_change=add_todo)

# 할 일 목록 출력
if st.session_state['todos']:
    for i, todo in enumerate(st.session_state['todos']):
        col1, col2 = st.columns([0.1, 0.9])

        # 체크박스
        # value: 현재 완료 상태(True/False)를 반영
        # args=(i,): toggle_done 함수에 몇 번째 항목인지(i)를 전달
        col1.checkbox(
            label=f'{i}',  # 라벨은 고유해야 하지만 화면엔 잘 안 보임(레이아웃상)
            value=todo.get_done(),
            key=f'done_{i}',
            on_change=toggle_done,
            args=(i,),
            label_visibility="collapsed"  # 체크박스 옆 숫자 숨기기 (선택사항)
        )

        # 텍스트 표시 (완료 시 취소선 적용)
        display_text = f'~~{todo.get_task()}~~' if todo.get_done() else todo.get_task()
        col2.markdown(display_text)

else:
    st.info('할 일을 추가해 보세요.')
