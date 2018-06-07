# ipx800-python

ipx800-python is a Python3 Library for controlling GCE-Electronics IPX800 V4 via its public API.

## Sample Usage

### Setting up IPX800

    # Setup IPX800 V4
    host = "yourhostname.lan"
    port = 80
    apiKey = "YourAPIKey"

    ipx = IPX800(host, port, apiKey)

### Setting up Relays

    # Setup Relays you want to control
    enabled_relays = [1, 2, 15]
    r_conf = IPXRelaysConfig(enabled_relays)
    ipx.configure_relays(r_conf)

### Controlling relays

    # Retrieve a specific relay in the list
    # here r15 is a instance of 'Relay' class nested in 'IPX800' class
    r15 = ipx.relays['R15']

    # We now create a instance of IPXRelay
    relay = IPXRelay(ipx, r15.number, r15.name)

    # Request relay state from the server
    relay.reload_state()

    # Turn on the relay (close it)
    relay.turn_on()

    print("Relay %d aka <%s> state is %d" % (relay.number, relay.name, relay.is_on))

    # Wait 2 seconds
    time.sleep(2)

    # Turn off the relay (open it)
    relay.turn_off()

    print("Relay %d aka <%s> state is %d" % (relay.number, relay.name, relay.is_on))

### Setting up PWM channels

    # Setup PWM Channels
    # /!\ Some XPWM functions are not accessible via json API
    # So we use CGI api that require username and password
    username = "username"
    password = "yourPassword"

    enabled_pwm_channels = [1, 2, 3, 4]
    pwm_conf = IPXPwmConfig(username, password, enabled_pwm_channels)
    ipx.configure_pwm(pwm_conf)

### Controlling PWM channels

    # Retrieve a specific PWM channel in the list
    # here pwm1 is a instance of 'PWM' class nested in 'IPX800' class
    pwm1 = ipx.pwm_channels['PWM1']

    # Instanciate an IPXPwmChannel
    ch1 = IPXPwmChannel(ipx, pwm1.number)

    # Request current power value of the PWM Channel
    ch1.reload_power()

    # Turn PWM Channel on at 100%
    ch1.turn_on(100)

    time.sleep(1)

    # Set power of the PWM channel to 30%
    ch1.turn_on(30)

    time.sleep(1)

    # Turn the PWM Channel off
    ch1.turn_off()

    # You can turn PWM channel on without power value
    # It will take the last value OR 100 if the last value was 0
    ch1.turn_on()

## Features

- [x] Control IPX800 relays and X8R extension
- [x] Control light brightness via XPWM extension module
- [ ] Control roller shutters via X4VR extension module
- [ ] Control pilot wire extension
- [ ] Request XHTL sensor values
- [ ] Request digital input values
- [ ] Request analog input value
- [ ] ... Control all other extensions modules

/!\ This code is still under development an test. This is my first Python code so I'm not sure doing everything right. Feel free to comment and contribure !