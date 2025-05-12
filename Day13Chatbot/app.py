from flask import Flask, render_template, request, session
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mistralai import ChatMistralAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
import os
from uuid import uuid4

app = Flask(__name__)
app.secret_key = os.urandom(24)  


llm = ChatMistralAI(
    api_key=os.getenv("MISTRAL_API_KEY", "zycyPOcxBLJpE6Mxo9eWE3dTUMFaeW41"),  # Replace with your actual API key or use env variable
    model="mistral-small-latest",
    temperature=0.7
)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Use the conversation history to provide context for your response. Respond concisely and accurately."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])


chain = prompt | llm


store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversation = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

@app.route("/", methods=["GET", "POST"])
def index():
    
    if 'session_id' not in session:
        session['session_id'] = str(uuid4())
    
    session_id = session['session_id']
    chat_history = get_session_history(session_id).messages
    response = None

    if request.method == "POST":
        user_input = request.form.get('query', '').strip()
        if user_input:
            try:
                
                result = conversation.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": session_id}}
                )
                response = result.content
                
                chat_history = get_session_history(session_id).messages
            except Exception as e:
                response = f"Error: {str(e)}"
                chat_history = get_session_history(session_id).messages
    
    return render_template(
        'index.html',
        response=response,
        chat_history=chat_history
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)