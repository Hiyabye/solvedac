# scripts/update-data.py - Fetches problems from solved.ac API and saves them to JSON files.

import json
import os
import requests
import sys
from tqdm import tqdm

"""
Fetch problems from solved.ac API for a given range.
Returns a list of problems in JSON format.
"""
def fetch_problems(start, end):
  ids = ",".join(map(str, range(start, end+1)))
  response = requests.get("https://solved.ac/api/v3/problem/lookup", params={"problemIds": ids})

  if response.status_code != requests.codes.ok:
    print(f"Failed to get problems {start}-{end}")
    print(f"Status code: {response.status_code}")
    return []
  
  return json.loads(response.content.decode("utf-8"))

"""
Save a single problem to a JSON file based on its problemId.
"""
def save_problem(problem):
  problem_id = problem["problemId"]
  directory = os.path.join("data", str(problem_id // 10000) + str(problem_id % 10000 // 1000) + "xxx")
  
  if not os.path.exists(directory):
    os.makedirs(directory)

  file_path = os.path.join(directory, f"{problem_id}.json")
  with open(file_path, "w") as file:
    json.dump(problem, file, indent=2)

def main(start, end):
  problems = []

  print(f"Getting problems {start}-{end}...")
  for i in tqdm(range(start, end+1, 100)):
    problems.extend(fetch_problems(i, min(i+99, end)))
  
  print("Saving files...")
  for problem in tqdm(problems):
    save_problem(problem)

if __name__ == "__main__":
  start = int(sys.argv[1])
  end = int(sys.argv[2])
  main(start, end)
