from models.llm import model
from prompts.project_prompt import project_prompt


class ProjectAnalyzer:

    def __init__(self):
        self.chain = project_prompt | model

    def analyze(self, project_idea: str):
        response = self.chain.invoke(
            {
                "project_idea": project_idea
            }
        )

        return response.content