import json
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from models.llm import model


class ChatService:

    def __init__(self):
        self.model = model

    def get_response(self, chat_history: list, project_blueprint: dict = None):
        """
        Gets response from the LLM based on user prompt and conversation history,
        injecting the selected project's blueprint context if available.
        """
        system_prompt = (
            "You are ProjectForge AI Chat assistant, an expert Product Manager, "
            "Software Architect, and Tech Lead. Your goal is to help the user plan, "
            "refine, design, and write technical specifications for their software project.\n\n"
            "Keep your responses professional, insightful, and technical. Use markdown formatting "
            "for code snippets, lists, and headings.\n\n"
        )

        if project_blueprint:
            name = project_blueprint.get("project_overview", {}).get("project_name", "Selected Project")
            system_prompt += (
                f"You are currently chatting in the context of the project: **{name}**.\n"
                f"Here is the project blueprint in JSON format to help you answer their questions contextually:\n"
                f"```json\n{json.dumps(project_blueprint, indent=2)}\n```\n\n"
                "Please reference these details, requirements, stack, and roadmap elements in your answers."
            )
        else:
            system_prompt += (
                "Currently, no specific project is selected. You can help the user brainstorm new ideas, "
                "discuss software architecture, or guide them through creating a new blueprint."
            )

        messages = [SystemMessage(content=system_prompt)]

        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        try:
            response = self.model.invoke(messages)
            return response.content
        except Exception as e:
            return f"⚠️ **Error connecting to AI Model**: {str(e)}\n\nPlease ensure your MISTRAL_API_KEY is correctly configured in your `.env` file."
