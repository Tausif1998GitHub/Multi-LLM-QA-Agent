import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================================================
# LOAD EMBEDDING MODEL ONLY ONCE
# =========================================================

print("\n[FAISS] Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("[FAISS] Embedding model loaded.")

# =========================================================
# GLOBAL VARIABLES
# =========================================================

GLOBAL_POLICIES = []

GLOBAL_INDEX = None

IS_INITIALIZED = False


# =========================================================
# VECTOR STORE
# =========================================================

class PolicyVectorStore:

    def __init__(self):

        global IS_INITIALIZED

        # ================================================
        # INITIALIZE ONLY ONCE
        # ================================================

        if not IS_INITIALIZED:

            print("\n[FAISS] Initializing vector store...")

            self.load_policies(
                "policies/policies.txt"
            )

            IS_INITIALIZED = True

            print("[FAISS] Vector store ready.")

    # =====================================================
    # LOAD POLICIES
    # =====================================================

    def load_policies(self, filepath):

        global GLOBAL_POLICIES
        global GLOBAL_INDEX

        # ================================================
        # RESET EVERYTHING
        # ================================================

        GLOBAL_POLICIES = []

        GLOBAL_INDEX = faiss.IndexFlatL2(384)

        # ================================================
        # LOAD FILE
        # ================================================

        with open(filepath, "r", encoding="utf-8") as f:

            content = f.read()

        # ================================================
        # SPLIT POLICIES
        # ================================================

        GLOBAL_POLICIES = [

            p.strip()

            for p in content.split("Policy")

            if p.strip()
        ]

        # ================================================
        # CREATE EMBEDDINGS
        # ================================================

        embeddings = embedding_model.encode(
            GLOBAL_POLICIES
        )

        embeddings = np.array(
            embeddings
        ).astype("float32")

        # ================================================
        # ADD TO FAISS
        # ================================================

        GLOBAL_INDEX.add(embeddings)

    # =====================================================
    # SEARCH
    # =====================================================

    def search(self, query, top_k=3):

        global GLOBAL_POLICIES
        global GLOBAL_INDEX

        query_embedding = embedding_model.encode(
            [query]
        )

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        distances, indices = GLOBAL_INDEX.search(
            query_embedding,
            top_k
        )

        # ================================================
        # SAFE INDEX ACCESS
        # ================================================

        results = []

        for i in indices[0]:

            if i < len(GLOBAL_POLICIES):

                results.append(
                    GLOBAL_POLICIES[i]
                )

        return results