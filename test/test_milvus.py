cat > test_milvus.py << 'EOF'
"""测试 Milvus 连接 + 插入 + 检索"""
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
import random

# 连接
connections.connect(host="localhost", port="19530")
print("✅ 已连接 Milvus")

# 建集合
COLLECTION = "test_rag"
if utility.has_collection(COLLECTION):
    utility.drop_collection(COLLECTION)

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128),
]
schema = CollectionSchema(fields)
col = Collection(COLLECTION, schema)
print("✅ 集合已创建")

# 插入测试数据
test_chunks = ["Python 是动态语言", "Milvus 是向量数据库", "RAG 结合检索与生成"]
test_vectors = [[random.random() for _ in range(128)] for _ in test_chunks]
col.insert([test_chunks, test_vectors])
col.flush()
print("✅ 插入 3 条数据")

# 建索引
col.create_index("embedding", {"metric_type": "COSINE", "index_type": "IVF_FLAT", "params": {"nlist": 128}})
col.load()
print("✅ 索引就绪")

# 检索
query_vec = [random.random() for _ in range(128)]
results = col.search(
    data=[query_vec],
    anns_field="embedding",
    param={"metric_type": "COSINE", "params": {"nprobe": 10}},
    limit=3,
    output_fields=["content"],
)
print("\n📚 检索结果:")
for hit in results[0]:
    print(f"  [{hit.distance:.4f}] {hit.entity.content}")

connections.disconnect("default")
print("\n✅ 全链路通过")
EOF