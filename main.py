import argparse
import sys
import os
from dotenv import load_dotenv
from src.utils.logger import log_experiment
from pathlib import Path
from src.utils.agents.auditor import AuditorAgent


load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
   
    target_dir = Path(args.target_dir)
    python_files = list(target_dir.rglob("*.py"))
    if not python_files:
        print(f"❌ Aucun fichier .py trouvé dans {target_dir}")
        sys.exit(1)
    else:
        print(f"🔍 Fichiers .py trouvés : {[str(f) for f in python_files]}" )

    for file_to_analyze in python_files:
        print(f"🔎 Fichier analysé par l'Auditor : {file_to_analyze}")
        auditor = AuditorAgent()
        auditor.analyze_file(str(file_to_analyze))

    

    print("✅ MISSION_COMPLETE")


if __name__ == "__main__":
    main()