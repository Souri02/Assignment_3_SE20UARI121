class Process:
    def __init__(self, name, arrival_time, burst_time, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.waiting_time = 0  
        self.turnaround_time = 0  

# Define a list of processes
processes = [
    Process("Process1", 0, 24, 3),
    Process("Process2", 4, 3, 1),
    Process("Process3", 5, 3, 4),
    Process("Process4", 6, 12, 2),
]

def first_come_first_serve(processes):
    schedule = []  
    current_time = 0  

    processes.sort(key=lambda x: x.arrival_time)

    for process in processes:
        process.waiting_time = max(0, current_time - process.arrival_time)

        current_time += process.burst_time

        process.turnaround_time = process.waiting_time + process.burst_time

        schedule.append((process.name, current_time - process.burst_time))

    total_waiting_time = sum(process.waiting_time for process in processes)
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    average_waiting_time = total_waiting_time / len(processes)
    average_turnaround_time = total_turnaround_time / len(processes)

    return schedule, average_waiting_time, average_turnaround_time

def shortest_job_first(processes):
    if not processes:
        return [], 0, 0

    schedule = []  
    current_time = 0  

    processes_copy = processes.copy()

    waiting_times = []  
    turnaround_times = []  

    while processes_copy:
        eligible_processes = [process for process in processes_copy if process.arrival_time <= current_time]

        if not eligible_processes:
            current_time += 1
        else:
            shortest_burst_process = min(eligible_processes, key=lambda x: x.burst_time)

            waiting_time = max(0, current_time - shortest_burst_process.arrival_time)
            waiting_times.append(waiting_time)

            current_time += shortest_burst_process.burst_time

            turnaround_time = waiting_time + shortest_burst_process.burst_time
            turnaround_times.append(turnaround_time)

            schedule.append((shortest_burst_process.name, current_time - shortest_burst_process.burst_time))

            processes_copy.remove(shortest_burst_process)

    average_waiting_time = sum(waiting_times) / len(waiting_times)
    average_turnaround_time = sum(turnaround_times) / len(turnaround_times)

    return schedule, average_waiting_time, average_turnaround_time

def priority_scheduling(processes):
    if not processes:
        return [], 0, 0

    schedule = []  
    current_time = 0  

    processes_copy = processes.copy()

    waiting_times = []  
    turnaround_times = []  

    while processes_copy:
        eligible_processes = [process for process in processes_copy if process.arrival_time <= current_time]

        if not eligible_processes:
            current_time += 1
        else:
            highest_priority_process = min(eligible_processes, key=lambda x: x.priority)

            waiting_time = max(0, current_time - highest_priority_process.arrival_time)
            waiting_times.append(waiting_time)

            current_time += highest_priority_process.burst_time

            turnaround_time = waiting_time + highest_priority_process.burst_time
            turnaround_times.append(turnaround_time)

            schedule.append((highest_priority_process.name, current_time - highest_priority_process.burst_time))

            processes_copy.remove(highest_priority_process)

    average_waiting_time = sum(waiting_times) / len(waiting_times) if waiting_times else 0
    average_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0

    return schedule, average_waiting_time, average_turnaround_time

def round_robin_scheduling(processes, time_quantum=4):
    if not processes:
        return [], 0, 0

    schedule = []  
    current_time = 0  

    processes_copy = processes.copy()

    waiting_times = []  
    turnaround_times = []  

    while processes_copy:
        process = processes_copy.pop(0)

        if process.arrival_time <= current_time:
            waiting_time = max(0, current_time - process.arrival_time)
            waiting_times.append(waiting_time)

            if process.burst_time <= time_quantum:
                current_time += process.burst_time

                turnaround_time = waiting_time + process.burst_time
                turnaround_times.append(turnaround_time)

                schedule.append((process.name, current_time - process.burst_time))
            else:
                current_time += time_quantum
                process.burst_time -= time_quantum

                processes_copy.append(process)
        else:
            current_time += 1

    average_waiting_time = sum(waiting_times) / len(waiting_times) if waiting_times else 0
    average_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0

    return schedule, average_waiting_time, average_turnaround_time

# Call the scheduling functions for different algorithms
fcfs_schedule, fcfs_avg_waiting_time, fcfs_avg_turnaround_time = first_come_first_serve(processes)
sjf_schedule, sjf_avg_waiting_time, sjf_avg_turnaround_time = shortest_job_first(processes)
priority_schedule, priority_avg_waiting_time, priority_avg_turnaround_time = priority_scheduling(processes)
round_robin_schedule, round_robin_avg_waiting_time, round_robin_avg_turnaround_time = round_robin_scheduling(processes)

# Print average waiting and turnaround times for all algorithms
print(f"FCFS - Average Waiting Time: {fcfs_avg_waiting_time:.2f}, Average Turnaround Time: {fcfs_avg_turnaround_time:.2f}")
print(f"SJF - Average Waiting Time: {sjf_avg_waiting_time:.2f}, Average Turnaround Time: {sjf_avg_turnaround_time:.2f}")
print(f"Priority - Average Waiting Time: {priority_avg_waiting_time:.2f}, Average Turnaround Time: {priority_avg_turnaround_time:.2f}")
print(f"Round Robin - Average Waiting Time: {round_robin_avg_waiting_time:.2f}, Average Turnaround Time: {round_robin_avg_turnaround_time:.2f}")

# Determine the suitable algorithm based on average turnaround time and average waiting time
average_times = {
    "FCFS": (fcfs_avg_waiting_time, fcfs_avg_turnaround_time),
    "SJF": (sjf_avg_waiting_time, sjf_avg_turnaround_time),
    "Priority": (priority_avg_waiting_time, priority_avg_turnaround_time),
    "Round Robin": (round_robin_avg_waiting_time, round_robin_avg_turnaround_time)
}

suitable_algorithm = min(average_times, key=lambda x: (average_times[x][1], average_times[x][0]))
print(f"Suitable Algorithm: {suitable_algorithm}")
