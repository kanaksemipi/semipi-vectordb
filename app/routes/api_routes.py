from flask import Blueprint, request, jsonify
from app.chroma_client import get_chroma_collection
from uuid import uuid4
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List, Optional, Literal
from datetime import datetime
from sentence_transformers import SentenceTransformer
from app.auth import require_api_key

import json

collection = get_chroma_collection()

embedding_model = SentenceTransformer("BAAI/bge-large-en")
api_bp = Blueprint('api', __name__)

class PropertyMetadata(BaseModel):
    mode: Literal["developer", "customer"]
    type: Literal["project", "unit", "lead"]
    project_name: str
    developer: str
    location: str
    property_type: str
    price: Optional[float] = None
    possession_date: str
    features: Optional[List[str]] = None
    floor_plan_url: Optional[str] = None
    brochure_url: Optional[str] = None
    source: Literal["uploaded_document", "scraped_web", "manual"]
    timestamp: str

    @field_validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("timestamp must be in ISO format (YYYY-MM-DDTHH:MM:SS)")

def prepare_metadata(metadata: PropertyMetadata):
	md=metadata.model_dump()
	cleaned_md={}
	for k,v in md.items():
		if v is None: 
			continue
		elif isinstance(v,list):
			cleaned_md[k]=json.dumps(v)
		else:
			cleaned_md[k]=v
	return cleaned_md


# ---------- API 1: Add Data ----------
#Authenticate
@api_bp.route('/add_data', methods=['POST'])
@require_api_key
def add_data():
    data = request.json
    id = data.get("id", str(uuid4()))
    document = data.get("document")
    metadata_dict = data.get("metadata")

    if not document or not metadata_dict:
        return jsonify({"error": "Both 'document' and 'metadata' are required."}), 400

    try:
        metadata = PropertyMetadata(**metadata_dict)
        cleaned_metadata = prepare_metadata(metadata)

        embedding = embedding_model.encode(document).tolist()
        collection.add(
            documents=[document],
            metadatas=[cleaned_metadata],
            embeddings=[embedding],
            ids=[id]
        )   

        return jsonify({"message": "Data added successfully.", "id": id}), 200
    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- API 2: Delete Data ----------
@api_bp.route('/delete_data/<doc_id>', methods=['DELETE'])
@require_api_key
def delete_data(doc_id):
    try:
        collection.delete(ids=[doc_id])
        return jsonify({"message": f"Document with ID '{doc_id}' deleted."}), 200
    except Exception as e:
           return jsonify({"error": str(e)}), 500

# ---------- API 3: Update Data ----------
@api_bp.route('/update_data', methods=['POST'])
@require_api_key
def update_data():
    data = request.json
    id = data.get("id")
    new_metadata_dict = data.get("metadata")

    if not id or not new_metadata_dict:
        return jsonify({"error": "Both 'id' and 'metadata' are required."}), 400

    try:
        new_metadata = PropertyMetadata(**new_metadata_dict)
        cleaned_metadata = prepare_metadata(new_metadata)

        existing = collection.get(ids=[id])
        if not existing['documents']:
            return jsonify({"error": "Document not found."}), 404

        document = existing['documents'][0]
        embedding = embedding_model.encode(document).tolist()  
        collection.delete(ids=[id])
        collection.add(
            documents=[document],
            metadatas=[cleaned_metadata],
            ids=[id],
            embeddings=[embedding]  
        )
        return jsonify({"message": f"Metadata updated for ID '{id}'."}), 200
    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- API 4: Query DB ----------
@api_bp.route('/query_db', methods=['POST'])
@require_api_key
def query_db():
    data = request.json
    query = data.get("query")
    n_results = data.get("n_results", 10)

    if not query:
        return jsonify({"error": "Query text is required."}), 400

    try:
        query_embedding = embedding_model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- API 5: Generate Embedding ----------
@api_bp.route('/generate_embedding', methods=['POST'])
@require_api_key
def generate_embedding():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text input is required."}), 400

    try:
        embedding = embedding_model.encode(text).tolist()
        return jsonify({"embedding": embedding}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- API 6: View All Data ----------
@api_bp.route('/view_all', methods=['GET'])
@require_api_key
def view_all():
    try:
        results = collection.get()

        for md in results.get("metadatas", []):
            if isinstance(md.get("features"), str):
                try:
                    md["features"] = json.loads(md["features"])
                except json.JSONDecodeError:
                    pass

        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
