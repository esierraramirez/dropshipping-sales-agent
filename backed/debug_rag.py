#!/usr/bin/env python3
"""Script para debuggear el RAG y ver por qué no retorna productos"""

import sys
sys.path.insert(0, '/backed')

from app.models.vendor import Vendor
from app.services.retrieval_service import retrieve_vendor_context
from app.rag.retriever import retrieve_documents

# Crear un vendor dummy
class DummyVendor:
    def __init__(self):
        self.name = "Akari Cafe"
        self.slug = "akari-cafe"
        self.id = 4

vendor = DummyVendor()

# Test queries
queries = [
    "Estoy interesado en una camisa para Bogota que es muy fría",
    "¿Qué productos tienes?",
    "Quiero una camisa",
    "Qué camisas manejan",
]

print("=" * 80)
print("TESTING RAG RETRIEVAL")
print("=" * 80)

for query in queries:
    print(f"\n📝 Query: '{query}'")
    
    result = retrieve_vendor_context(
        vendor=vendor,
        query=query,
        top_k=3
    )
    
    print(f"   Knowledge base ready: {result['knowledge_base_ready']}")
    print(f"   Total matches: {result['total_matches']}")
    print(f"   Results: {len(result['results'])} items")
    
    if result['results']:
        for item in result['results']:
            print(f"   • {item['name']} (score: {item['score']})")
    else:
        print("   ❌ NO RESULTS")

print("\n" + "=" * 80)
