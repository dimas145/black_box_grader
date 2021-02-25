import docker
import os
import uuid
client = docker.from_env()

IMAGE_NAME = "python:latest"  # create custom linux with alpine to reduce size
SANDBOX_TMP_DIR = "/workspace"


class Grader:
    def __init__(self, tmpPath, entryPoint, testcases):
        self.tmpPath = os.path.abspath(tmpPath)
        self.entryPoint = entryPoint
        self.testcases = testcases
        self.container = None
        self.cid = str(uuid.uuid4()) # container id

    def grade(self):
        count = 0
        for testcase in self.testcases:

            command = f"echo {testcase['input']} | python3 {self.entryPoint}"
            command2 = "sleep 10"

            # add time limit
            self.container = client.containers.run(
                image=IMAGE_NAME,
                command=f"sh -c '{command}'",
                read_only=True,
                network_mode="none",
                volumes={self.tmpPath: {"bind": SANDBOX_TMP_DIR, "mode": "ro"}},
                working_dir=os.path.join(SANDBOX_TMP_DIR, "src"),
                nano_cpus=1 * 1000000000,
                mem_limit="128m",
                memswap_limit="256m",
                pids_limit=64,
                detach=True
            )
            for line in self.container.logs(stream=True, follow=True):
                print(line)
            output = self.container.wait(timeout=2) # in s
            print(output)
            print('removing container')
            self.container.remove()
