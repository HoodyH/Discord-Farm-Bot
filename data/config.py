import json

with open('config.json', 'r') as file:
    _data = json.load(file)

# users ids where messages will be analysed
ALLOWED_IDS = _data.get('allowed_id', [])
LOG_CHANNEL = _data.get('log_channel')

# the main
_trainer = _data.get('trainer')
TRAINER_ID = _trainer.get('id')
TRAINER_TOKEN = _trainer.get('token')
TRAINER_ACTIONS = _trainer.get('actions', {})
