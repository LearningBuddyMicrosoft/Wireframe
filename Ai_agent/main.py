import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from tools import load_pdf_tool, load_image_tool, search_tool

load_dotenv()

# -------------------------------------------------
# Structured output model
# -------------------------------------------------
class ResponseModel(BaseModel):
    topic: str
    summary: str
    source: List[str]
    tools_used: List[str]


# -------------------------------------------------
# LLM + parser
# -------------------------------------------------
llm = ChatOllama(
    model="qwen2.5:7b-instruct",
    temperature=0.4,
    options={"num_ctx": 4096},
)

parser = PydanticOutputParser(pydantic_object=ResponseModel)


# -------------------------------------------------
# Automatic PDF detection
# -------------------------------------------------
PDF_DIR = "pdfs"

def find_matching_pdf(user_query: str) -> Optional[str]:
    """Try to find a PDF in the pdfs/ folder that matches the user query."""
    if not os.path.exists(PDF_DIR):
        return None

    files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    if not files:
        return None

    # Exact match
    for f in files:
        name = f.lower().replace(".pdf", "")
        if name in user_query.lower():
            return os.path.join(PDF_DIR, f)

    # Keyword match
    for f in files:
        if any(word in f.lower() for word in user_query.lower().split()):
            return os.path.join(PDF_DIR, f)

    # If only one PDF exists, assume it's the one
    if len(files) == 1:
        return os.path.join(PDF_DIR, files[0])

    return None


# -------------------------------------------------
# Detect tool intent from natural language
# -------------------------------------------------
def detect_tool_intent(text: str) -> Optional[str]:
    t = text.lower()

    if "pdf" in t or "read the pdf" in t or "document" in t:
        return "pdf"

    if "image" in t or "picture" in t or "extract text from the image" in t:
        return "image"

    if "search" in t or "internet" in t or "look up" in t or "google" in t:
        return "search"

    return None


# -------------------------------------------------
# Run the chosen tool
# -------------------------------------------------
def run_tool(tool_name: str, user_query: str):
    tools_used = []
    source = []
    result_text = ""

    if tool_name == "pdf":
        auto_path = find_matching_pdf(user_query)

        if auto_path:
            print(f"[Auto-detected PDF]: {auto_path}")
            file_path = auto_path
        else:
            file_name = input("Enter PDF filename (inside pdfs/): ")
            file_path = os.path.join(PDF_DIR, file_name)

        result_text = load_pdf_tool(file_path)
        tools_used.append("load_pdf_tool")
        source.append(file_path)

    elif tool_name == "image":
        file_path = input("Enter image path: ")
        result_text = load_image_tool(file_path)
        tools_used.append("load_image_tool")
        source.append(file_path)

    elif tool_name == "search":
        result_text = search_tool(user_query)
        tools_used.append("search_tool")
        source.append("web_search")

    return result_text, tools_used, source


# -------------------------------------------------
# Prompt: first pass (decide if tools are needed)
# -------------------------------------------------
tool_decision_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful study assistant.

First, think about whether you need to use any tools:
- PDF tool: when the user asks about a document or PDF.
- Image tool: when the user asks about an image or picture.
- Search tool: when the user asks about current information or facts you are unsure about.

Respond in natural language, explaining whether you need a tool.
If you need a tool, clearly say things like:
- "You should read the PDF first."
- "You should extract text from the image."
- "You should search the internet for this."

If you can answer directly, say that no tools are needed and answer briefly.
            """,
        ),
        ("human", "{query}"),
    ]
)


# -------------------------------------------------
# Prompt: second pass (final JSON answer)
# -------------------------------------------------
final_answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a study assistant AI.

You MUST respond ONLY with valid JSON that matches this schema:

{format_instructions}

RULES:
- Output ONLY JSON.
- No markdown.
- No explanations.
- No natural language outside the JSON.
- If a field is unknown, use "" or [].
            """,
        ),
        (
            "human",
            """
User question:
{query}

Context from tools (may be empty):
{context}
            """,
        ),
    ]
).partial(format_instructions=parser.get_format_instructions())


# -------------------------------------------------
# Main loop
# -------------------------------------------------
def main():
    user_query = input("What can I help you research: ")

    # 1) Ask model how to handle the query
    decision_msg = tool_decision_prompt.format_messages(query=user_query)
    decision_response = llm.invoke(decision_msg)
    decision_text = decision_response.content
    print("\n[Model decision]:", decision_text)

    # 2) Detect tool intent
    tool_name = detect_tool_intent(decision_text)

    context_text = ""
    tools_used = []
    source = []

    if tool_name:
        print(f"\n[Tool detected]: {tool_name}")
        context_text, tools_used, source = run_tool(tool_name, user_query)
    else:
        print("\n[No tool detected]")

    # 3) Ask model for final structured JSON answer
    final_msg = final_answer_prompt.format_messages(
        query=user_query,
        context=context_text,
    )
    final_response = llm.invoke(final_msg)

    try:
        structured = parser.parse(final_response.content)

        # Patch in tools_used/source if model leaves them empty
        if not structured.tools_used and tools_used:
            structured.tools_used = tools_used
        if not structured.source and source:
            structured.source = source

        print("\nStructured Output:\n", structured)

    except Exception as e:
        print("\nParsing error:", e)
        print("Raw final response:", final_response)


if __name__ == "__main__":
    main()