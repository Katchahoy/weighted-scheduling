"""HTTP request handler accepting a list of contracts and returning the optimal schedule."""

import json
from jsonschema import validate
from aiohttp.web import Request, Response
from optimizer.optimizer import Contract, calculate_optimal_schedule

contracts_schema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'maxLength':64
        },
        'start': {
            'type': 'integer'
        },
        'duration': {
            'type': 'integer'
        },
        'price': {
            'type': 'integer'
        }
    }
}

def validate_json(data):
    """Validates that the JSON array can be mapped to a list of Contract objects."""
    for contract in data:
        validate(instance = contract, schema = contracts_schema)

def as_contract(item: dict) -> Contract:
    """Creates a Contract object from a dictionary with similar fields."""
    return Contract(item['name'], item['start'], item['duration'], item['price'])

def parse_contracts(text: str) -> list[Contract]:
    """Converts a JSON text input tu a list of Contract objects."""
    return json.loads(text, object_hook = as_contract)

def to_json(obj) -> str:
    """Convert any object to a JSON representation of its fields as a dictionary."""
    return json.dumps(obj, default = lambda o: o.__dict__)

async def handle_optimize_request(request: Request) -> Response:
    """
    Handles an HTTP request with a number of contracts as payload
    and returns the Schedule yielding the highest income.
    """
    request_body = await request.text()
    try:
        contracts = parse_contracts(request_body)
    except Exception:
        return Response(status = 400)

    optimal_schedule = calculate_optimal_schedule(contracts)

    return Response(
        status = 200,
        headers = {'Content-Type': 'application/json'},
        text = to_json(optimal_schedule)
    )
