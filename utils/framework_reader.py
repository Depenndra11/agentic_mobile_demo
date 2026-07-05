from pathlib import Path


class FrameworkReader:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parent.parent

        self.folders = [
            "pages",
            "utils"
        ]

        self.files = [
            "conftest.py"
        ]

    # -----------------------------------------
    # Read a single file
    # -----------------------------------------
    def read_file(self, file_path):

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

        except Exception:
            return ""

    # -----------------------------------------
    # Read all framework files
    # -----------------------------------------
    def get_framework(self):

        framework = []

        # Read folders
        for folder in self.folders:

            folder_path = self.project_root / folder

            if not folder_path.exists():
                continue
            skip_files = {
                "__init__.py",
                "framework_reader.py",
                "excel_reader.py",
                "llm.py",
                "logger.py",
            }

            for file in folder_path.rglob("*.py"):

                if file.name in skip_files:
                    continue

                framework.append(
                    f"""
            File:
            {file.name}

            Code:
            {self.read_file(file)}
            """
                )

        # Read root files
        for filename in self.files:

            file_path = self.project_root / filename

            if file_path.exists():

                framework.append(
                    f"""
                    File:
                    {filename}
                    
                    Code:
                    {self.read_file(file_path)}
                    """
                )

        return "\n\n".join(framework)


if __name__ == "__main__":

    reader = FrameworkReader()

    print(reader.get_framework())