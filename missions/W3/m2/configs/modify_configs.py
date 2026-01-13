import os
import json
import shutil
import xml.etree.ElementTree as ET
import subprocess
import sys


def modify_xml(file_path: str, updates: dict[str, str]) -> bool:
    """
    Reads a Hadoop XML configuration file to update or add specific property values.

    Args:
        file_path (str): The full path of the XML file to be modified.
        updates (dict[str, str]): A dictionary containing pairs of property names and their values to update.

    Returns:
        bool: True if the update is successful, False if the file does not exist.
    """
    if not os.path.exists(file_path):
        print(f"Error: {file_path} doesn't exist.")
        return False

    backup_path: str = file_path + ".bak"
    shutil.copy2(file_path, backup_path)
    print(f"Backing up {os.path.basename(file_path)}...")

    tree = ET.parse(file_path)
    if not tree:
        print(f"Error: Can't parse {file_path}")
        return False

    root: ET.Element = tree.getroot()

    for name, value in updates.items():
        found: bool = False
        for prop in root.findall("property"):
            name_node = prop.find("name")
            if name_node is not None and name_node.text == name:
                value_node = prop.find("value")
                if value_node is not None:
                    value_node.text = str(value)
                found = True
                break

        if not found:
            new_prop: ET.Element = ET.SubElement(root, "property")
            ET.SubElement(new_prop, "name").text = name
            ET.SubElement(new_prop, "value").text = str(value)

    tree.write(file_path, encoding="utf-8", xml_declaration=True)
    print(f"Modifying {os.path.basename(file_path)}...")
    return True


def restart_services() -> None:
    commands = [
        ("Stopping YARN", ["stop-yarn.sh"]),
        ("Stopping Hadoop DFS", ["stop-dfs.sh"]),
        ("Starting Hadoop DFS", ["start-dfs.sh"]),
        ("Starting YARN", ["start-yarn.sh"]),
    ]

    for action, cmd in commands:
        print(f"{action}...")
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            error_details = e.stderr.strip()

            print(f"\n[ERROR] {action} failed!")
            print(f"- Exit Status: {e.returncode}")
            print(f"- Error Detail: {error_details}")
            return

    print("PASS: Configuration changes applied and services restarted.")

def distribute_to_workers(conf_dir: str, xml_files: list[str]) -> None:
    workers_file_path = os.path.join(conf_dir, 'workers')
    if not os.path.exists(workers_file_path):
        print(f"Error: {workers_file_path} doesn't exist")
        return

    with open(workers_file_path, 'r', encoding='utf-8') as f:
        worker_names = [line.strip() for line in f if line.strip()]
        
    for worker in worker_names:
        for xml_file in xml_files:
            src_path = os.path.join(conf_dir, xml_file)
            dest_path = f"{worker}:{conf_dir}/"
            try:
                subprocess.run(["scp", src_path, f"{worker}:{conf_dir}"], capture_output=True, check=True)
            except:
                print(f"Error: scp to {worker} not completed.")
            
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 modify_configs.py <config_json_file_path> [hadoop_config_dir_absolute_path]")
        sys.exit(1)

    json_path = sys.argv[1]
    if len(sys.argv) >= 3:
        conf_dir = sys.argv[2]
    else:
        conf_dir = "/opt/hadoop/etc/hadoop"

    if not os.path.exists(json_path):
        print(f"Can't find Json file: {json_path}")
        sys.exit(1)

    with open(json_path, "r") as f:
        config_data: dict[str, dict[str, str]] = json.load(f)

    modified_files = []
    for xml_file, updates in config_data.items():
        modify_xml(xml_file, updates)
        modified_files.append(xml_file)

    distribute_to_workers(conf_dir, modified_files)

    restart_services()
