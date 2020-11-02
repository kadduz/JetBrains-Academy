from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def main_menu():
    menu = ["\n1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Missed tasks",
            "5) Add task", "6) Delete task", "0) Exit"]
    for elem in menu:
        print(elem)


def main():
    main_menu()
    while (choice := input()) != '0':
        if choice == '1':
            todays_tasks()
        elif choice == '2':
            week_tasks()
        elif choice == '3':
            all_tasks()
        elif choice == '4':
            missed_tasks()
        elif choice == '5':
            add_task()
        elif choice == '6':
            delete_task()
        else:
            print("\nChoice not allowed")
        main_menu()
    print("\nBye!")


def todays_tasks():
    today = datetime.today()
    print(f"\nToday {today.strftime('%d %b')}:")
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if rows:
        for i, row in enumerate(rows):
            print(f"{1 + i}. {row}")
    else:
        print("Nothing to do!")


def week_tasks():
    today = datetime.today()
    num_of_day = 0
    while num_of_day < 7:
        date_to_show = today + timedelta(days=num_of_day)
        print(f"\n{date_to_show.strftime('%A')} {date_to_show.strftime('%d %b')}:")
        rows = session.query(Table).filter(Table.deadline == date_to_show.date()).all()
        if rows:
            for i, row in enumerate(rows):
                print(f"{1 + i}. {row}")
        else:
            print("Nothing to do!")
        num_of_day += 1


def all_tasks():
    print("\nAll tasks: ")
    if not show_all_tasks():
        print("Nothing to do!")


def show_all_tasks():
    ids_task = {}
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        for i, row in enumerate(rows):
            dt = row.deadline.strftime('%d %b').lstrip("0").replace(" 0", " ")
            print(f"{1 + i}. {row}. {dt}")
            ids_task[1 + i] = row.id
    return ids_task


def missed_tasks():
    today = datetime.today()
    print("\nMissed tasks:")
    rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
    if rows:
        for i, row in enumerate(rows):
            dt = row.deadline.strftime('%d %b').lstrip("0").replace(" 0", " ")
            print(f"{1 + i}. {row}. {dt}")
    else:
        print("Nothing is missed!")


def add_task():
    print("\nEnter task")
    inp_task = input()
    print("Enter deadline")
    year, month, day = map(int, input().split('-'))
    new_row = Table(task=inp_task,
                    deadline=datetime(year, month, day))
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def delete_task():
    print("\nChoose the number of the task you want to delete:")
    ids_task = show_all_tasks()
    if ids_task:
        task_number = int(input())
        task_table_id = ids_task.get(task_number, None)
        if task_table_id:
            session.query(Table).filter(Table.id == task_table_id).delete()
            session.commit()
            print("The task has been deleted!")
        else:
            print("Task not found!")
    else:
        print("Nothing to delete!")


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
if __name__ == "__main__":
    main()
