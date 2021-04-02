import json

with open('config.json', 'r') as file:
    _data = json.load(file)


class Account:
    """
    Obj that rappresents the main user
    """
    def __init__(self, data):
        self.token: str = data.get('token')
        self.id: int = data.get('id')
        self.username: int = data.get('username')
        self.routine_raw: list = data.get('routine', [])
        self.actions_raw: list = data.get('actions', [])


class Configs:

    def __init__(self, config_raw):
        _trainer = config_raw.get('trainer')
        self.trainer: Account = Account(_trainer)

        self.global_actions: list = config_raw.get('global_actions', [])
        self.allowed_ids: list = config_raw.get('allowed_ids', [])
        self.target_id = config_raw.get('target', [])
        self.log_channel = config_raw.get('log_channel', [])

        self.allowed_ids.append(self.trainer.id)
        self.allowed_ids.append(self.target_id)


configs = Configs(_data)
