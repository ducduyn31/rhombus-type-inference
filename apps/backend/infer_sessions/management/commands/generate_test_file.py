import random

from django.core.management.base import BaseCommand, CommandError
import os
from faker import Faker
import pandas as pd

f = Faker()
f_cn = Faker("zh_CN")


class Command(BaseCommand):
    help = 'Generate test csv files'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the file to generate')
        parser.add_argument('rows', type=int, help='Number of rows to generate')
        parser.add_argument('cols', type=int, help='Number of columns to generate')

    def handle(self, *args, **kwargs):
        file_name = kwargs['name']
        rows = kwargs['rows']
        columns = kwargs['cols']

        if os.path.exists(file_name):
            raise CommandError(f'File {file_name} already exists')

        generator_options = {
            "id": [
                lambda n: [f.random_number(digits=5, fix_len=True) for _ in range(n)],
                lambda n: [f.random_number(digits=10, fix_len=True) for _ in range(n)],
            ],
            "name": [
                lambda n: [f.name() for _ in range(n)]
            ],
            "non_standard_date": [
                lambda n: [f.date_between(start_date="-30y", end_date="today").strftime("%d-%m-%Y") for _ in
                           range(n)],
                lambda n: [f.date_between(start_date="-30y", end_date="today").strftime("%m-%d-%Y") for _ in
                           range(n)],
                lambda n: [f.date_between(start_date="-30y", end_date="today").strftime("%Y-%m-%d") for _ in
                           range(n)],
                lambda n: [f.random_element(
                    elements=(
                        f.date_between(start_date="-30y", end_date="today").strftime("%d-%m-%Y"),
                        f.date_between(start_date="-30y", end_date="today").strftime("%m-%d-%Y"),
                        f.date_between(start_date="-30y", end_date="today").strftime("%Y-%m-%d"),
                        f.date_between(start_date="-30y", end_date="today").strftime("%d/%m/%d"),
                        f.date_between(start_date="-30y", end_date="today").strftime("%m/%d/%Y"),
                    )
                ) for _ in range(n)]
            ],
            "email": [
                lambda n: [f.email() for _ in range(n)]
            ],
            "mixed_names_with_nulls": [
                lambda n: [f.random_element(elements=(None, f.name())) for _ in range(n)]
            ],
            "mixed_dates_with_nulls": [
                lambda n: [f.random_element(
                    elements=(None, f.date_between(start_date="-30y", end_date="today").strftime("%d-%m-%Y"))) for _ in
                    range(n)],
                lambda n: [f.random_element(
                    elements=(None, f.date_between(start_date="-30y", end_date="today").strftime("%m-%d-%Y"))) for _ in
                    range(n)],
                lambda n: [f.random_element(
                    elements=(None, f.date_between(start_date="-30y", end_date="today").strftime("%Y-%m-%d"))) for _ in
                    range(n)],
            ],
            "very_large_number": [
                lambda n: [f.random_number(digits=20) for _ in range(n)],
            ],
            "category": [
                lambda n: [f.random_element(elements=("A", "B", "C", "D", None)) for _ in range(n)]
            ],
            "boolean": [
                lambda n: [f.boolean() for _ in range(n)],
                lambda n: [f.random_element(elements=(True, False, "YES", "NO", None)) for _ in range(n)],
                lambda n: [f.random_element(elements=(True, False, "Y", "N", None)) for _ in range(n)],
            ],
            "small_floats": [
                lambda n: [random.random() for _ in range(n)]
            ],
            "sparsed_columns": [
                lambda n: [f.word() if random.random() > 0.5 else None for _ in range(n)],
            ],
            "complex": [
                lambda n: [complex(random.random(), random.random()) for _ in range(n)]
            ],
            "mixed_numeric": [
                lambda n: [random.choice([f.random_number(digits=3), f.word()]) for _ in range(n)]
            ],
            "utf8": [
                lambda n: [f_cn.name() for _ in range(n)]
            ],
            "mixed_missing_values": [
                lambda n: [f.random_element(
                    elements=(None, "missing", "Missing", "Not found", f.word())
                ) for _ in range(n)]
            ]
        }

        flatten_options = [(key, item) for key, sublist in generator_options.items() for item in sublist]

        picked_options = random.choices(flatten_options, k=columns)

        data = {
            f"{key}_{i}": generator(rows) for i, (key, generator) in enumerate(picked_options)
        }

        df = pd.DataFrame(data)
        df.to_csv(f"assets/{file_name}", index=False)

        self.stdout.write(self.style.SUCCESS(f"File {file_name} generated successfully"))
