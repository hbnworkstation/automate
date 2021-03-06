Automate Components
===================

.. inheritance-diagram:: automate.program.Program
                         automate.program.DefaultProgram
                         automate.statusobject.StatusObject
                         automate.statusobject.AbstractSensor
                         automate.statusobject.AbstractActuator
                         automate.callable.AbstractCallable
                         automate.service.AbstractService
   :parts: 1

Automate system is built of the following components:

* **System** (derived by user from :class:`~automate.system.System`) binds all parts together into a single state machine
* **Services** (subclassed of :class:`~automate.service.AbstractService`) provide
  programming interfaces with user and devices that can be used by **SystemObjects**.
* **SystemObjects** (subclassed of :class:`~automate.systemobject.SystemObject` or :class:`~automate.program.ProgrammableSystemObject`):

  * **Sensors** (subclassed on :class:`~automate.statusobject.AbstractSensor`) are used as an interface to the (usually read-only)
    state of device or software.
  * **Actuators** (subclassed on :class:`~automate.statusobject.AbstractActuator`) are used as an interface to set/write the state of
    device or software.
  * **Programs** (subclassed on :class:`~automate.program.ProgrammableSystemObject`) define the logic between
    Sensors and Actuators.
    They are used to control statuses of Actuators, by rules that are programmed by using special
    **Callables** (subclasses of :class:`~automate.callable.AbstractCallable`) objects that depend on statuses of
    Sensors and other components.  Also Sensors and Actuators are often subclassed from
    :class:`~automate.program.ProgrammableSystemObject` so
    they also have similar features by themselves. Depending on the application, however, it might (or might not)
    improve readability if plain :class:`~automate.program.Program` component is used.

All Automate components are derived from :class:`~traits.has_traits.HasTraits`, provided by
Traits library, which provides automatic notification of attribute changes, which is used
extensively in Automate. Due to traits, all Automate components are configured by passing
attribute names as keyword arguments in object initialization (see for example attributes
:attr:`~automate.extensions.arduino.AbstractArduinoActuator.pin`
and
:attr:`~automate.extensions.arduino.AbstractArduinoActuator.dev` traits of
:class:`~automate.extensions.arduino.ArduinoDigitalActuator`
in the example below).

Automate system is written by subclassing :class:`~automate.system.System` and adding there desired
:class:`~automate.systemobject.SystemObject` as its attributes, such as in the following example::

  from automate import *
  class MySystem(System):
    mysensor = FloatSensor()
    myactuator = ArduinoDigitalActuator(pin=13, service=0)
    myprogram = Program()
    ...

After defining the system, it can be instantiated. There, services with their necessary arguments
can be explicitly defined as follows::

  mysys = MySystem(services=[WebService(http_port=8080), ArduinoService(device='/dev/ttyS0')])

Some services (those that have :attr:`~automate.service.AbstractService.autoload` atribute set to True)
do not need to be explicitly defined. For example,
:class:`~automate.extensions.arduino.arduino_service..ArduinoService` would be used automatically
loaded because of the usage of :class:`~automate.extensions.arduino.arduino_actuator.ArduinoDigitalActuator`,
with default settings (``device='/dev/ttyUSB0'``). Instantiating
System will launch IPython shell to access the system internals from the command line. This can be prevented, if
necessary, by defining keyword argument :attr:`~automate.system.System.exclude_services` as
``['TextUIService']``, which disables autoloading of
:class:`~automate.services.textui.TextUIService`. For further information about services, see :ref:`services`.
