import streamlit as st


# ===========================
# HERO SECTION
# ===========================

def hero_section():
    st.markdown(
        """
        <div class="fade-in">
            <div class="hero-title">🚀 ProjectForge AI</div>
            <div class="hero-subtitle">
                AI Software Planning & Architecture Assistant<br><br>
                Transform your software idea into a professional project blueprint.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ===========================
# SECTION TITLE
# ===========================

def section_title(title):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        """,
        unsafe_allow_html=True
    )


# ===========================
# GLASS CARD
# ===========================

def glass_card(title, content):
    st.markdown(
        f"""
        <div class="glass-card fade-in">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ===========================
# METRIC CARD
# ===========================

def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ===========================
# TECHNOLOGY PILLS
# ===========================

def tech_stack(tech_list):
    html = ""
    for tech in tech_list:
        html += f"<span class='tech-pill'>{tech}</span>"
    st.markdown(html, unsafe_allow_html=True)


# ===========================
# ROADMAP
# ===========================

def roadmap(phases):
    st.markdown(
        """
        <div class="glass-card">
            <h3>🛣 Development Roadmap</h3>
        """,
        unsafe_allow_html=True
    )
    for phase in phases:
        st.markdown(f"✅ {phase}<br><br>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ===========================
# JSON VIEWER
# ===========================

def json_view(data):

    st.json(data)


import json
import os

# ===========================
# BLUEPRINT VISUALIZER
# ===========================

def blueprint_visualizer(project):
    overview = project.get("project_overview", {})
    stakeholders = project.get("stakeholders", {})
    requirements = project.get("requirements", {})
    features = project.get("features", {})
    architecture = project.get("architecture", {})
    dev_plan = project.get("development_plan", {})
    risks = project.get("risks", {})
    ai_recs = project.get("ai_recommendations", {})
    learning = project.get("learning_roadmap", {})
    future = project.get("future_scope", {})

    st.markdown(f"<h2 style='color:#38BDF8;'>📄 {overview.get('project_name', 'Unnamed Project')}</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs([
        "📋 Overview", 
        "👥 Stakeholders", 
        "🏗 Architecture", 
        "🛠 Req & Features", 
        "📅 Roadmap", 
        "⚠️ Risks & Mitigation",
        "🧠 AI & Learning",
        "💾 Download"
    ])

    with tabs[0]:
        st.markdown("### 🔍 Project Overview")
        c1, c2 = st.columns(2)
        with c1:
            glass_card("Objective", overview.get("project_objective", "Not specified"))
        with c2:
            glass_card("Business Problem", overview.get("business_problem", "Not specified"))
            
        st.markdown(f"""
        <div class='glass-card'>
            <h3>Detailed Description</h3>
            <p>{overview.get('project_description', 'No description provided.')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        target = overview.get("target_users", "")
        if isinstance(target, list):
            target = ", ".join(target)
        if target:
            glass_card("Target Users", target)

    with tabs[1]:
        st.markdown("### 👥 Stakeholders & Roles")
        has_roles = False
        
        # Display specific role classifications if they exist
        for category in ["users", "developers", "administrators"]:
            roles = stakeholders.get(category, [])
            if roles:
                st.markdown(f"#### {category.title()}")
                has_roles = True
                cols = st.columns(min(len(roles), 3))
                for idx, r in enumerate(roles):
                    with cols[idx % min(len(roles), 3)]:
                        if isinstance(r, dict):
                            role_name = r.get("role") or r.get("role_name") or "Role"
                            desc = r.get("description") or ""
                        else:
                            role_name = str(r)
                            desc = ""
                        
                        desc_html = f'<div style="font-size:13px; color:#CBD5E1; margin-top:5px; line-height:1.4;">{desc}</div>' if desc else ""
                        st.markdown(f"""
                        <div class="metric-card" style="margin-bottom:15px; text-align:left; min-height:100px;">
                            <div style="font-weight:700; color:#38BDF8; font-size:16px;">{role_name}</div>
                            {desc_html}
                        </div>
                        """, unsafe_allow_html=True)
                        
        # Fallback to general user roles or listing
        if not has_roles:
            user_roles = stakeholders.get("user_roles", [])
            target_users = stakeholders.get("target_users", [])
            
            if target_users:
                st.markdown("#### Target Users")
                tech_stack(target_users)
                st.markdown("<br>", unsafe_allow_html=True)
                
            if user_roles:
                st.markdown("#### User Roles")
                cols = st.columns(min(len(user_roles), 3))
                for idx, r in enumerate(user_roles):
                    with cols[idx % min(len(user_roles), 3)]:
                        if isinstance(r, dict):
                            role_name = r.get("role_name") or r.get("role") or "Role"
                            desc = r.get("description") or ""
                        else:
                            role_name = str(r)
                            desc = ""
                        
                        desc_html = f'<div style="font-size:13px; color:#CBD5E1; margin-top:5px; line-height:1.4;">{desc}</div>' if desc else ""
                        st.markdown(f"""
                        <div class="metric-card" style="margin-bottom:15px; text-align:left; min-height:100px;">
                            <div style="font-weight:700; color:#38BDF8; font-size:16px;">{role_name}</div>
                            {desc_html}
                        </div>
                        """, unsafe_allow_html=True)
                        has_roles = True
                        
        if not has_roles and not target_users:
            st.info("No specific stakeholder roles specified in the blueprint.")

    with tabs[2]:
        st.markdown("### 🏗 Software Architecture")
        style = architecture.get("architecture_style") or architecture.get("software_architecture") or "Not specified"
        desc = architecture.get("architecture_description") or ""
        
        st.markdown(f"""
        <div class="glass-card">
            <h4>Architecture Design Pattern: <span style="color:#38BDF8;">{style}</span></h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Technology Stack
        tech = project.get("technology_stack", {}) or architecture.get("technology_stack", {})
        if tech:
            st.markdown("#### 🛠 Technology Stack")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown("**Frontend**")
                val = tech.get("frontend", "N/A")
                tech_stack([val] if isinstance(val, str) else val)
            with c2:
                st.markdown("**Backend**")
                val = tech.get("backend", "N/A")
                tech_stack([val] if isinstance(val, str) else val)
            with c3:
                st.markdown("**Database**")
                val = tech.get("database", "N/A")
                tech_stack([val] if isinstance(val, str) else val)
            with c4:
                st.markdown("**AI / ML**")
                val = tech.get("ai_ml") or tech.get("ai") or "N/A"
                tech_stack([val] if isinstance(val, str) else val)

        # Components
        comps = architecture.get("components", [])
        if comps:
            st.markdown("<br>#### 🧩 System Architecture Components", unsafe_allow_html=True)
            cols = st.columns(min(len(comps), 3))
            for idx, comp in enumerate(comps):
                with cols[idx % min(len(comps), 3)]:
                    if isinstance(comp, dict):
                        c_name = comp.get("name") or comp.get("component_name") or "Component"
                        c_desc = comp.get("description") or ""
                    else:
                        c_name = str(comp)
                        c_desc = ""
                    
                    desc_html = f'<p style="font-size:13px; margin-bottom:0; line-height:1.4; color:#CBD5E1;">{c_desc}</p>' if c_desc else ""
                    st.markdown(f"""
                    <div class="glass-card" style="padding:18px; min-height:140px; margin-bottom:15px;">
                        <h4 style="color:#60A5FA; margin-top:0; margin-bottom:8px;">{c_name}</h4>
                        {desc_html}
                    </div>
                    """, unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("### 📋 Requirements & Features")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='glass-card' style='min-height:350px;'>", unsafe_allow_html=True)
            st.markdown("#### ⚙ Functional Requirements")
            for req in requirements.get("functional_requirements", []):
                st.markdown(f"- {req}")
            if not requirements.get("functional_requirements"):
                st.write("*None specified.*")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-card' style='min-height:350px; margin-top:15px;'>", unsafe_allow_html=True)
            st.markdown("#### 🌟 Core Features")
            for feat in features.get("core_features", []):
                st.markdown(f"- {feat}")
            if not features.get("core_features"):
                st.write("*None specified.*")
            st.markdown("</div>", unsafe_allow_html=True)
                
        with c2:
            st.markdown("<div class='glass-card' style='min-height:350px;'>", unsafe_allow_html=True)
            st.markdown("#### 🔒 Non-Functional Requirements")
            for req in requirements.get("non_functional_requirements", []):
                st.markdown(f"- {req}")
            if not requirements.get("non_functional_requirements"):
                st.write("*None specified.*")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-card' style='min-height:350px; margin-top:15px;'>", unsafe_allow_html=True)
            st.markdown("#### 🚀 Advanced / Additional Features")
            add_feats = features.get("additional_features", []) or features.get("advanced_features", [])
            for feat in add_feats:
                st.markdown(f"- {feat}")
            if not add_feats:
                st.write("*None specified.*")
            st.markdown("</div>", unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("### 📅 Development Plan & Phased Timeline")
        duration = dev_plan.get("total_duration") or dev_plan.get("estimated_duration") or "Not estimated"
        
        st.markdown(f"""
        <div class="metric-card" style="padding:12px; margin-bottom:20px; display:inline-block;">
            Estimated Duration: <span style="font-weight:700; color:#38BDF8;">{duration}</span>
        </div>
        """, unsafe_allow_html=True)
        
        phases = dev_plan.get("phases", [])
        if phases:
            # Render each phase cleanly
            for idx, phase in enumerate(phases):
                p_name = phase.get("phase") or phase.get("phase_name") or f"Phase {idx+1}"
                p_dur = phase.get("duration") or ""
                p_tasks = phase.get("tasks", [])
                
                header_text = f"{p_name}"
                if p_dur:
                    header_text += f" ({p_dur})"
                    
                with st.expander(f"📍 {header_text}", expanded=True):
                    for task in p_tasks:
                        st.markdown(f"✅ {task}")
        else:
            st.info("No phased development timeline specified.")

    with tabs[5]:
        st.markdown("### ⚠️ Risks & Mitigation Strategies")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='glass-card' style='min-height:220px;'>", unsafe_allow_html=True)
            st.markdown("#### 💻 Technical Risks")
            for risk in risks.get("technical_risks", []):
                st.markdown(f"• {risk}")
            if not risks.get("technical_risks"):
                st.write("*None specified.*")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='glass-card' style='min-height:220px;'>", unsafe_allow_html=True)
            st.markdown("#### 💼 Business & Operational Risks")
            b_risks = risks.get("business_risks") or risks.get("operational_risks") or []
            for risk in b_risks:
                st.markdown(f"• {risk}")
            if not b_risks:
                st.write("*None specified.*")
            st.markdown("</div>", unsafe_allow_html=True)
                
        st.markdown("#### 🛡 Mitigation Strategies")
        for strategy in risks.get("mitigation_strategies", []):
            st.markdown(f"✅ {strategy}")
        if not risks.get("mitigation_strategies"):
            st.write("*None specified.*")

    with tabs[6]:
        st.markdown("### 🧠 AI Model Recommendations & Learning Plan")
        
        # AI Recommendations
        st.markdown("#### 🤖 AI Recommendations")
        ai_models = ai_recs.get("ai_models") or ai_recs.get("recommendations") or []
        
        # Check if recommendations list contains dictionaries or strings
        for m in ai_models:
            if isinstance(m, dict):
                model_name = m.get("model") or m.get("recommendation") or "AI Service"
                desc = m.get("description") or ""
                st.markdown(f"🤖 **{model_name}**: {desc}")
            else:
                st.markdown(f"- {m}")
        if not ai_models:
            st.write("*None specified.*")
            
        ai_int = ai_recs.get("ai_integration", [])
        if ai_int:
            st.markdown("<br>#### 🔌 AI Integration Steps", unsafe_allow_html=True)
            for step in ai_int:
                st.markdown(f"⚡ {step}")

        st.markdown("<br>#### 📚 Learning Roadmap", unsafe_allow_html=True)
        tech_skills = learning.get("technical_skills") or learning.get("recommended_skills") or []
        biz_skills = learning.get("business_skills") or learning.get("learning_resources") or []
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Core Skills to Acquire**")
            for s in tech_skills:
                st.markdown(f"- {s}")
            if not tech_skills:
                st.write("*None specified.*")
        with col2:
            st.markdown("**Learning Resources / Supporting Skills**")
            for s in biz_skills:
                st.markdown(f"- {s}")
            if not biz_skills:
                st.write("*None specified.*")

    with tabs[7]:
        st.markdown("### 💾 Export Blueprint")
        json_str = json.dumps(project, indent=4)
        
        st.download_button(
            label="💾 Download Blueprint JSON",
            data=json_str,
            file_name=f"{overview.get('project_name', 'blueprint').lower().replace(' ', '_')}.json",
            mime="application/json"
        )
        
        st.markdown("<br>#### Raw JSON Output", unsafe_allow_html=True)
        st.code(json_str, language="json")


# ===========================
# SIDEBAR
# ===========================

def sidebar():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    st.sidebar.markdown(
        """
        <div style='text-align: center; padding-top: 15px; margin-bottom: 25px;'>
            <h1 style='font-size: 26px; font-weight: 900; background: linear-gradient(135deg, #60a5fa, #38bdf8, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px; letter-spacing: -0.5px;'>ProjectForge AI</h1>
            <span style='color: #38BDF8; font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase;'>Planning Assistant</span>
        </div>
        <hr style='border-color: rgba(255,255,255,0.06); margin-top:0; margin-bottom: 20px;'>
        """,
        unsafe_allow_html=True
    )

    page_options = [
        "🏠 Dashboard",
        "➕ New Project",
        "📂 Saved Blueprints",
        "🧠 Project Embeddings",
        "🔍 Semantic Search",
        "💬 Architecture Chat",
        "⚙ Settings"
    ]

    route_to_option = {
        "Dashboard": "🏠 Dashboard",
        "NewProject": "➕ New Project",
        "SavedBlueprints": "📂 Saved Blueprints",
        "Embeddings": "🧠 Project Embeddings",
        "SemanticSearch": "🔍 Semantic Search",
        "AIChat": "💬 Architecture Chat",
        "Settings": "⚙ Settings"
    }
    option_to_route = {v: k for k, v in route_to_option.items()}

    current_route = st.session_state.current_page
    default_index = 0
    if current_route in route_to_option:
        default_index = page_options.index(route_to_option[current_route])

    selected_option = st.sidebar.radio(
        "Navigation",
        page_options,
        index=default_index,
        label_visibility="collapsed"
    )

    selected_route = option_to_route[selected_option]
    if selected_route != current_route:
        st.session_state.current_page = selected_route
        st.rerun()

    # Footer
    st.sidebar.markdown(
        """
        <div style='position: fixed; bottom: 15px; width: 250px; text-align: center; font-size: 11px; color: rgba(255,255,255,0.25); border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;'>
            ProjectForge AI v1.0 • Running Locally
        </div>
        """,
        unsafe_allow_html=True
    )


# ===========================
# DASHBOARD METRICS
# ===========================

def dashboard_metrics():
    total_projects = 0
    total_embeddings = 0
    embedding_dim = 384

    if os.path.exists("data/projects.json"):
        try:
            with open("data/projects.json", "r") as file:
                projects = json.load(file)
                total_projects = len(projects)
        except Exception:
            pass

    if os.path.exists("data/project_embeddings.json"):
        try:
            with open("data/project_embeddings.json", "r") as file:
                embeddings = json.load(file)
                total_embeddings = len(embeddings)
        except Exception:
            pass

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card("Total Blueprints", str(total_projects))

    with c2:
        metric_card("Active Embeddings", str(total_embeddings))

    with c3:
        metric_card("Vector Dimension", str(embedding_dim))