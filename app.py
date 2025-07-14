import streamlit as st
import uuid
from datetime import datetime
from typing import Dict, List, Any

# Page configuration
st.set_page_config(
    page_title="할 일 목록",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Korean design theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

:root {
    --primary-color: #002152;
    --accent-color: #f7941d;
    --text-color: #ffffff;
    --bg-color: #002152;
    --card-bg: rgba(255, 255, 255, 0.1);
    --border-color: rgba(255, 255, 255, 0.2);
}

.stApp {
    background: linear-gradient(135deg, var(--primary-color) 0%, #003366 100%);
    font-family: 'Noto Sans KR', sans-serif;
}

.main-header {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-color);
}

.main-header h1 {
    color: var(--text-color);
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.main-header p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
    margin-bottom: 0;
}

.task-card {
    background: var(--card-bg);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid var(--border-color);
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.task-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.task-completed {
    background: rgba(76, 175, 80, 0.2);
    border-color: #4caf50;
}

.custom-button {
    background: var(--accent-color);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 25px;
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1rem;
    box-shadow: 0 4px 15px rgba(247, 148, 29, 0.3);
}

.custom-button:hover {
    background: #e6850a;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(247, 148, 29, 0.4);
}

.filter-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 2rem 0;
}

.filter-button {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-family: 'Noto Sans KR', sans-serif;
    cursor: pointer;
    transition: all 0.3s ease;
}

.filter-button:hover, .filter-button.active {
    background: var(--accent-color);
    border-color: var(--accent-color);
    transform: translateY(-1px);
}

.stats-container {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 2rem 0;
}

.stat-card {
    background: var(--card-bg);
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
    min-width: 150px;
    border: 1px solid var(--border-color);
    backdrop-filter: blur(10px);
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent-color);
    margin-bottom: 0.5rem;
}

.stat-label {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
    font-weight: 400;
}

/* Override Streamlit default styles */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid var(--border-color);
    color: var(--text-color);
    font-family: 'Noto Sans KR', sans-serif;
    border-radius: 10px;
    padding: 0.75rem;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

.stCheckbox > label {
    color: var(--text-color);
    font-family: 'Noto Sans KR', sans-serif;
}

.stButton > button {
    background: var(--accent-color);
    color: white;
    border: none;
    border-radius: 25px;
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 500;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(247, 148, 29, 0.3);
}

.stButton > button:hover {
    background: #e6850a;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(247, 148, 29, 0.4);
}

.stMarkdown {
    color: var(--text-color);
    font-family: 'Noto Sans KR', sans-serif;
}

.stInfo, .stSuccess, .stWarning, .stError {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

.stMetric {
    background: var(--card-bg);
    border-radius: 10px;
    padding: 1rem;
    border: 1px solid var(--border-color);
    backdrop-filter: blur(10px);
}

.stMetric > div {
    color: var(--text-color);
    font-family: 'Noto Sans KR', sans-serif;
}

.stMetric [data-testid="metric-value"] {
    color: var(--accent-color);
    font-weight: 700;
}

.stDivider {
    border-color: var(--border-color);
    margin: 2rem 0;
}

.footer {
    text-align: center;
    color: rgba(255, 255, 255, 0.6);
    padding: 2rem;
    margin-top: 3rem;
    border-top: 1px solid var(--border-color);
    font-family: 'Noto Sans KR', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for todos
if 'todos' not in st.session_state:
    st.session_state.todos = []

if 'filter_state' not in st.session_state:
    st.session_state.filter_state = 'all'

def add_todo(task_text: str) -> None:
    """Add a new todo item to the list."""
    if task_text.strip():
        new_todo = {
            'id': str(uuid.uuid4()),
            'text': task_text.strip(),
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.todos.append(new_todo)
        st.rerun()

def toggle_todo(todo_id: str) -> None:
    """Toggle the completion status of a todo item."""
    for todo in st.session_state.todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    st.rerun()

def delete_todo(todo_id: str) -> None:
    """Delete a todo item from the list."""
    st.session_state.todos = [todo for todo in st.session_state.todos if todo['id'] != todo_id]
    st.rerun()

def filter_todos(filter_type: str) -> List[Dict[str, Any]]:
    """Filter todos based on completion status."""
    if filter_type == 'completed':
        return [todo for todo in st.session_state.todos if todo['completed']]
    elif filter_type == 'pending':
        return [todo for todo in st.session_state.todos if not todo['completed']]
    else:  # 'all'
        return st.session_state.todos

def main():
    # Modern header with custom styling
    st.markdown("""
    <div class="main-header">
        <h1>📝 할 일 목록</h1>
        <p>효율적인 작업 관리를 위한 간단한 할 일 목록 애플리케이션</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Task input section
    st.markdown("### 새로운 할 일 추가")
    
    # Create columns for input and button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_task = st.text_input(
            "새로운 할 일을 입력하세요:",
            placeholder="무엇을 해야 하나요?",
            key="new_task_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("할 일 추가", type="primary"):
            if new_task.strip():
                add_todo(new_task)
                # Clear the input by resetting the key
                st.session_state.new_task_input = ""
            else:
                st.error("유효한 할 일을 입력해주세요.")
    
    # Filter section
    st.markdown("### 할 일 필터")
    
    # Filter buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("모든 할 일", use_container_width=True):
            st.session_state.filter_state = 'all'
            st.rerun()
    
    with col2:
        if st.button("완료된 할 일", use_container_width=True):
            st.session_state.filter_state = 'completed'
            st.rerun()
    
    with col3:
        if st.button("진행 중인 할 일", use_container_width=True):
            st.session_state.filter_state = 'pending'
            st.rerun()
    
    # Display current filter
    filter_labels = {
        'all': "모든 할 일",
        'completed': "완료된 할 일",
        'pending': "진행 중인 할 일"
    }
    st.info(f"현재 보기: {filter_labels[st.session_state.filter_state]}")
    
    # Display todos
    filtered_todos = filter_todos(st.session_state.filter_state)
    
    if not filtered_todos:
        if st.session_state.filter_state == 'all':
            st.info("할 일이 없습니다. 새로운 할 일을 추가해보세요!")
        elif st.session_state.filter_state == 'completed':
            st.info("완료된 할 일이 없습니다.")
        else:  # pending
            st.info("진행 중인 할 일이 없습니다.")
    else:
        st.markdown(f"### 할 일 목록 ({len(filtered_todos)}개)")
        
        # Display each todo item with custom styling
        for todo in filtered_todos:
            # Create a task card with custom styling
            card_class = "task-card task-completed" if todo['completed'] else "task-card"
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="flex: 1;">
                        {'<s>' if todo['completed'] else '<strong>'}
                        {todo['text']}
                        {'</s>' if todo['completed'] else '</strong>'}
                    </div>
                    <div style="font-size: 0.8rem; color: rgba(255, 255, 255, 0.7);">
                        {'✅ 완료됨' if todo['completed'] else '⏳ 진행 중'} | 생성일: {todo['created_at']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Control buttons for each task
            col1, col2, col3 = st.columns([0.5, 3, 0.5])
            
            with col1:
                # Checkbox for completion status
                if st.checkbox(
                    "완료",
                    value=todo['completed'],
                    key=f"checkbox_{todo['id']}",
                    help="완료/미완료 상태 변경",
                    label_visibility="collapsed"
                ):
                    if not todo['completed']:
                        toggle_todo(todo['id'])
                else:
                    if todo['completed']:
                        toggle_todo(todo['id'])
            
            with col3:
                # Delete button
                if st.button(
                    "🗑️",
                    key=f"delete_{todo['id']}",
                    help="이 할 일 삭제",
                    use_container_width=True
                ):
                    delete_todo(todo['id'])
            
            # Add spacing between tasks
            st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistics section
    if st.session_state.todos:
        st.markdown("### 통계")
        
        total_tasks = len(st.session_state.todos)
        completed_tasks = len([todo for todo in st.session_state.todos if todo['completed']])
        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("전체 할 일", total_tasks)
        
        with col2:
            st.metric("완료된 할 일", completed_tasks)
        
        with col3:
            st.metric("진행 중인 할 일", pending_tasks)
        
        with col4:
            st.metric("완료율", f"{completion_rate:.1f}%")
    
    # Modern footer
    st.markdown("""
    <div class="footer">
        <p>Streamlit으로 제작된 할 일 목록 애플리케이션</p>
        <p>효율적인 작업 관리를 위한 간단하고 직관적인 도구</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
