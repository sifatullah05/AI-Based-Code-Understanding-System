from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from chains.prompt import SYSTEM_PROMPT
from utils.memory import get_history


def build_rag_chain(retriever, llm, system_prompt=SYSTEM_PROMPT):
    def build_context(question: str):
        docs = retriever.invoke(question)
        return "\n".join(doc.page_content for doc in docs)
    
    def format_history(message):
        if not message:
            return "No previous conversation."
        return "\n".join(f"{m.type.capitalize()}: {m.content}" for m in message)
    
    prompt = ChatPromptTemplate.from_template(system_prompt)
    
    base_chain = (
        {
            "question": RunnableLambda(lambda x: x["question"]),
            "context": RunnableLambda(lambda x: build_context(x["question"])),
            "history": RunnableLambda(lambda x: format_history(x["history"]))
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    source_code = RunnableWithMessageHistory(
        base_chain,
        get_history,
        input_messages_key="question",
        history_messages_key="history"
    )
    return source_code