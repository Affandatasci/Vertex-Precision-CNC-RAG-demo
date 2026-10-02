import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# --- Clients ---
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
embedder = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0, max_tokens=700, api_key=os.getenv("GROQ_API_KEY"))
COLLECTION = os.getenv("QDRANT_COLLECTION", "vertex-precision-rag")

with open("orders.json", "r") as f:
    ORDERS = json.load(f)

# --- Tools ---
@tool
def search_knowledge_base(query: str) -> str:
    """Search Vertex Precision Engineering product catalogue, capabilities, materials, pricing and FAQs."""
    vec = embedder.embed_query(query)
    results = qdrant.search(collection_name=COLLECTION, query_vector=vec, limit=5)
    if not results:
        return "No relevant information found in the knowledge base."
    return "\n\n".join([r.payload.get("text", "") for r in results])

@tool
def lookup_order(order_id: str) -> str:
    """Look up a CNC machining order by order ID (e.g. VPE-1001)."""
    order_id = order_id.strip().upper()
    for order in ORDERS:
        if order["order_id"] == order_id:
            items_str = "\n".join(
                f"  - {i['part']} x{i['qty']} @ £{i['unit_price_gbp']:.2f} each"
                for i in order["items"]
            )
            return (
                f"Order ID: {order['order_id']}\n"
                f"Customer: {order['customer_name']}\n"
                f"Order Date: {order['order_date']}\n"
                f"Status: {order['status']}\n"
                f"Estimated Delivery: {order['estimated_delivery']}\n"
                f"Items:\n{items_str}\n"
                f"Total: £{order['total_gbp']:.2f}\n"
                f"Notes: {order['notes']}"
            )
    return f"Order {order_id} not found. Please check the order ID and try again."

# --- System Prompt ---
SYSTEM_PROMPT = """You are the AI assistant for Vertex Precision Engineering Ltd, a CNC machining and mechanical components manufacturer based in the West Midlands, UK.

You help customers with:
- Product enquiries (CNC turned parts, milled parts, bearings, rotors, gears, hydraulic fittings, fasteners)
- Material selection (steels, aluminium alloys, titanium, Inconel, PEEK, Delrin)
- Manufacturing capabilities and tolerances
- Pricing and lead times
- Order tracking
- Quote requests
- Quality certifications (ISO 9001:2015, AS9100D)

Always be professional, precise and helpful. Use £ for prices. If asked about pricing give ranges from the knowledge base. For order lookups, always use the lookup_order tool with the exact order ID (format: VPE-XXXX).

If you cannot answer from the knowledge base or order data, say: "Please contact our team at enquiries@vertexprecision.co.uk or call +44 121 456 7890."

Do not make up specifications, prices or delivery times that are not in the knowledge base."""

# --- Agent ---
tools = [search_knowledge_base, lookup_order]
agent = create_react_agent(llm, tools)

def run_agent(user_message: str) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, HumanMessage(content=user_message)]
    result = agent.invoke({"messages": messages})
    return result["messages"][-1].content