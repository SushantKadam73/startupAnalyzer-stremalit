import typer
from rich.prompt import Prompt
from typing import Optional

from phi.agent import Agent
from phi.model.google import Gemini
from phi.knowledge.docx import DocxKnowledgeBase

from phi.vectordb.chroma import ChromaDb
import os                                                                                                                                                                                                          
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
load_dotenv(Path("keys.env"))
print(os.getenv("CONNSTRING"))

from phi.embedder.google import GeminiEmbedder

embeddings = GeminiEmbedder().get_embedding("The quick brown fox jumps over the lazy dog.").model(id="gemini-1.5-flash-8b")

knowledge_base = DocxKnowledgeBase(
    path=Path("data/docs"),
    vector_db=ChromaDb(
        table_name="docx_documents",
        db_url=db_url,
    ),
)
# Comment out after first run
knowledge_base.load(recreate=True)


def pdf_agent(user: str = "user"):
    run_id: Optional[str] = None

    agent = Agent(
        model=Gemini(id="gemini-1.5-flash-8b"),
        run_id=run_id,
        user_id=user,
        knowledge_base=knowledge_base,
        use_tools=True,
        show_tool_calls=True,
        debug_mode=True,
    )
    if run_id is None:
        run_id = agent.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    while True:
        message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
        if message in ("exit", "bye"):
            break
        agent.print_response(message)


if __name__ == "__main__":
    typer.run(pdf_agent)
