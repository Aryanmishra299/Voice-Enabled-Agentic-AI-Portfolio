import os
import json


class LocalDataStoreService:

    def __init__(self):
        self.base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data-store"
        )

        print("\n" + "=" * 80)
        print("📂 DATA STORE INITIALIZATION")
        print("=" * 80)
        print(f"BASE PATH: {self.base_path}")
        print(f"PATH EXISTS: {os.path.exists(self.base_path)}")
        print("=" * 80 + "\n")

    def _read_json(self, file_name: str) -> dict:

        file_path = os.path.join(self.base_path, file_name)

        print(f"\n🔍 Reading JSON: {file_path}")

        try:
            if not os.path.exists(file_path):
                print(f"❌ FILE NOT FOUND: {file_path}")
                return {}

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(f"✅ FILE LOADED: {file_name}")
            print(f"🔑 ROOT KEYS: {list(data.keys())}")

            return data

        except Exception as e:
            print(f"❌ JSON LOAD ERROR: {file_name}")
            print(f"ERROR: {str(e)}")
            return {}

    def get_profile(self) -> dict:
        data = self._read_json("profile.json")
        return data.get("profile", {})

    def get_projects(self) -> list:
        data = self._read_json("projects.json")
        return data.get("projects", [])

    def get_experience_records(self) -> dict:
        return self._read_json("experience.json")

    def get_skills_catalog(self) -> dict:
        data = self._read_json("skills.json")
        return data.get("skills_catalog", {})


data_store_service = LocalDataStoreService()