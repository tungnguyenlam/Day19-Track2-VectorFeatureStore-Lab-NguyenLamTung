import time
from datetime import datetime, timezone
from typing import List, Dict, Any

from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class HybridMemoryAgent:
    def __init__(self):
        # 1. Episodic Memory (Vector Store)
        # Using multilingual model to support Vietnamese and code-switching
        self.embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        self.qdrant = QdrantClient(":memory:")
        self.collection_name = "episodic_memory"
        
        self.qdrant.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        self.memory_counter = 0

        # 2. Stable user profile (Mock Feature Store)
        # In production, this would be `fs.get_online_features(...)`
        self.feature_store: Dict[str, Dict[str, Any]] = {
            "u_001": {
                "preferred_language": "vi-en mix",
                "reading_speed_wpm": 220,
                "topic_affinity": ["cloud", "kubernetes", "ai", "security"],
            }
        }

        # 3. Recent activity (Mock Streaming Feature View)
        # In production, updated via streaming pipeline (Kafka -> Redis)
        self.streaming_features: Dict[str, Dict[str, Any]] = {
            "u_001": {
                "queries_last_hour": 12,
                "recent_focus": "infrastructure scaling",
                "fatigue_level": "moderate (late night)",
            }
        }

    def remember(self, text: str, user_id: str = "u_001") -> None:
        """Add a new piece of episodic memory for this user."""
        vector = next(self.embedder.embed([text])).tolist()
        self.memory_counter += 1
        
        point = PointStruct(
            id=self.memory_counter,
            vector=vector,
            payload={
                "user_id": user_id,
                "text": text,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
        
        self.qdrant.upsert(
            collection_name=self.collection_name, 
            points=[point]
        )
        
        # Conceptually update streaming feature
        if user_id in self.streaming_features:
            self.streaming_features[user_id]["queries_last_hour"] += 1

    def recall(self, query: str, user_id: str = "u_001") -> str:
        """Retrieve top-K memories + user profile features → return assembled context."""
        # 1. Retrieve Episodic Memory (Vector Search)
        query_vector = next(self.embedder.embed([query])).tolist()
        
        # Note: Using application-level filter for isolation in this POC.
        # Production should use Qdrant's Native Filter by payload.
        search_result = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=5
        )
        
        memories = [
            p.payload["text"] 
            for p in search_result.points 
            if p.payload.get("user_id") == user_id
        ]

        # 2. Get Stable Profile (Feature Store)
        profile = self.feature_store.get(user_id, {})

        # 3. Get Recent Activity (Streaming Features)
        activity = self.streaming_features.get(user_id, {})

        # Assemble Context
        lines = []
        lines.append(f"--- ASSEMBLED CONTEXT FOR USER: {user_id} ---")
        lines.append(f"System: You are a personal assistant. Answer based on the following user context.")
        
        lines.append("\n[Stable Profile]")
        for k, v in profile.items():
            lines.append(f"- {k}: {v}")
            
        lines.append("\n[Recent Activity]")
        for k, v in activity.items():
            lines.append(f"- {k}: {v}")
            
        lines.append("\n[Relevant Episodic Memory]")
        if not memories:
            lines.append("- (No relevant past memories found)")
        else:
            for i, mem in enumerate(memories, 1):
                lines.append(f"{i}. {mem}")
                
        lines.append(f"\nUser Query: {query}")
        
        return "\n".join(lines)
