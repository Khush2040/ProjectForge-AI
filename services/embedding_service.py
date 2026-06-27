import json
import os
import numpy as np

from embeddings.embedding_model import embedding_model


def get_project_document(project):
    overview = project.get("project_overview", {})
    requirements = project.get("requirements", {})
    features = project.get("features", {})
    
    # Extract technology stack from either top-level or under architecture
    tech = project.get("technology_stack", {})
    if not tech and "architecture" in project:
        tech = project.get("architecture", {}).get("technology_stack", {})
    
    # Safely convert lists of requirements/features to strings
    func_reqs = requirements.get("functional_requirements", [])
    non_func_reqs = requirements.get("non_functional_requirements", [])
    core_feats = features.get("core_features", [])
    add_feats = features.get("additional_features", []) or features.get("advanced_features", [])

    if isinstance(func_reqs, list):
        func_reqs = "\n".join(func_reqs)
    if isinstance(non_func_reqs, list):
        non_func_reqs = "\n".join(non_func_reqs)
    if isinstance(core_feats, list):
        core_feats = "\n".join(core_feats)
    if isinstance(add_feats, list):
        add_feats = "\n".join(add_feats)

    document = f"""
Project Name:
{overview.get("project_name", "")}

Description:
{overview.get("project_description", "")}

Business Problem:
{overview.get("business_problem", "")}

Objective:
{overview.get("project_objective", "")}

Functional Requirements:
{func_reqs}

Non Functional Requirements:
{non_func_reqs}

Core Features:
{core_feats}

Additional Features:
{add_feats}

Technology Stack:
Frontend: {tech.get("frontend", "")}
Backend: {tech.get("backend", "")}
Database: {tech.get("database", "")}
AI: {tech.get("ai_ml", "") or tech.get("ai", "")}
"""
    return document.strip()


def generate_embeddings():
    file_path = "data/projects.json"
    if not os.path.exists(file_path):
        return [], []

    with open(file_path, "r") as file:
        try:
            projects = json.load(file)
        except Exception:
            projects = []

    if not projects:
        return [], []

    documents = [get_project_document(project) for project in projects]
    vectors = embedding_model.embed_documents(documents)

    # Save vectors to cache
    embeddings_data = []
    for project, vector in zip(projects, vectors):
        name = project.get("project_overview", {}).get("project_name", "Untitled Project")
        embeddings_data.append({
            "project_name": name,
            "vector": vector
        })

    os.makedirs("data", exist_ok=True)
    with open("data/project_embeddings.json", "w") as file:
        json.dump(embeddings_data, file, indent=4)

    return vectors, projects


def semantic_search(query: str, top_k: int = 3):
    file_path = "data/projects.json"
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as file:
        try:
            projects = json.load(file)
        except Exception:
            projects = []

    if not projects:
        return []

    # Try to load cached embeddings
    embeddings_path = "data/project_embeddings.json"
    vectors = []
    if os.path.exists(embeddings_path):
        try:
            with open(embeddings_path, "r") as file:
                cached = json.load(file)
            if len(cached) == len(projects):
                vectors = [c["vector"] for c in cached]
        except Exception:
            pass

    # If cache is missing or mismatched, regenerate
    if not vectors:
        vectors, _ = generate_embeddings()

    if not vectors:
        return []

    # Embed query
    query_vector = embedding_model.embed_query(query)
    q_vec = np.array(query_vector)

    results = []
    for idx, project in enumerate(projects):
        p_vec = np.array(vectors[idx])
        dot_product = np.dot(q_vec, p_vec)
        norm_q = np.linalg.norm(q_vec)
        norm_p = np.linalg.norm(p_vec)
        similarity = dot_product / (norm_q * norm_p) if norm_q > 0 and norm_p > 0 else 0.0
        results.append({
            "project": project,
            "score": float(similarity)
        })

    # Sort descending by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]