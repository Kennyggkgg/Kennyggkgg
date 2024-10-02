import os

class SelfModificationModule:
    def __init__(self, core_directory):
        self.core_directory = core_directory

    def modify_code(self, file_name, new_code):
        file_path = os.path.join(self.core_directory, file_name)
        with open(file_path, 'a') as file:
            file.write(f"\n# New code modification\n{new_code}")
        return f"Code added to {file_name} successfully."

    def shutdown(self):
        print("Shutting down the system now...")
        exit(0)