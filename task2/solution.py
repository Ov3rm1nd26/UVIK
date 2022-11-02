import datetime


import typer
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, delete_todo, insert_todo, complete_todo, count_completed, uncompleted_todo


console = Console()
app = typer.Typer()


@app.command(short_help='add an item(s): add --items "item1" --items "item2"')
def add(items: Optional[List[str]] = typer.Option(None)):
    all_items = ', '.join(items)
    typer.echo(f'adding {all_items} task')
    for item in items:
        todo = Todo(item)
        insert_todo(todo)
    show()


@app.command(short_help='remove an item(s): remove --positions 1 --positions 2')
def remove(positions: Optional[List[int]] = typer.Option(None)):
    typer.echo(f'deleting position(s) {positions}')
    counter = 1
    for position in positions:
        if counter == 1:
            delete_todo(position-1)
            counter += 1
        else:
            delete_todo(position - counter)
            counter += 1
    show()


@app.command(short_help='mark item as done')
def mark_done(position: int):
    typer.echo(f'mark position {position} as done')
    complete_todo(position - 1)
    show()


@app.command(short_help='mark item as uncompleted')
def mark_uncompleted(position: int):
    typer.echo(f'mark position {position} as uncompleted')
    uncompleted_todo(position - 1)
    show()


@app.command(short_help='show an items')
def show():
    tasks = get_all_todos()
    number_of_done = count_completed()
    console.print(f"{datetime.datetime.now().replace(microsecond=0)} you've completed {number_of_done[0][0]} tasks!")

    table = Table(show_header=True, header_style='bold white')
    table.add_column('№', style='bold white', width=6)
    table.add_column('Todo', style='bold white', min_width=20)
    table.add_column('Done', min_width=12, justify='right')

    for number, task in enumerate(tasks, start=1):
        is_done = '[green]Yes[/green]' if task.status == 2 else '[red]No[/red]'
        table.add_row(str(number), task.task, is_done)
    console.print(table)


if __name__ == '__main__':
    app()
