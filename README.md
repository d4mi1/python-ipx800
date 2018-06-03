# ipx800-python

ipx800-python is a Python3 Library for controlling GCE-Electronics IPX800 V4 via its public API.

## Usage

    # Setup IPX800 V4
    host = "yourhostname.lan"
    port = 80
    apiKey = "YourAPIKey"

    # Setup Relays
    enabled_relays = [1,2,3,56]
    r_conf = IPXRelaysConfig(enabled_relays)
    ipx.configure_relays(r_conf)

    # Setup PWM Channels
    # /!\ Some XPWM functions are not accessible via json API
    # So we use CGI api that require username and password
    username = "username"
    password = "yourPassword"

    enabled_pwm_channels = [1,2,3,4]
    pwm_conf = IPXPwmConfig(username, password, enabled_pwm_channels)
    ipx.configure_pwm(pwm_conf)

## Features to implement

- [x] Control IPX800 relays and X8R extension
- [x] Control light brightness via XPWM extension module
- [ ] Control roller shutters via X4VR extension module
- [ ] Control pilot wire extension
- [ ] Request XHTL sensor values
- [ ] Request digital input values
- [ ] Request analog input value
- [ ] ... Control all other extensions modules

/!\ This code is still under development an test. This is my first Python code so I'm not sure doing everything right. Feel free to comment and contribure !