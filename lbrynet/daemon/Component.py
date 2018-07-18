import logging
from twisted.internet import defer
from .ComponentManager import ComponentManager

log = logging.getLogger(__name__)


class ComponentType(type):
    def __new__(mcs, name, bases, newattrs):
        klass = type.__new__(mcs, name, bases, newattrs)
        if name != "Component":
            ComponentManager.default_component_classes[klass.component_name] = klass
        return klass


class Component(object, metaclass=ComponentType):
    """
    lbrynet-daemon component helper

    Inheriting classes will be automatically registered with the ComponentManager and must implement setup and stop
    methods
    """

    depends_on = []
    component_name = None

    def __init__(self, component_manager):
        self.component_manager = component_manager
        self._running = False

    @property
    def running(self):
        return self._running

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def component(self):
        raise NotImplementedError()

    @defer.inlineCallbacks
    def _setup(self):
        result = yield defer.maybeDeferred(self.start)
        self._running = True
        defer.returnValue(result)

    @defer.inlineCallbacks
    def _stop(self):
        result = yield defer.maybeDeferred(self.stop)
        self._running = False
        defer.returnValue(result)
