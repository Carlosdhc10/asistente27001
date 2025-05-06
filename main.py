import os
from interface.ui import launch_ui

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    launch_ui(server_name="localhost", server_port=port)
