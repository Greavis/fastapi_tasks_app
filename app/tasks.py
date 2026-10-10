import json
from pathlib import Path
from fastapi import HTTPException

DATA_FILE = Path(__file__).parent / "data.json"

class Tasks():
    def __init__(self):
        pass

    def status_validate(self, status):
        valid_status = ["open", "in_progress", "done"]
        if status not in valid_status:
            return False
        else:
            return True

    def priority_validate(self, priority):
        valid_priority = ["low", "medium", "high"]
        if priority not in valid_priority:
            return False
        else:
            return True
    
    def create_task(self, title, description, status, priority):
        if not self.status_validate(status):
            return {"status": "can be 'open', 'in_progress' or 'done'"}
        if not self.priority_validate(priority):
            return {"priority": "can be 'low', 'medium' or 'high'"}
        
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        last_task_pos = len(data["tasks"]) - 1
        task_id = data["tasks"][last_task_pos]["id"] + 1
        new_task = {
            "id": task_id,
            "title": title,
            "description": description,
            "status": status,
            "priority": priority
        }
        data['tasks'].append(new_task)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return new_task

    def get_tasks(self, status, priority, search, order, sort_by):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = [
            task for task in data["tasks"]
            if (search is None or search.lower() in task["title"].lower())
            and (status is None or task["status"] == status)
            and (priority is None or task["priority"] == priority)
        ]

        if sort_by and sort_by != "priority":
            tasks.sort(key=lambda task: task[sort_by].lower())

        if sort_by and sort_by == "priority":
            priority_order = {
                "high": 1,
                "medium": 2,
                "low": 3
            }
            tasks.sort(key=lambda task: priority_order[task[sort_by].lower()])
        
        if order == "desc":
            tasks.reverse()

        if not tasks:
            raise HTTPException(status_code=404, detail="Tasks Not Found")
        
        return tasks

    def get_task(self, task_id):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if task_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="task_id must be greater than 0"
            )
        for task in data["tasks"]:
            if task["id"] == task_id:
                return task
        raise HTTPException(status_code=404, detail="Tasks Not Found")

    def update_task(self, task_id, title, description, status, priority):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        task = None
        for item in data["tasks"]:
            if item["id"] == task_id:
                task = item
                break
            
        if task is None:
            raise HTTPException(status_code=404, detail="Tasks Not Found")

        new_task_data = {
            "id": task_id,
            "title": title if title is not None else task["title"],
            "description": description if description is not None else task["description"],
            "status": status if status is not None else task["status"],
            "priority": priority if priority is not None else task["priority"]
        }
        if new_task_data == {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "status": task["status"],
            "priority": task["priority"]
        }:
            return {"error": "same data"}
        

        if not self.status_validate(new_task_data["status"]):
            return {"status": "can be 'open', 'in_progress' or 'done'"}
        if not self.priority_validate(new_task_data["priority"]):
            return {"priority": "can be 'low', 'medium' or 'high'"}

        task.update(new_task_data)
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return new_task_data

    def delete_task(self, task_id):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for i, task in enumerate(data["tasks"]):
            if task["id"] == task_id:
                del data["tasks"][i]
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                return {"204": "No Content"}
        raise HTTPException(status_code=404, detail="Tasks Not Found")