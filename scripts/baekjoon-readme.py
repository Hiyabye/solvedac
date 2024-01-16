# scripts/baekjoon-readme.py - Update README.md automatically.

from datetime import datetime, timezone, timedelta
import glob
import json
import requests
from tqdm import tqdm
import os

"""
Returns number of solved problems from solved.ac API.
"""
def get_solved_count(handle):
  response = requests.get("https://solved.ac/api/v3/user/show", params={"handle": handle})

  if response.status_code != requests.codes.ok:
    print("Failed to get user info")
    print(f"Status code: {response.status_code}")
    exit(1)

  return int(json.loads(response.content.decode("utf-8"))["solvedCount"])

"""
Fetch solved problems from solved.ac API for a given page.
Returns a list of problems in JSON format.
"""
def get_problems(handle, page):
  response = requests.get("https://solved.ac/api/v3/search/problem", params={"query": f"solved_by:{handle}", "direction": "asc", "page": page, "sort": "id"})

  if response.status_code != requests.codes.ok:
    print(f"Failed to get solved problems for page {page}")
    print(f"Status code: {response.status_code}")
    exit(1)

  return json.loads(response.content.decode("utf-8"))

"""
Returns problem URL from problem ID.
"""
def get_problem_url(id):
  return f"https://www.acmicpc.net/problem/{id}"

"""
Returns problem title with special characters escaped.
"""
def get_problem_title(title):
  title = title.replace("|", "\\|") # 17203: ∑|ΔEasyMAX|
  return title

"""
Returns problem tier from problem level.
"""
def get_problem_tier(level):
  tier = {
    0: "Unrated",
    1: "Bronze V", 2: "Bronze IV", 3: "Bronze III", 4: "Bronze II", 5: "Bronze I",
    6: "Silver V", 7: "Silver IV", 8: "Silver III", 9: "Silver II", 10: "Silver I",
    11: "Gold V", 12: "Gold IV", 13: "Gold III", 14: "Gold II", 15: "Gold I",
    16: "Platinum V", 17: "Platinum IV", 18: "Platinum III", 19: "Platinum II", 20: "Platinum I",
    21: "Diamond V", 22: "Diamond IV", 23: "Diamond III", 24: "Diamond II", 25: "Diamond I",
    26: "Ruby V", 27: "Ruby IV", 28: "Ruby III", 29: "Ruby II", 30: "Ruby I"
  }
  return f'<img src="https://static.solved.ac/tier_small/{level}.svg" alt="{tier[level]}" width="24" height="24">'

"""
Find and returns solution path from problem ID.
"""
def get_solution_path(id):
  if (id < 10000):
    id = f"0{id}"
  dir = f"{str(id)[:2]}xxx"

  ext = {
    ".ads": "Ada",
    ".bas": "FreeBASIC",
    ".c"  : "C99",
    ".cpp": "C++17",
    ".gs" : "Golfscript",
    ".py" : "Python 3",
    ".txt": "Text",
    ".vb" : "Visual Basic"
  }

  files = glob.glob(f"baekjoon/{dir}/{id}.*")
  if len(files) == 0:
    print(f"Failed to find solution for problem {id}")
    exit(1)
  solution = ""
  for file in files:
    file = file[9:] # Remove "baekjoon/"
    solution += f"[{ext[file[file.rfind('.'):]]}]({file}) "
  return solution

"""
Generates README.md header.
"""
def get_header(handle):
  header = "# Baekjoon\n\n"
  header += "백준 알고리즘 문제 풀이 기록\n\n"
  header += f"[![Solved.ac 프로필](http://mazassumnida.wtf/api/v2/generate_badge?boj={handle})](https://solved.ac/{handle})\n\n"
  header += "문제들은 주로 C/C++로 해결하였으며, 가끔 Python으로도 풀었습니다. 목록은 다음과 같습니다:\n\n"
  header += "마지막으로 업데이트: "
  header += datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
  header += " (KST)\n\n"
  return header

"""
Generates README.md table.
"""
def get_table(problems):
  table = "| # | 제목 | 레벨 | 솔루션 |\n"
  table += "|:---:|:---:|:---:|:---:|\n"

  print("Generating table...")
  for (id, title, level) in tqdm(problems):
    url = get_problem_url(id)
    title = get_problem_title(title)
    tier = get_problem_tier(level)
    path = get_solution_path(id)
    table += f"| [{id}]({url}) | {title} | {tier} | {path}|\n"
  return table

if __name__ == "__main__":
  solved_count = get_solved_count("hiyabye")
  pages = (solved_count - 1) // 50 + 1
  problems = []

  print(f"Getting problems from {pages} pages...")
  for page in tqdm(range(1, pages+1)):
    solved = get_problems("hiyabye", page)
    for problem in solved["items"]:
      problems.append((int(problem["problemId"]), problem["titleKo"], int(problem["level"])))
  
  if not os.path.exists("output"):
    os.makedirs("output")

  with open("output/README.md", "w") as f:
    f.write(get_header("hiyabye") + get_table(problems))
  print("README.md updated without errors")
