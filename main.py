import streamlit as st
import agent
import tools
import os
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="GHL Email Workbench")

# --- Initialize Session State ---
if "html_history" not in st.session_state:
    st.session_state.html_history = [] # Stack for Undo

if "current_html" not in st.session_state:
    st.session_state.current_html = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Helper Functions ---
def save_state():
    """Push current state to history before mutation."""
    if st.session_state.current_html:
        st.session_state.html_history.append(st.session_state.current_html)

def undo():
    """Pop from history."""
    if st.session_state.html_history:
        st.session_state.current_html = st.session_state.html_history.pop()
        st.rerun()

# --- UI Layout ---

# 1. Load Screen (if empty)
if not st.session_state.current_html:
    st.title("GHL Email Template Workbench")
    st.write("Paste your GHL Email HTML below to get started.")
    
    # Try to load sample if available for convenience
    sample_html = ""
    if os.path.exists("data/sample_ghl.html"):
        try:
            with open("data/sample_ghl.html", "r", encoding="utf-8") as f:
                sample_html = f.read()
        except Exception:
            pass

    initial_input = st.text_area("HTML Content", value=sample_html, height=300)
    
    if st.button("Start Editing"):
        st.session_state.current_html = initial_input
        st.rerun()

else:
    # 2. Editor Screen
    
    # --- Sidebar: Chat & Controls ---
    with st.sidebar:
        st.header("Jarvis Agent")
        
        # Undo Button
        if st.button("Undo Last Change", disabled=len(st.session_state.html_history) == 0, type="primary"):
            undo()
        
        st.divider()
        
        # Chat History Display
        chat_container = st.container(height=500)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    
        # User Input
        if prompt := st.chat_input("Instruct Jarvis (e.g., 'Make the button blue')"):
            # Add user message to UI history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.write(prompt)
            
            # --- Agent Execution ---
            save_state() # Save before agent messes with it
            
            try:
                with st.spinner("Jarvis is working..."):
                    # Run Agent using the new abstraction
                    # We pass the user prompt and the current HTML state
                    # The agent handles context injection, ADK execution, and state retrieval
                    response_text, new_html = agent.run_agent(
                        user_input=prompt,
                        current_html=st.session_state.current_html
                    )
                
                # Update State
                st.session_state.current_html = new_html
                
                # Add model response to UI history
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Agent Error: {e}")

    # --- Main Area: Preview & Code ---
    st.subheader("Template Preview")
    
    tab1, tab2 = st.tabs(["Preview", "Code"])
    
    with tab1:
        # Render HTML
        components.html(st.session_state.current_html, height=800, scrolling=True)
        
    with tab2:
        st.code(st.session_state.current_html, language='html')
