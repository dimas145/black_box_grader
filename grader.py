import docker
import os
import uuid
import json
import requests

client = docker.from_env()

IMAGE_NAME = "python:latest"  # create custom linux with alpine to reduce size
SANDBOX_TMP_DIR = "/workspace"
TIME_LIMIT_REASON = "Time Limit Exceeded"

class Grader:
    def __init__(self, tmpPath, entryPoint, testcases):
        self.tmpPath = os.path.abspath(tmpPath)
        self.entryPoint = entryPoint
        self.testcases = testcases
        self.container = None
        self.cid = str(uuid.uuid4()) # container id

    def grade(self):
        count = 0
        total_correct = 0
        result = []
        for testcase in self.testcases:
            count += 1
            command = f"echo {testcase['input']} | python3 {self.entryPoint}"
            command2 = "sleep 60"
            reason = "success"
            isCorrect = True
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
                detach=True,
                log_config={
                'config': {
                    'mode': 'non-blocking',
                    'max-size': '1m',
                    'max-file': '2'
                }}
            )

            chunk = b''
            try:
                output = self.container.wait(timeout=2) # in s
            except requests.exceptions.ConnectionError:
                self.container.remove(force=True)
                result.append({
                    'isCorrect': False,
                    'reason': TIME_LIMIT_REASON
                })
                continue

            for line in self.container.logs(stream=True, follow=True):
                chunk += line

            if(output['StatusCode'] == 0):
                if (chunk.decode().rstrip() == testcase['output']):
                    total_correct += 1
                else:
                    reason = "wrong answer"
                    isCorrect = False
            else:
                reason = chunk.decode()
            
            
            result.append({
                'isCorrect': isCorrect,
                'reason': reason
            })
            
            self.container.remove(force=True)
        
        point = 0
        if(count > 0):
            point = (total_correct / count) * 100
        
        response = {
            'total': point,
            'detail': result
        }

        # print(json.dumps(response))
        return json.dumps(response)


testcase_json = "{\"testcases\": [{\"input\": \"1\",\"output\": \"True\"},{\"input\": \"2\",\"output\": \"False\"}]}"

grade = Grader(tmpPath="tmp", entryPoint='test.py', testcases=json.loads(testcase_json)['testcases'])
grade.grade()