import subprocess
import json
import sys
import re


def check_config(cmd_type: str, key: str, expected: str) -> None:
    """
    Executes a Hadoop command to verify if a specific configuration value matches the expected value.

    Args:
        cmd_type (str): The type of Hadoop command to execute (hdfs, hadoop, yarn).
        key (str): The configuration key to be verified (confKey).
        expected (str): The expected configuration value.
    """
    cmd = [cmd_type, "getconf", "-confKey", key]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to execute command while verifying {key}: {e.stderr}")
        return

    else:
        result = result.stdout.strip()
        if result == expected:
            print(f"PASS: {cmd} -> {result}")
        else:
            print(f"FAIL: {cmd} -> {result} (expected {expected})")


def verify_replication(expected_rep_factor: int = 2) -> None:
    """Creates a test file in HDFS and verifies its replication factor."""
    test_file_path: str = "/tmp/test_replication.txt"
    content: str = "verification"
    try:
        subprocess.run(
            ["hdfs", "dfs", "-put", "-f", "-", test_file_path],
            input=content,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to create test_file in HDFS: {e.stderr}")
        return

    try:
        result = subprocess.run(
            ["hdfs", "dfs", "-stat", "%r", test_file_path],
            capture_output=True,
            text=True,
            check=True,
        )
        rep_factor = result.stdout.strip()
        subprocess.run(
            ["hdfs", "dfs", "-rm", "-f", test_file_path],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to check replication factor: {e.stderr}")
        return

    if rep_factor == str(expected_rep_factor):
        print(f"PASS: Replication factor is {rep_factor}")
    else:
        print(
            f"FAIL: Replication factor is {rep_factor} (expected {expected_rep_factor})"
        )


def verify_yarn_resources() -> None:
    """Verify the total available memory for YARN"""
    print("\n RUN yarn node -list -showDetails ")
    try:
        result = subprocess.run(
            ["yarn", "node", "-list", "-showDetails"],
            capture_output=True,
            text=True,
            check=True,
        )
        query_result = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to query yarn resource manager {e.stderr}")

    else:
        print("Current Status:")
        print(query_result)


def run_test_mapreduce() -> None:
    """Run a simple MapReduce job and ensure it uses the YARN framework."""
    print("\n--- Running Test MapReduce Job on YARN ---")

    jar_path = "/opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar"
    cmd = ["hadoop", "jar", jar_path, "pi", "2", "10"]
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to run mapreduce job {e.stderr}")

    else:
        yarn_app_id = re.search(
            r"Submitted application (application_\d+_\d+)", process.stderr
        )
        if process.returncode == 0 and "Estimated value of Pi" in process.stdout:
            print("PASS: MapReduce job completed successfully.")
            if yarn_app_id:
                print(f"YARN Verification: Success (App ID: {yarn_app_id.group(1)})")
            else:
                print(
                    "WARNING: Job finished but YARN application ID not found in logs."
                )
        else:
            print("FAIL: MapReduce job failed.")
            print(f"Error Log:\n{process.stderr}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 verify_configs.py <config_json_file_path>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        config_data = json.load(f)

    for xml_file, settings in config_data.items():
        cmd = "hdfs"
        for key, expected in settings.items():
            check_config(cmd, key, str(expected))

    rep = config_data["hdfs-site.xml"].get("dfs.replication", "2")
    verify_replication(int(rep))
    verify_yarn_resources()
    run_test_mapreduce()
