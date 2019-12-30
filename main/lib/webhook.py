from importlib import import_module


class Webhook():
    @classmethod
    def run(cls, event_type: str, payload: str) -> str:
        print('webhook_runner.' + event_type + " start.")
        module = import_module('main.lib.webhook_runner.' + event_type)
        Klass = getattr(module, 'Runner')
        runner = Klass(payload)
        result = runner.run()
        print('webhook_runner.' + event_type + " end.")

        return result
