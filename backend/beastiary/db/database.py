class Database:
    def __init__(self) -> None:
        self.data = {}

    def __repr__(self) -> str:
        return f"Database({' '.join([f'{table}:{len(self.data[table])}'  for table in self.data])})"

    def create_table(self, name):
        if name in self.data:
            raise ValueError(f"Table {name} already exists!")
        self.data[name] = []

    def query(self, table_name: str, *, id: int = None, skip=0, limit=100, **kwargs):
        if not id is None:
            try:
                row = self.data[table_name][id]
                return row
            except IndexError:
                return None
        return [
            row
            for row in self.data[table_name]
            if row is not None and all(row[k] == v for k, v in kwargs.items())
        ][skip : skip + limit]

    def add(self, table_name: str, obj):
        self.data[table_name].append(obj)

    def add_all(self, table_name, objs: list):
        self.data[table_name].extend(objs)

    def remove(self, table_name: str, *, id: int):
        try:
            row = self.data[table_name][id]
        except IndexError:
            return None
        self.data[table_name][id] = None
        return row

    def remove_where(self, table_name: str, **kwargs):
        removed = []
        for index, row in enumerate(self.data[table_name]):
            if row is not None and all(row[k] == v for k, v in kwargs.items()):
                removed.append(row)
                self.data[table_name][index] = None
        return removed
