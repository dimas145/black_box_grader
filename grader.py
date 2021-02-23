import docker
import os

client = docker.from_env()

IMAGE_NAME = "python:latest"  # create custom linux with alpine to reduce size
SANDBOX_TMP_DIR = "/workspace"


class Grader:
    def __init__(self, tmpPath, entryPoint):
        self.tmpPath = os.path.abspath(tmpPath)
        self.entryPoint = entryPoint
        self.input = "1"

    def grade(self):

        command = f"echo {self.input} | python3 {self.entryPoint}"

        output = client.containers.run(
            image=IMAGE_NAME,
            remove=True,
            command=f"sh -c '{command}'",
            read_only=True,
            network_mode="none",
            volumes={self.tmpPath: {"bind": SANDBOX_TMP_DIR, "mode": "ro"}},
            working_dir=os.path.join(SANDBOX_TMP_DIR, "src"),
            nano_cpus=1 * 1000000000,
            mem_limit="128m",
            memswap_limit="256m",
            pids_limit=64,
        )
        print(output)


grade = Grader("tmp", "main.py")
grade.grade()
