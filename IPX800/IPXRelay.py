# -*- coding: utf-8 -*-
# @Author: Damien FERRERE
# @Date:   2018-05-22 21:14:37
# @Last Modified by:   Damien FERRERE
# @Last Modified time: 2018-05-22 21:16:10

class IPXRelaysConfig:
  'IPX800 Relays configuration class'
  
  enabled_relays = [] # List of relays user want to control
  names_retrieved = False # indicate whether or not names have been retrieveds

  def __init__(self, enabled_relays):
    self.enabled_relays = enabled_relays



class IPXRelay:
  
  number = 0
  name = ''
  _ipx = None
  
  def __init__(self, ipx, relay_no, current_relay_state):
    self.number = relay_no
    self._is_on = current_relay_state
    self._ipx = ipx

  @property
  def is_on(self):
    return self._is_on

  def turn_on(self):
    self._is_on = 1
    self._ipx.update_relay(self)

  def turn_off(self):
    self._is_on = 0
    self._ipx.update_relay(self)

  def reload_state(self):
    self.state = self._ipx.get_state_of_relay(self.number)

