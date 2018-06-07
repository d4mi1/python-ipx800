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
  power = 0
  _is_on = False
  _ipx = None

  def __init__(self, ipx, channel_no):
    self.number = channel_no
    self._ipx = ipx

  def reload_power(self):
    p = self._ipx.get_value_of_pwm_channel(self.number)

    if p > 0:
      self._is_on = True
      self.power = p
    else:
      self._is_on = False
    # else we do not set power too keep last on power value

  @property
  def is_on(self):
      return self._is_on

  def turn_on(self, power=-1):
    self._is_on = True
    
    if power == -1: # used last power value
      if self.power == 0:
        self.power = 100
    else:
      self.power = power
    
    self._ipx.set_pwm_channel(self.number, self.power)

  def turn_off(self):
    self._is_on = False
    self._ipx.set_pwm_channel(self.number, 0)
