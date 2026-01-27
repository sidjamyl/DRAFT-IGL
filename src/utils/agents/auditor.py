# src/agents/auditor.py

from pathlib import Path

from src.utils.tools.code_tools import run_pylint_on_file
from src.utils.llm.gemini_client import GeminiClient
from src.utils.logger import log_experiment, ActionType


class AuditorAgent:
    """
    Agent Auditor minimal :
    - utilise le tool run_pylint_on_file pour analyser un fichier
    - construit un prompt avec le rapport pylint
    - appelle Gemini pour obtenir un résumé
    - loggue l'interaction dans logs/experiment_data.json
    """

    def __init__(self, name: str = "AuditorAgent", model_used: str = "gemini-2.5-flash"):
        self.name = name
        self.model_used = model_used
        self.llm = GeminiClient(model_name=model_used)

    def analyze_file(self, file_path: str) -> None:
        path = Path(file_path)

        # 1) TOOL : lancer pylint
        return_code, pylint_output = run_pylint_on_file(str(path))

        # 2) Construire le PROMPT (métier de l'agent)
        input_prompt = (
            "Tu es un expert Python.\n"
            "On te donne un rapport pylint sur un fichier de code.\n"
            "Ton rôle :\n"
            "le reecrire de façon concise en listant les points clés,et en donnant la note "
            f"{pylint_output}"
        )



        # 3) Appel LLM (client générique)
        output_response = self.llm.generate(input_prompt)

        print(f"📝 Résumé de l'Auditor pour {path.name} :\n{output_response}")

        # 4) LOG : obligatoire pour le TP (input_prompt + output_response).[file:2]
        log_experiment(
            agent_name=self.name,
            model_used=self.model_used,
            action=ActionType.ANALYSIS,  # l'agent lit et analyse le code.[file:2]
            details={
                "file_analyzed": str(path),
                "pylint_return_code": return_code,
                "input_prompt": input_prompt,      # texte exact envoyé au LLM.[file:2]
                "output_response": output_response,  # réponse brute du LLM.[file:2]
                "issues_found": None,  # tu pourras remplacer par un nombre plus tard
                "status": "SUCCESS" if return_code == 0 else "WARNING",
            },
           status="SUCCESS" if return_code == 0 else "FAILURE",
        )
