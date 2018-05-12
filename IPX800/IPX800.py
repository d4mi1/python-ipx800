# -*- coding: utf-8 -*-
# @Author: Damien FERRERE
# @Date:   2018-05-06 20:44:51
# @Last Modified by:   Damien FERRERE
# @Last Modified time: 2018-05-12 10:02:56


import requests
import re
import datetime

import time

class IPX800:
  'IPX800 control class'

  host = ''
  port = ''
  api_key = ''
  base_url = ''

  relays = {}

  __last_request_dt = datetime.datetime.fromtimestamp(0)

  def __init__(self, host, port, api_key, enables_relays):
    self.host = host
    self.port = port
    self.api_key = api_key
    self.base_url = "http://"+host+":"+port+"/api/xdevices.json?key="+api_key

    for r in enables_relays:
      self.relays['R%d' % r] = IPXRelay(self, r, 0) # init enabled relays


  def set_relay_to(self, relay_no, is_on):
    ''' Remotely set the relay N° relay_no to is_on
        0 is Off (Relay opened)
        1 is On (Relays is closed)
    '''
    print ("Setting relay No %d to %d" % (relay_no, is_on))
    command = 'SetR'
    
    if not is_on:
      command = 'ClearR'
    
    command_url = self.base_url + '&%s=%d' % (command, relay_no)
    
    #print (command_url)
    r = requests.get(command_url)

    if r.status_code == 200:
      answer = r.json()
      #print (answer['status'])
      # Request relays state to update local relays state
      self.__request_relays_state()
      return True

    return False

  def update_relay(self, relay): 
    ''' Remotely update the specified 'relay' 
    '''
    self.set_relay_to(relay.number, relay.is_on)


  def __request_relays_state(self):
    ''' Requests all 56 relays of IPX800 and extensions, even not connected
        Then filter to match the enabled_relays list
    '''
    current_dt = datetime.datetime.now()

    # Prevent to poll IPX to many time
    if (current_dt - self.__last_request_dt).total_seconds() < 1.0:
      return

    self.__last_request_dt = datetime.datetime.now()
    command_url = self.base_url + '&Get=R'
    
    #print (command_url)
    r = requests.get(command_url)

    if r.status_code == 200:
      answer = r.json()

    for key, value in answer.items():
      if re.match(r'R\d{1,2}', key):
        if (key in self.relays):
          self.relays[key]._is_on = value


  def get_state_of_relay(self, relay_no):
    ''' Return the state of a specific relay 
        0 is Off (Relay is opened)
        1 is On (Relays is closed)
    '''
    self.__request_relays_state()
    return self.relays['R%d' % relay_no].is_on


class IPXRelay:
  
  number = 0
  __ipx = None
  
  def __init__(self, ipx, relayNo, currentRelayState):
    self.number = relayNo
    self._is_on = currentRelayState
    self.__ipx = ipx

  @property
  def is_on(self):
    return self._is_on

  def turn_on(self):
    self._is_on = 1
    self.__ipx.update_relay(self)

  def turn_off(self):
    self._is_on = 0
    self.__ipx.update_relay(self)

  def reload_state(self):
    self.state = self.__ipx.get_state_of_relay(self.number)