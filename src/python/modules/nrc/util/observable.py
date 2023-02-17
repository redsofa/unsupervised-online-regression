from collections import defaultdict
from abc import ABCMeta, abstractmethod

# Observer pattern bits. Adapted from this reference : https://www.youtube.com/watch?v=KAwOtYk7QSE


# Manages the list of observers
# Notifies them of state changes
class IObservable(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def subscribe(event_type, fn):
        # The subscribe method
        pass

    @staticmethod
    @abstractmethod
    def unsubscribe(event_type, fn):
        # The unsubscribe method
        pass

    @staticmethod
    @abstractmethod
    def trigger(event_type, fn):
        # The trigger method
        pass

# Observer interface
class IObserver(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def register_event_handlers():
        # Receive notification
        pass

class BaseObservableImpl(IObservable):
    def __init__(self):
        #default values of the dictionary will be a list
        self._observers = defaultdict(list)

    def subscribe(self, event_type, fn):
        self._observers[event_type].append(fn)

    def unsubscribe(self, event_type, fn):
        for f in self._observers[event_type]:
            if f == fn :
                self._observers[event_type].remove(f)

    def trigger(self, event_type, *args, **kwargs):
        for fn in self._observers[event_type]:
            fn(event_type, *args, **kwargs)

'''
# Usage example :

class Observer(IObserver):
    def __init__(self, observable):
        self._observable = observable
        self.register_event_handlers()

    def register_event_handlers(self):
       self._observable.subscribe('on_change_this', self.on_change_this)

    def on_change_this(self, *args, **kwargs):
        print('in OBSERVER_1 on_change_this')

subject = BaseObservableImpl()
observer_1 = Observer(subject)
subject.trigger('on_change_this', 'bla', this='a', that='kk')
'''


if __name__ == '__main__':
    pass
