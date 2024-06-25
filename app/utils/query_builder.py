from datetime import datetime

from sqlalchemy import select, and_, or_, cast
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.dialects.postgresql import DATE

from app.utils.filter_service import FilterService
from app.constants.types import OrmExpressions
from app.database.models.event import Event
from asyncio import *

class QueryBuilder:
    def __init__(self, db):
        self.db = db
        self.model_class = Event

    def execute_query(self, input_data: dict):
        query = (
            select(self.model_class)
            .options(selectinload(self.model_class.tag))
            .options(selectinload(self.model_class.organizer))
            .options(joinedload(self.model_class.feedbacks))
        )

        if "filters" in input_data:
            query = self.apply_filters(query, input_data["filters"])

        if "sort" in input_data:
            query = self.apply_sort(query, input_data["sort"])

        if "pagination" in input_data:
            query = self.apply_pagination(query, input_data["pagination"])

        return query

    def apply_filters(self, query, filter_spec):
        filters = self.build_filters(filter_spec)
        return query.filter(filters)

    def build_filters(self, filter_spec):
        if isinstance(filter_spec, dict):
            if "or" in filter_spec:
                or_filters = [self.build_filters(f) for f in filter_spec["or"]]
                return or_(*or_filters)
            elif "and" in filter_spec:
                and_filters = [self.build_filters(f) for f in filter_spec["and"]]
                return and_(*and_filters)
            elif (
                    filter_spec["field"] == "date"
                    and filter_spec["op"] in ("==", ">", "<", ">=", "<=")
            ):
                date_value = datetime.fromisoformat(filter_spec["value"])
                return self.model_class.date.cast(DATE) == cast(date_value, DATE)
            elif (
                    "field" in filter_spec
                    and filter_spec["field"] == "tag_id"
                    and filter_spec["op"] == "=="
            ):
                return FilterService(filter_spec).to_expression()
            elif any(key in filter_spec for key in OrmExpressions.BOOLEAN_FUNCTIONS.value):
                key = next(iter(filter_spec.keys()))
                return OrmExpressions.BOOLEAN_FUNCTIONS.value[key](
                    *[self.build_filters(f) for f in filter_spec[key]]
                )
            else:
                return FilterService(filter_spec).to_expression()
        elif isinstance(filter_spec, list):
            return and_(*[self.build_filters(f) for f in filter_spec])
        else:
            raise ValueError("Invalid filter specification")

    def apply_sort(self, query, sort_spec):
        for sort in sort_spec:
            field = getattr(self.model_class, sort["field"])
            if sort["direction"] == "asc":
                query = query.order_by(field.asc())
            elif sort["direction"] == "desc":
                query = query.order_by(field.desc())
        return query

    def apply_pagination(self, query, pagination_spec):
        limit = pagination_spec.get("limit", 10)
        offset = pagination_spec.get("offset", 0)
        return query.limit(limit).offset(offset)
