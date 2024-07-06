from datetime import datetime

import pytest

from app.constants.event_tags import EventTags
from app.database.models.event import Event


def test_filter_service_eq(filter_service_factory):
    filter_spec = {"field": "location", "op": "==", "value": "EventLocation"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.location == "EventLocation")

def test_filter_service_neq(filter_service_factory):
    filter_spec = {"field": "location", "op": "!=", "value": "EventLocation"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.location != "EventLocation")

def test_filter_service_gt(filter_service_factory):
    filter_spec = {"field": "date", "op": ">", "value": "2024-01-01"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.date > datetime.fromisoformat("2024-01-01"))

def test_filter_service_gte(filter_service_factory):
    filter_spec = {"field": "date", "op": ">=", "value": "2024-01-01"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.date >= datetime.fromisoformat("2024-01-01"))

def test_filter_service_lt(filter_service_factory):
    filter_spec = {"field": "date", "op": "<", "value": "2024-01-01"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.date < datetime.fromisoformat("2024-01-01"))

def test_filter_service_lte(filter_service_factory):
    filter_spec = {"field": "date", "op": "<=", "value": "2024-01-01"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.date <= datetime.fromisoformat("2024-01-01"))

def test_filter_service_like(filter_service_factory):
    filter_spec = {"field": "description", "op": "like", "value": "%Event%"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.description.like("%Event%"))

def test_filter_service_ilike(filter_service_factory):
    filter_spec = {"field": "description", "op": "ilike", "value": "%event%"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.description.ilike("%event%"))

def test_filter_service_is_null(filter_service_factory):
    filter_spec = {"field": "description", "op": "is_null"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.description.is_(None))

def test_filter_service_is_not_null(filter_service_factory):
    filter_spec = {"field": "description", "op": "is_not_null"}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.description.isnot(None))

def test_filter_service_in(filter_service_factory):
    filter_spec = {"field": "tag_id", "op": "in", "value": [EventTags.CONCERT, EventTags.CONCERT]}
    filter_service = filter_service_factory(filter_spec)
    expression = filter_service.to_expression()
    assert str(expression) == str(Event.tag_id.in_([EventTags.CONCERT.value, EventTags.CONCERT.value]))

def test_filter_service_invalid_op(filter_service_factory):
    filter_spec = {"field": "location", "op": "invalid_op", "value": "EventLocation"}
    filter_service = filter_service_factory(filter_spec)
    with pytest.raises(ValueError, match="Unknown operator invalid_op"):
        filter_service.to_expression()
