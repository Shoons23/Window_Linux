import queue
import threading
import time

class Robot:
    def __init__(self, robot_id):
        self.robot_id = robot_id
        self.is_idle = True # 유휴 상태
        self.current_task = None 
    
    def assign_task(self, task):
        self.is_idle = False
        self.current_task = task
        print(f"Robot {self.robot_id} assigned to task {task}")
    
    def complete_task(self):
        print(f"Robot {self.robot_id} completed task {self.current_task}")
        self.is_idle = True
        self.current_task = None

def worker(robot, task_queue):
    while not task_queue.empty():
        if robot.is_idle:
            try:
                task = task_queue.get_nowait()
                robot.assign_task(task)
                time.sleep(task['duration'])  # Simulate task duration
                robot.complete_task()
                task_queue.task_done()
            except queue.Empty:
                break

def dispatch_tasks(num_robots, tasks):
    robots = [Robot(robot_id) for robot_id in range(num_robots)]
    task_queue = queue.Queue()

    for task in tasks:
        task_queue.put(task)
    
    threads = []
    for robot in robots:
        t = threading.Thread(target=worker, args=(robot, task_queue))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    print("All tasks completed.")

# Example usage
tasks = [{'id': 1, 'duration': 2}, {'id': 2, 'duration': 3}, {'id': 3, 'duration': 1}]
num_robots = 2

dispatch_tasks(num_robots, tasks)
