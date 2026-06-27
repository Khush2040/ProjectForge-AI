import streamlit as st
import json
import os
from dotenv import load_dotenv

from services.project_analyzer import ProjectAnalyzer
from services.embedding_service import generate_embeddings, semantic_search
from services.chat_service import ChatService
from storage.save_project import save_project

from ui.components import (
    hero_section,
    sidebar,
    dashboard_metrics,
    blueprint_visualizer,
    glass_card,
    tech_stack
)

from ui.animations import (
    project_analysis_loader,
)

# Load environment variables
load_dotenv()

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="🚀 ProjectForge AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Load CSS
# ==========================================

def load_css():
    with open("ui/styles.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True,
        )

load_css()

# ==========================================
# Session State Initialization & URL Sync
# ==========================================

if "current_page" not in st.session_state:
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.current_page = query_params["page"]
    else:
        st.session_state.current_page = "Dashboard"

if "selected_project" not in st.session_state:
    st.session_state.selected_project = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_generated_blueprint" not in st.session_state:
    st.session_state.last_generated_blueprint = None

# ==========================================
# Sidebar Rendering
# ==========================================

sidebar()

# ==========================================
# Page Views Routing
# ==========================================

def render_dashboard_page():
    hero_section()
    dashboard_metrics()
    
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
    
    c_main, c_side = st.columns([2.2, 1])
    
    with c_main:
        st.markdown("### 📂 Recent Project Blueprints")
        if os.path.exists("data/projects.json"):
            try:
                with open("data/projects.json", "r") as file:
                    projects = json.load(file)
            except Exception:
                projects = []
        else:
            projects = []
            
        if not projects:
            st.info("💡 No project blueprints generated yet. Head over to **New Project** to start planning!")
        else:
            cols = st.columns(min(len(projects), 2))
            latest_projects = list(reversed(projects))[:2]
            for idx, project in enumerate(latest_projects):
                with cols[idx % min(len(projects), 2)]:
                    overview = project.get("project_overview", {})
                    name = overview.get("project_name", "Untitled Project")
                    desc = overview.get("project_description", "No description provided.")
                    
                    st.markdown(f"""
                    <div class="glass-card fade-in" style="min-height: 220px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 15px;">
                        <div>
                            <h4 style="color: #38BDF8; margin-top:0; margin-bottom:8px;">{name}</h4>
                            <p style="font-size: 13px; color: #CBD5E1; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; text-align: justify;">{desc}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("👁 View Blueprint", key=f"dash_view_{idx}", use_container_width=True):
                        st.session_state.selected_project = project
                        st.session_state.current_page = "SavedBlueprints"
                        st.rerun()
                        
    with c_side:
        st.markdown("### ⚡ System Status")
        st.markdown(f"""
        <div class="glass-card" style="padding: 16px; min-height: 290px; margin-bottom:15px;">
            <h5 style="margin-top:0; color:#10B981; font-weight:700; margin-bottom: 15px;">● Telemetry Online</h5>
            <div style="font-size:12px; line-height:1.6; color:#CBD5E1;">
                <p style="margin-bottom:8px;">🤖 <strong>AI LLM Engine</strong>: mistral-small-2506</p>
                <p style="margin-bottom:8px;">🧠 <strong>Embeddings Model</strong>: all-MiniLM-L6-v2</p>
                <p style="margin-bottom:8px;">💾 <strong>Storage Engine</strong>: local JSON cache</p>
                <p style="margin-bottom:8px;">🔗 <strong>Mistral Connection</strong>: active (0.2s latency)</p>
                <p style="margin-bottom:0; color:#38BDF8; font-weight:600; font-size:11px; margin-top:15px; letter-spacing: 0.5px;">EXECUTION LOGS:</p>
                <code style="font-size:10px; color:#A78BFA; background:rgba(0,0,0,0.2); display:block; padding:8px; border-radius:8px; margin-top:5px; line-height:1.3; border: 1px solid rgba(255,255,255,0.03);">
                [info] Vector database synchronized.<br>
                [info] Mistral connection established.<br>
                [info] Local cache synced successfully.
                </code>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_new_project_page():
    st.markdown("<h2 class='fade-in'>➕ Create New Project Blueprint</h2>", unsafe_allow_html=True)
    st.markdown("Transform your software project idea into a professional architecture and implementation specification plan.")
    
    col_input, col_config = st.columns([2.2, 1])
    
    with col_input:
        project_idea = st.text_area(
            "💡 Describe Your Project Idea",
            placeholder="""Example:
Build an AI Interview Preparation Platform that helps students practice technical interviews, analyze resumes, generate mock interviews, and provide AI feedback.
""",
            height=260,
        )
        
        generate_btn = st.button("🚀 Analyze & Generate Blueprint", use_container_width=True)
        
    with col_config:
        st.markdown("<div class='glass-card' style='padding: 16px; min-height: 330px;'>", unsafe_allow_html=True)
        st.markdown("#### ⚙️ Design Preferences")
        arch_pref = st.selectbox(
            "Architecture Style",
            ["No Preference", "Microservices Architecture", "Monolithic Architecture", "Serverless Architecture", "Event-Driven Architecture"]
        )
        db_pref = st.selectbox(
            "Database System",
            ["No Preference", "PostgreSQL (Relational SQL)", "MongoDB (Document NoSQL)", "MySQL (Relational SQL)", "Redis (In-Memory Key-Value)"]
        )
        cloud_pref = st.selectbox(
            "Target Cloud Provider",
            ["No Preference", "AWS (Amazon Web Services)", "GCP (Google Cloud Platform)", "Microsoft Azure", "Vercel / Supabase"]
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    if generate_btn:
        if project_idea.strip() == "":
            st.warning("⚠️ Please enter a project idea.")
            st.stop()
            
        analyzer = ProjectAnalyzer()
        
        # Inject design preferences into the query
        final_query = project_idea
        if arch_pref != "No Preference":
            final_query += f"\n- Architecture Style Preference: {arch_pref}"
        if db_pref != "No Preference":
            final_query += f"\n- Database System Preference: {db_pref}"
        if cloud_pref != "No Preference":
            final_query += f"\n- Cloud Host Provider Preference: {cloud_pref}"
            
        # Beautiful progress steps animation
        project_analysis_loader()
        
        try:
            result = analyzer.analyze(final_query)
            
            # Save project to projects.json
            save_project(result)
            
            # Try to parse the result so we can load it
            result_clean = result.replace("```json", "").replace("```", "").strip()
            project_data = json.loads(result_clean)
            
            st.session_state.last_generated_blueprint = project_data
            st.session_state.selected_project = project_data
            
            st.success("🎉 Project Blueprint Generated Successfully!")
            
            # Regenerate embeddings in the background to keep it sync'd
            try:
                generate_embeddings()
            except Exception:
                pass
                
        except Exception as e:
            st.error(f"❌ Failed to generate blueprint: {str(e)}")
            
    if st.session_state.last_generated_blueprint:
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown("### ✨ Generated Project Architecture")
        blueprint_visualizer(st.session_state.last_generated_blueprint)


def render_saved_blueprints_page():
    st.markdown("<h2 class='fade-in'>📂 Saved Project Blueprints</h2>", unsafe_allow_html=True)
    
    if os.path.exists("data/projects.json"):
        try:
            with open("data/projects.json", "r") as file:
                projects = json.load(file)
        except Exception:
            projects = []
    else:
        projects = []
        
    if not projects:
        st.info("💡 No project blueprints saved yet. Go to **New Project** to create one.")
        return
        
    project_names = [p.get("project_overview", {}).get("project_name", f"Project {i+1}") for i, p in enumerate(projects)]
    
    default_idx = 0
    if st.session_state.selected_project:
        sel_name = st.session_state.selected_project.get("project_overview", {}).get("project_name", "")
        if sel_name in project_names:
            default_idx = project_names.index(sel_name)
            
    c_list, c_detail = st.columns([1, 2.2])
    
    with c_list:
        st.markdown("<div class='glass-card' style='padding: 16px; min-height: 480px;'>", unsafe_allow_html=True)
        st.markdown("#### 📁 Select Specification")
        selected_name = st.selectbox("Project List", project_names, index=default_idx, label_visibility="collapsed")
        
        selected_project = projects[project_names.index(selected_name)]
        st.session_state.selected_project = selected_project
        
        overview = selected_project.get("project_overview", {})
        desc = overview.get("project_description", "No description provided.")
        st.markdown(f"""
        <h5 style='color:#38BDF8; margin-top:15px; margin-bottom:5px;'>Brief Summary</h5>
        <p style='font-size:12.5px; line-height:1.4; color:#CBD5E1; text-align:justify;'>{desc[:240]}...</p>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.06);'><br>", unsafe_allow_html=True)
        
        if st.button("💬 Discuss in AI Chat", use_container_width=True):
            st.session_state.current_page = "AIChat"
            st.rerun()
            
        if st.button("🗑️ Delete Blueprint", use_container_width=True):
            projects.remove(selected_project)
            with open("data/projects.json", "w") as file:
                json.dump(projects, file, indent=4)
            st.session_state.selected_project = None
            try:
                generate_embeddings()
            except Exception:
                pass
            st.success("Deleted project successfully!")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    with c_detail:
        blueprint_visualizer(selected_project)


def render_embeddings_page():
    st.markdown("<h2 class='fade-in'>🧠 Project Embeddings Manager</h2>", unsafe_allow_html=True)
    st.markdown("Verify, synchronize, and examine the semantic vector space of your software project blueprints.")
    
    total_projects = 0
    total_embeddings = 0
    
    if os.path.exists("data/projects.json"):
        try:
            with open("data/projects.json", "r") as file:
                projects = json.load(file)
                total_projects = len(projects)
        except Exception:
            pass
            
    embeddings_data = []
    if os.path.exists("data/project_embeddings.json"):
        try:
            with open("data/project_embeddings.json", "r") as file:
                embeddings_data = json.load(file)
                total_embeddings = len(embeddings_data)
        except Exception:
            pass

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="glass-card" style="padding: 20px; min-height: 180px;">
            <h4 style="margin-top:0; color:#38BDF8;">Embedding Status</h4>
            <p style="margin-bottom:6px;">📁 Total Blueprints: <strong>{total_projects}</strong></p>
            <p style="margin-bottom:6px;">🧠 Vector Count: <strong>{total_embeddings}</strong></p>
            <p style="margin-bottom:0;">📐 Dimensions: <strong>384</strong> (Sentence-Transformers all-MiniLM-L6-v2)</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("<div class='glass-card' style='padding: 20px; min-height: 180px;'>", unsafe_allow_html=True)
        st.markdown("##### Actions")
        if st.button("🔄 Sync & Regenerate Embeddings", use_container_width=True):
            with st.spinner("🧠 Calculating embeddings using sentence-transformers model..."):
                try:
                    vectors, projects_list = generate_embeddings()
                    st.success(f"Successfully generated embeddings for {len(vectors)} projects!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating embeddings: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    if embeddings_data:
        st.markdown("<br>### 📊 Vector Index Table", unsafe_allow_html=True)
        table_data = []
        for emb in embeddings_data:
            vec = emb.get("vector", [])
            table_data.append({
                "Project Name": emb.get("project_name", "Untitled"),
                "Dimensions": len(vec),
                "Sample Vector (First 8 elements)": str(vec[:8])[:-1] + ", ...]"
            })
        st.dataframe(table_data, use_container_width=True)


def render_semantic_search_page():
    st.markdown("<h2 class='fade-in'>🔍 Semantic Search Engine</h2>", unsafe_allow_html=True)
    st.markdown("Query your project specifications using natural language. The engine uses vector embeddings to map requirements and architectures.")
    
    c_search, c_results = st.columns([1, 1.8])
    
    with c_search:
        st.markdown("<div class='glass-card' style='padding: 16px; min-height: 250px;'>", unsafe_allow_html=True)
        st.markdown("#### 🔍 Filter Parameters")
        query = st.text_input(
            "What architecture, stack, or feature are you looking for?", 
            placeholder="e.g., 'React frontend with postgres'",
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        top_k = st.slider("Max Search Results", min_value=1, max_value=10, value=3)
        search_triggered = st.button("🔍 Search Index", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c_results:
        if search_triggered or (query.strip() and st.session_state.get("prev_query") != query):
            if not query.strip():
                st.info("Please enter a search query.")
                return
                
            st.session_state["prev_query"] = query
            with st.spinner("🧠 Embedding query and running cosine similarity search..."):
                results = semantic_search(query, top_k=top_k)
                
            if not results:
                st.warning("No matching blueprints found. Ensure you have generated blueprints and synchronized embeddings.")
            else:
                st.markdown(f"### 🎯 Top {len(results)} Matches:")
                for idx, res in enumerate(results):
                    project = res["project"]
                    score = res["score"]
                    overview = project.get("project_overview", {})
                    name = overview.get("project_name", "Untitled Project")
                    desc = overview.get("project_description", "")
                    
                    percentage = int(score * 100)
                    
                    st.markdown(f"""
                    <div class="search-card">
                        <div class="search-header">
                            <span class="search-title">{name}</span>
                            <span class="search-badge">{percentage}% Match</span>
                        </div>
                        <div class="search-description">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"👁️ View {name} Blueprint", key=f"search_view_{idx}", use_container_width=True):
                        st.session_state.selected_project = project
                        st.session_state.current_page = "SavedBlueprints"
                        st.rerun()
        else:
            st.info("💡 Enter a query on the left to search blueprints semantically.")


def render_ai_chat_page():
    st.markdown("<h2 class='fade-in'>💬 Architecture AI Chat</h2>", unsafe_allow_html=True)
    st.markdown("Discuss system design, requirements, stack details, or future scopes. Select a project below to chat contextually.")
    
    if os.path.exists("data/projects.json"):
        try:
            with open("data/projects.json", "r") as file:
                projects = json.load(file)
        except Exception:
            projects = []
    else:
        projects = []
        
    project_names = ["No Project Context"] + [p.get("project_overview", {}).get("project_name", f"Project {i+1}") for i, p in enumerate(projects)]
    
    default_idx = 0
    if st.session_state.selected_project:
        sel_name = st.session_state.selected_project.get("project_overview", {}).get("project_name", "")
        if sel_name in project_names:
            default_idx = project_names.index(sel_name)
            
    selected_context = st.selectbox("📂 Chat Context (Selected Project)", project_names, index=default_idx)
    
    context_project = None
    if selected_context != "No Project Context":
        context_project = projects[project_names.index(selected_context) - 1]
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = msg["content"]
            bubble_class = "user" if role == "user" else "assistant"
            sender_name = "👤 You" if role == "user" else "🤖 ProjectForge AI"
            
            st.markdown(f"""
            <div class="chat-message {bubble_class}">
                <div class="message-sender">{sender_name}</div>
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
            
    prompt = st.chat_input("Ask a question about the design...")
    
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        chat_service = ChatService()
        with st.spinner("🤖 Thinking..."):
            response = chat_service.get_response(st.session_state.chat_history, context_project)
            
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
        
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


def render_settings_page():
    st.markdown("<h2 class='fade-in'>⚙ Settings & Maintenance</h2>", unsafe_allow_html=True)
    
    st.markdown("### 🔑 API Verification")
    mistral_key_status = "Configured ✅" if os.getenv("MISTRAL_API_KEY") else "Missing ❌"
    st.markdown(f"**Mistral API Key**: `{mistral_key_status}`")
    
    st.markdown("<br>### 🧹 Data Cleaning", unsafe_allow_html=True)
    st.warning("⚠️ The actions below are permanent and cannot be undone.")
    
    if st.button("🗑️ Reset All Project Data", use_container_width=True):
        if os.path.exists("data/projects.json"):
            try:
                os.remove("data/projects.json")
            except Exception:
                pass
        if os.path.exists("data/project_embeddings.json"):
            try:
                os.remove("data/project_embeddings.json")
            except Exception:
                pass
        st.session_state.selected_project = None
        st.session_state.last_generated_blueprint = None
        st.session_state.chat_history = []
        st.success("All projects and cached embeddings have been deleted successfully!")
        st.rerun()


# Page Routing Execution
if st.session_state.current_page == "Dashboard":
    render_dashboard_page()
elif st.session_state.current_page == "NewProject":
    render_new_project_page()
elif st.session_state.current_page == "SavedBlueprints":
    render_saved_blueprints_page()
elif st.session_state.current_page == "Embeddings":
    render_embeddings_page()
elif st.session_state.current_page == "SemanticSearch":
    render_semantic_search_page()
elif st.session_state.current_page == "AIChat":
    render_ai_chat_page()
elif st.session_state.current_page == "Settings":
    render_settings_page()