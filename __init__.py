from DomsSoftStep2Controller import DomsSoftStep2Controller
import Logging


def create_instance(c_instance):
    c_instance.log_message("DomsSoftStep2ControllerLogginxyz::__creeateinstance")
    Logging.startlogging()
    return DomsSoftStep2Controller(c_instance)
