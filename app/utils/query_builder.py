import json

from sqlalchemy import select, and_, or_, not_, cast, Date, func

from app.constants.tags import Tags



BOOLEAN_FUNCTIONS = {
    'or': lambda *clauses: or_(*clauses),
    'and': lambda *clauses: and_(*clauses),
    'not': lambda clause: not_(clause),
}

class QueryBuilder:
    def __init__(self, db):
        self.db = db

    async def execute_query(self, model_class, json_input):
        async with self.db.get_sessionmaker() as session:
            input_data = json.loads(json_input)
            print(input_data)
            query = select(model_class)

            if "filters" in input_data:
                query = self.apply_filters(query, model_class, input_data["filters"])

            if "sort" in input_data:
                query = self.apply_sort(query, model_class, input_data["sort"])

            if "pagination" in input_data:
                query = self.apply_pagination(query, input_data["pagination"])
            print(query)

            results = await session.execute(query)
            results = results.scalars().all()

            return [result.to_dict() for result in results]

    def apply_filters(self, query, model_class, filter_spec):
        filters = self.build_filters(model_class, filter_spec)
        return query.filter(filters)

    def build_filters(self, model_class, filter_spec):
        if isinstance(filter_spec, dict):
            if 'field' in filter_spec and filter_spec['field'] == 'tag_id' and filter_spec['op'] == '==':
                return self.Filter(model_class, filter_spec).to_expression()
            elif any(key in filter_spec for key in BOOLEAN_FUNCTIONS):
                key = next(iter(filter_spec.keys()))
                return BOOLEAN_FUNCTIONS[key](*[self.build_filters(model_class, f) for f in filter_spec[key]])
            else:
                return self.Filter(model_class, filter_spec).to_expression()
        elif isinstance(filter_spec, list):
            return and_(*[self.build_filters(model_class, f) for f in filter_spec])
        else:
            raise ValueError("Invalid filter specification")

    def apply_sort(self, query, model_class, sort_spec):
        for sort in sort_spec:
            field = getattr(model_class, sort['field'])
            if sort['direction'] == 'asc':
                query = query.order_by(field.asc())
            elif sort['direction'] == 'desc':
                query = query.order_by(field.desc())
        return query

    def apply_pagination(self, query, pagination_spec):
        limit = pagination_spec.get("limit", 10)
        offset = pagination_spec.get("offset", 0)
        return query.limit(limit).offset(offset)

    class Filter:
        def __init__(self, model_class, filter_spec):
            self.model_class = model_class
            self.field = filter_spec['field']
            self.op = filter_spec.get('op', '==')
            self.value = filter_spec.get('value')

        def to_expression(self):
            field = getattr(self.model_class, self.field)
            if self.op == '==':
                if isinstance(self.value, Tags):
                    self.value = self.value.value
                return field == self.value
            elif self.op == '!=':
                if isinstance(self.value, Tags):
                    self.value = self.value.value
                return field != self.value
            elif self.op == 'like':
                return field.like(self.value)
            elif self.op == 'ilike':
                return field.ilike(self.value)
            elif self.op == 'is_null':
                return field.is_(None)
            elif self.op == 'is_not_null':
                return field.isnot(None)
            elif self.op == 'in':
                if isinstance(self.value, list) and all(isinstance(val, Tags) for val in self.value):
                    self.value = [val.value for val in self.value]
                return field.in_(self.value)
            elif self.op == 'not_in':
                if isinstance(self.value, list) and all(isinstance(val, Tags) for val in self.value):
                    self.value = [val.value for val in self.value]
                return field.not_in(self.value)
            else:
                raise ValueError(f"Unknown operator {self.op}")








