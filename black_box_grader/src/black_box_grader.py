import docker
import requests

client = docker.from_env()

IMAGE_NAME = "python:3.9-alpine"  # create custom linux with alpine to reduce size
TIME_LIMIT_REASON = "Time Limit Exceeded"
UNKNOWN_REASON = "Unknown Error"

def grade(testcases: list, base64Source: str):
    fileName = "temp.py"
    total_correct = 0
    results = []

    for testcase in testcases:
        command = f"touch {fileName} && echo `echo {base64Source} | base64 -d` > {fileName} && echo \"{testcase['input']}\" | python3 {fileName}"
        reason = "correct"

        # add time limit
        container = client.containers.run(
            image=IMAGE_NAME,
            command=f"sh -c '{command}'",
            detach=True,
            network_mode="none",
            nano_cpus=1 * 1000000000,
            mem_limit="128m",
            memswap_limit="256m",
            pids_limit=64,
            log_config={
            "config": {
                "mode": "non-blocking",
                "max-size": "50m",
                "max-file": "100"
            }}
        )

        chunk = b""
        try:
            output = container.wait(timeout=2) # in s
        except requests.exceptions.ConnectionError:
            container.remove(force=True)
            results.append(TIME_LIMIT_REASON)
            continue
        except Exception as e:
            container.remove(force=True)
            results.append(UNKNOWN_REASON)
            continue

        for line in container.logs(stream=True, follow=True):
            chunk += line

        if (output["StatusCode"] == 0):
            if (chunk.decode().rstrip() == testcase["output"]):
                total_correct += 1
            else:
                reason = "wrong answer"
        else:
            reason = chunk.decode()

        results.append(reason)
        container.remove(force=True)

    point = (total_correct / len(testcases)) * 100
    return point, results
