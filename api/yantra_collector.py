import json
from logic import YantraCollector

def handler(event, context):
    body = json.loads(event["body"])
    grid = body["grid"]
    strategy = body["strategy"]
    
    game = YantraCollector(grid)
    path = game.get_path(strategy)
    
    response = {
        "statusCode": 200,
        "body": json.dumps(path if path else [])
    }
    
    return response