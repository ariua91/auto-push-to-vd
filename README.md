# auto-push-to-vd
A script to check VF for "Assigned" tasks. If any exists, login and send to VD.

### Usage
1. Needs a VF PUBLIC API `client_id` & `client_secret` in secret_keys.py. 
   Also needs a VF COOKIE 'cookie', and random_task_id in secret_keys
2. Run via `python anomaly.py`

## Potential Bugs
 - Relies completely on the cookie refreshing everytime it is used. 
   Not sure if this is valid, we'll see. 