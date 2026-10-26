"""Test script to diagnose sentence-transformers issues"""
import sys
from pathlib import Path

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print()

# Test 1: Import sentence_transformers
try:
    import sentence_transformers
    print("✅ sentence_transformers imported successfully")
    print(f"   Version: {sentence_transformers.__version__}")
except Exception as e:
    print(f"❌ Failed to import sentence_transformers: {e}")
    sys.exit(1)

# Test 2: Import SentenceTransformer class
try:
    from sentence_transformers import SentenceTransformer
    print("✅ SentenceTransformer class imported")
except Exception as e:
    print(f"❌ Failed to import SentenceTransformer class: {e}")
    sys.exit(1)

# Test 3: Load the model
model_name = "paraphrase-multilingual-MiniLM-L12-v2"
print(f"\nAttempting to load model: {model_name}")
try:
    model = SentenceTransformer(model_name)
    print(f"✅ Model loaded successfully")
    print(f"   Embedding dimension: {model.get_sentence_embedding_dimension()}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Encode a test sentence
try:
    test_text = ["Ceci est un test"]
    embeddings = model.encode(test_text, normalize_embeddings=True)
    print(f"✅ Successfully encoded test text")
    print(f"   Embedding shape: {embeddings.shape}")
    print(f"   First 5 values: {embeddings[0][:5]}")
except Exception as e:
    print(f"❌ Failed to encode text: {e}")
    sys.exit(1)

print("\n✅ All tests passed! Embeddings are working correctly.")
