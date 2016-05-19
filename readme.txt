Project to stop the home becoming slave to the wifi

Configuration

You'll want a settings file, the default name being homefi.conf, along the following lines:

[controller]
username = admin
password = admin
server = 1.2.3.4
api_version = v4

[evening]
block_groups: children

[morning]
unblock_groups: children

Then, you will want to set up a cron task to apply the different profiles, for instance:

# m h  dom mon dow   command
  0 7  *   *   *                   cd ~/homefi && ./homefi.py morning
  0 21 *   *   *                   cd ~/homefi && ./homefi.py evening

This will switch wifi off for the children in the evenings, and put it back on in the morning.
