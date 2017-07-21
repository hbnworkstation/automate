# -*- coding: utf-8 -*-
# (c) 2015 Tuomas Airaksinen
#
# This file is part of automate-arduino.
#
# automate-arduino is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# automate-arduino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with automate-arduino.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from traits.api import CInt, Instance, CFloat, CBool, CStr, Int, Any
from automate.service import AbstractSystemService
from automate.statusobject import AbstractSensor


class AbstractArduinoSensor(AbstractSensor):

    """
        Abstract base class for Arduino sensors
    """

    user_editable = CBool(False)

    #: Arduino device number (specify, if more than 1 devices configured in ArduinoService)
    dev = CInt(0)

    #: Arduino pin number
    pin = CInt

    _arduino = Instance(AbstractSystemService, transient=True)

    def setup(self, *args, **kwargs):
        super(AbstractArduinoSensor, self).setup(*args, **kwargs)
        self._arduino = self.system.request_service('ArduinoService', self.dev)


class ArduinoAnalogSensor(AbstractArduinoSensor):

    """
        Float-valued sensor object for analog Arduino input pins
    """
    _status = CFloat

    def setup(self, *args, **kwargs):
        super(ArduinoAnalogSensor, self).setup(*args, **kwargs)
        self._arduino.subscribe_analog(self.pin, self)

    def cleanup(self):
        self._arduino.unsubscribe_analog(self.pin)


class ArduinoVirtualWireMessageSensor(AbstractArduinoSensor):

    """
        String valued sensor object for analog Arduino VirtualWire input 
    """ # TODO docstring

    _status = CStr

    def setup(self, *args, **kwargs):
        super(ArduinoVirtualWireMessageSensor, self).setup(*args, **kwargs)
        self._arduino.subscribe_virtualwire_messages(self)

    def cleanup(self):
        self._arduino.unsubscribe_virtual_messages(self)


class ArduinoVirtualWireAbstractSensor(AbstractArduinoSensor):

    """
        String valued sensor object for analog Arduino VirtualWire input 
    """ # TODO docstring

    virtual_pin = Int

    _status = Any

    def setup(self, *args, **kwargs):
        super(ArduinoVirtualWireAbstractSensor, self).setup(*args, **kwargs)
        self._arduino.subscribe_virtualwire_virtual_pin(self, self.virtual_pin)

    def cleanup(self):
        self._arduino.unsubscribe_virtualwire_virtual_pin(self.virtual_pin)

class ArduinoDigitalSensor(AbstractArduinoSensor):

    """
        Boolean-valued sensor object for digital Arduino input pins
    """

    _status = CBool

    def setup(self, *args, **kwargs):
        super(ArduinoDigitalSensor, self).setup(*args, **kwargs)
        self._arduino.subscribe_digital(self.pin, self)

    def cleanup(self):
        self._arduino.unsubscribe_digital(self.pin)
