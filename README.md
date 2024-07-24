# *\*pours syrup*\*
Using a Muse EEG headset to identify and classify the user EEG data related to 'focusing really hard on pancakes', which will cause the pancakes to explode. 

That's right, you're gonna __blow up pancakes with mind__. *Ma fuckin pancakes*

## Modeled after this meme
https://knowyourmeme.com/memes/blows-up-pancakes-with-mind




# Troubleshooting

## SER_PORT_ERROR = 3

It is most likely that the program doesn't have the permissions configured to open the serial port.
You may run it as sudo or add your user to the group `Gid` listed in `stat <such_a_serial_port>`.

If `stat <such_a_serial_port>` isn't working, it's most likely that your computer does not realize that there is a bluetooth device. If you are using a BLED112 adapter, please unplug and plug it back in.
