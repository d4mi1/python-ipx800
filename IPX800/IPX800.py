# -*- coding: utf-8 -*-
# @Author: Damien FERRERE
# @Date:   2018-05-06 20:44:51
# @Last Modified by:   Damien FERRERE
# @Last Modified time: 2018-05-28 20:47:08


import requests
import re
import datetime
import time

from requests_xml import XMLSession

from IPX800.IPXRelay import IPXRelay
from IPX800.IPXRelay import IPXRelaysConfig

from IPX800.IPXPwmChannel import IPXPwmChannel
from IPX800.IPXPwmChannel import IPXPwmConfig

class IPX800:
  'IPX800 V4 control class'

  _host = ''
  _port = ''

  _json_api_url = ''
  _names_xml_url = ''
  _cgi_api_url = None
  
  _relays_config = None
  _relays_min_polling_time = 1 # seconds

  _pwm_config = None
  _pwm_min_polling_time = 2 # seconds

  # minimum seconds before polling again 
  _polling_delays = {'relays': 1, 'pwm': 2}
  
  relays = None
  pwm_channels = None

  def __init__(self, host, port, api_key):

    self._host = host
    self._port = port
    
    base_url = "http://"+host+":"+port

    self._json_api_url = base_url+"/api/xdevices.json?key="+api_key
    self._names_xml_url = base_url + '/global.xml'

    d0 = datetime.datetime.fromtimestamp(0)
    self._last_polling_dt = {'relays': d0, 'pwm': d0}

    
  def configure_relays(self, relays_config):
    self._relays_config = relays_config
    self.relays = {}

    for r in relays_config.enabled_relays:
      self.relays['R%d' % r] = IPXRelay(self, r, 0) # init enabled relays


  def configure_pwm(self, pwm_config):
    self._pwm_config = pwm_config
    self.pwm_channels = {}

    for p in pwm_config.enabled_pwm_channels:
      self.pwm_channels['PWM%d' % p] = IPXPwmChannel(self, p) # init enabled pwm channels

    self._cgi_api_url = "http://"+self._pwm_config.username+":"+self._pwm_config.password+"@"
    self._cgi_api_url += self._host+":"+self._port+"/user/api.cgi"



  ############################################
  # RELAYS MANAGEMENT
  ############################################

  def set_relay_to(self, relay_no, is_on):
    ''' Remotely set the relay N° relay_no to is_on
        0 is Off (Relay opened)
        1 is On (Relays is closed)
    '''
    if self._relays_config == None: 
      return False

    command = 'SetR'
    
    if not is_on:
      command = 'ClearR'
    
    command_url = self._json_api_url + '&%s=%d' % (command, relay_no)
    
    r = requests.get(command_url)

    if r.status_code == 200:
      # Request relays state to update local relays state
      self._request_relays_state()
      return True

    return False

  def update_relay(self, relay): 
    ''' Remotely update the specified 'relay' 
    '''
    if self._relays_config == None: 
      return False

    self.set_relay_to(relay.number, relay.is_on)


  def _request_relays_state(self):
    ''' Requests all 56 relays of IPX800 and extensions, even not connected
        Then filter to match the enabled_relays list
    '''
    if self._relays_config == None: 
      return False

    current_dt = datetime.datetime.now()

    # Prevent to poll IPX to many time
    if (current_dt - self._last_polling_dt['relays']).total_seconds() < self._polling_delays['relays']:
      return True

    self._last_polling_dt['relays'] = current_dt

    command_url = self._json_api_url + '&Get=R'
    
    r = requests.get(command_url)

    if r.status_code == 200:
      answer = r.json()

      for key, value in answer.items():
        if re.match(r'R\d{1,2}', key):
          if (key in self.relays):
            self.relays[key]._is_on = value

      return True

    return False

  def _request_relays_names(self):
    ''' Requests all 56 relays custom names configured in IPX800 UI '''

    if self._relays_config == None: 
      return False

    session = XMLSession()
    res = session.get(self._names_xml_url)

    if res.status_code == 200:
      for r in self._relays_config.enabled_relays:
        relay_name = res.xml.xpath('//response/output%d' % r, first=True).text
        self.relays['R%d' % r].name = relay_name

      self._relays_config.names_retrieved = True
    


  def get_state_of_relay(self, relay_no):
    ''' Return the state of a specific relay 
        0 is Off (Relay is opened)
        1 is On (Relays is closed)
    '''

    if self._relays_config == None: 
      return False

    self._request_relays_state()

    if self._relays_config.names_retrieved == False: 
      self._request_relays_names()

    return self.relays['R%d' % relay_no].is_on


  ############################################
  # PWM LIGHTS MANAGEMENT
  ############################################

  def set_pwm_channel(self, channel_no, power):
    ''' Remotely set the light of the PWM extension N° channel_no to power
        - power from 0 to 100
        - channel_no 1 to 12 for the extension 1 & 13 to 24 for the extension 2

        http://IPX800_V4/user/api.cgi?SetPWM=12&PWMValue=0
    '''

    if self._pwm_config == None: 
      return False

    command_url = self._cgi_api_url + '?SetPWM=%d&PWMValue=%d' % (channel_no, power)
    r = requests.get(command_url)

    if r.status_code == 200:
      self.pwm_channels['PWM%d' % channel_no]._power = power
      return True

    return False

  def _request_pwm_channels(self):
    ''' Request the power of all 24 PWM channels event not connected 
        and update their values

        http://IPX800_V4/api/xdevices.json?key=key&Get=XPWM|1-24
    '''

    if self._pwm_config == None: 
      return False

    current_dt = datetime.datetime.now()

    # Prevent to poll IPX to many time
    if (current_dt - self._last_polling_dt['pwm']).total_seconds() < self._polling_delays['pwm']:
      return True

    self._last_polling_dt['pwm'] = current_dt

    command_url = self._json_api_url + '&Get=XPWM|1-24'
    
    r = requests.get(command_url)

    if r.status_code == 200:
      answer = r.json()

      for key, value in answer.items():
        if re.match(r'PWM\d{1,2}', key):
          if (key in self.pwm_channels):
            self.pwm_channels[key]._power = value

    return True

  def get_value_of_pwm_channel(self, channel_no):
    ''' Return the value of a specific pwm channel 
        From 0 to 100
    '''

    if self._pwm_config == None: 
      return False

    self._request_pwm_channels()

    return self.pwm_channels['PWM%d' % channel_no]._power
