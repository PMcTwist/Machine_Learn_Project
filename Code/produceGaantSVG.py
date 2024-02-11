import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def create_gantt_chart(tasks):
    tasks.sort(key=lambda x: datetime.strptime(x['start_date'], '%Y-%m-%d'))
    tasks.reverse()

    fig, ax = plt.subplots(figsize=(10, len(tasks)))

    start_dates = [datetime.strptime(task['start_date'], '%Y-%m-%d') for task in tasks]
    end_dates = [datetime.strptime(task['end_date'], '%Y-%m-%d') for task in tasks]

    ax.xaxis_date()

    for i, task in enumerate(tasks):
        start_date = datetime.strptime(task['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(task['end_date'], '%Y-%m-%d')

        ax.barh(i, end_date - start_date, left=start_date, color='lightblue', edgecolor='black')
        ax.text(start_date, i, task['task'], va='center', ha='right', fontsize=8)

    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([])  # Remove default y-axis labels

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=90)
    plt.grid(axis='x')

    plt.tight_layout()

    plt.savefig('TimeLine.svg', format='svg', bbox_inches='tight')

    plt.show()

# Example usage
tasks_data = [
    {'task': 'Procrastinate', 'start_date': '2024-01-12', 'end_date': '2024-01-29'},
    {'task': 'Research', 'start_date': '2024-01-30', 'end_date': '2024-02-02'},
    {'task': 'Dig up Data', 'start_date': '2024-02-01', 'end_date': '2024-02-21'},
    {'task': 'Build Presentation', 'start_date': '2024-02-05', 'end_date': '2024-02-14'},
    {'task': 'Formulate Approach', 'start_date': '2024-02-05', 'end_date': '2024-02-07'},
    {'task': 'Build Gaant', 'start_date': '2024-02-05', 'end_date': '2024-02-07'},
    {'task': 'Present Proposal', 'start_date': '2024-02-15', 'end_date': '2024-02-15'},
    {'task': 'Build Demo Models', 'start_date': '2024-02-16', 'end_date': '2024-03-06'},
    {'task': 'Normalize final dataset', 'start_date': '2024-03-01', 'end_date': '2024-03-06'},
    {'task': 'Fine Tune Output', 'start_date': '2024-03-07', 'end_date': '2024-03-14'},
    {'task': 'Write Rough Draft', 'start_date': '2024-03-15', 'end_date': '2024-03-22'},
    {'task': 'Write Final Report', 'start_date': '2024-03-25', 'end_date': '2024-03-29'},
    {'task': 'Submit Project', 'start_date': '2024-04-01', 'end_date': '2024-04-01'},
]

create_gantt_chart(tasks_data)