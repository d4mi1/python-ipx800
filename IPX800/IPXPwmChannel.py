# -*- coding: utf-8 -*-
# @Author: Damien FERRERE
# @Date:   2018-05-22 21:13:38
# @Last Modified by:   Damien FERRERE
# @Last Modified time: 2018-05-27 22:52:10

class IPXPwmConfig:
  'IPX800 PWM Extension configuration class'
  # IPX800 Json api do not allow to command PWM extension
  # So we need user login an password to control it via cgi api
  username = ''
  password = ''
  enabled_pwm_channels = [] # List PWM channels user want to control

  def __init__(self, username, password, enabled_pwm_channels):
    self.username = username
    self.password = password

    self.enabled_pwm_channels = enabled_pwm_channels


class IPXPwmChannel:
  number = 0
  _power = 0
  _ipx = None

  def __init__(self, ipx, channel_no):
    self.number = channel_no
    self._ipx = ipx

  def set_to(self, power):
    self._power = power
    self._ipx.set_pwm_channel(self.number, self._power)

  def reload_power(self):
    self._power = self._ipx.get_value_of_pwm_channel(self.number)

  @property
  def power(self):
    return self._power

  @property
  def is_on(self):
    if self.power > 0:
      return True
    else:
      return False

  def turn_on(self):
    self.set_to(100)

  def turn_off(self):
    self.set_to(0)
