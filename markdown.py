#!/usr/bin/env python3

import csv

import click
from jinja2 import Environment, FileSystemLoader


JINJA = Environment(
    loader=FileSystemLoader('templates'),
    trim_blocks=True)


@click.command()
@click.argument('source', type=click.Path(dir_okay=False, readable=True))
def main(source):
    """Convert a CSV book list to Markdown."""
    click.echo(f'Input: {source}')
    data = read_csv(source)
    for book in data:
        if book['Language'] == 'EN':
            book['Category'] = book.get('English Package Name', 'No Category')
        elif book['Language'] == 'DE':
            book['Category'] = book.get('German Package Name', 'No Category')
        else:
            book['Category'] = 'No Category'
    template = JINJA.get_template('books.md')
    content = template.render(books=data)
    output = source.replace('.csv', '.md')
    with open(output, 'w', encoding='UTF-8') as file:
        file.write(content)
    click.echo(f'Output: {output}')
    click.echo(f'Titles: {len(data)}')


def read_csv(path):
    """Read the CSV file as a list of dicts using column names as keys."""
    data = []
    first = True
    names = None
    with open(str(path), encoding='UTF-8', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if first:
                names = row
                first = False
            else:
                if len(row) != len(names):
                    raise Exception(f'Unexpected column count: {row}')
                data.append(dict(zip(names, row)))
    return data


if __name__ == '__main__':
    main()
