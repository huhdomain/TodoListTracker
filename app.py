import streamlit as st
import uuid
from datetime import datetime
from typing import Dict, List, Any

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
    # App title
    st.title("📝 Todo List")
    st.write("Manage your tasks efficiently with this simple todo list application.")
    
    # Task input section
    st.subheader("Add New Task")
    
    # Create columns for input and button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_task = st.text_input(
            "Enter a new task:",
            placeholder="What needs to be done?",
            key="new_task_input"
        )
    
    with col2:
        if st.button("Add Task", type="primary"):
            if new_task.strip():
                add_todo(new_task)
                # Clear the input by resetting the key
                st.session_state.new_task_input = ""
            else:
                st.error("Please enter a valid task.")
    
    # Filter section
    st.subheader("Filter Tasks")
    
    # Filter buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("All Tasks", use_container_width=True):
            st.session_state.filter_state = 'all'
            st.rerun()
    
    with col2:
        if st.button("Completed", use_container_width=True):
            st.session_state.filter_state = 'completed'
            st.rerun()
    
    with col3:
        if st.button("Pending", use_container_width=True):
            st.session_state.filter_state = 'pending'
            st.rerun()
    
    # Display current filter
    filter_labels = {
        'all': "All Tasks",
        'completed': "Completed Tasks",
        'pending': "Pending Tasks"
    }
    st.info(f"Currently showing: {filter_labels[st.session_state.filter_state]}")
    
    # Display todos
    filtered_todos = filter_todos(st.session_state.filter_state)
    
    if not filtered_todos:
        if st.session_state.filter_state == 'all':
            st.info("No tasks found. Add a new task to get started!")
        elif st.session_state.filter_state == 'completed':
            st.info("No completed tasks found.")
        else:  # pending
            st.info("No pending tasks found.")
    else:
        st.subheader(f"Tasks ({len(filtered_todos)})")
        
        # Display each todo item
        for todo in filtered_todos:
            # Create a container for each todo item
            with st.container():
                col1, col2, col3 = st.columns([0.5, 3, 0.5])
                
                with col1:
                    # Checkbox for completion status
                    if st.checkbox(
                        "",
                        value=todo['completed'],
                        key=f"checkbox_{todo['id']}",
                        help="Mark as complete/incomplete"
                    ):
                        if not todo['completed']:
                            toggle_todo(todo['id'])
                    else:
                        if todo['completed']:
                            toggle_todo(todo['id'])
                
                with col2:
                    # Display task text with different styling for completed tasks
                    if todo['completed']:
                        st.markdown(f"~~{todo['text']}~~")
                        st.caption(f"✅ Completed | Created: {todo['created_at']}")
                    else:
                        st.markdown(f"**{todo['text']}**")
                        st.caption(f"⏳ Pending | Created: {todo['created_at']}")
                
                with col3:
                    # Delete button
                    if st.button(
                        "🗑️",
                        key=f"delete_{todo['id']}",
                        help="Delete this task",
                        use_container_width=True
                    ):
                        delete_todo(todo['id'])
                
                # Add a separator line
                st.divider()
    
    # Statistics section
    if st.session_state.todos:
        st.subheader("Statistics")
        
        total_tasks = len(st.session_state.todos)
        completed_tasks = len([todo for todo in st.session_state.todos if todo['completed']])
        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tasks", total_tasks)
        
        with col2:
            st.metric("Completed", completed_tasks)
        
        with col3:
            st.metric("Pending", pending_tasks)
        
        with col4:
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 10px;'>"
        "Built with Streamlit | Simple Todo List Application"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
