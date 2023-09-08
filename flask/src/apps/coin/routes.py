from apps.coin import blueprint
from apps.config import Config
from apps.coin.coin_executor import coin_executor_instance

@blueprint.route("/")
def route_default():
    return "coin generate page"


@blueprint.route("/start")
def run_background_script():
    return coin_executor_instance.start_background_script()

@blueprint.route("/stop")
def stop_background_script():
    return coin_executor_instance.stop_background_script()