#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, ConfigParser, logging
from unifi.controller import Controller

settings = ConfigParser.SafeConfigParser()

def get_members(controller, grp_list):
    """ Return a list of group members """
    group_ids = tuple(d['_id'] for d in controller.get_user_groups() if d['name'] in grp_list.split())
    return [u for u in controller.get_users() if u.get('usergroup_id', '') in group_ids]

def block_groups(controller, grps):
    """ Block the specified groups """
    members = [m for m in get_members(controller, grps) if m.get('blocked') == False]
    for m in members:
        logging.info("Blocking client: {}".format(m.get('name', m.get('hostname'))))
        controller.block_client(m['mac'])
    

def unblock_groups(controller, grps):
    """ Unblock the specified groups """
    members = [m for m in get_members(controller, grps) if m.get('blocked') == True]
    for m in members:
        logging.info("Unblocking client: {}".format(m.get('name', m.get('hostname'))))
        controller.unblock_client(m['mac'])

action_dict = {"block_groups": block_groups,
               "unblock_groups": unblock_groups}

def do_work(controller, settings, args):
    """ Main entry point for the heavy lifting """
    for key, val in settings.items(args.scene):
        if key in action_dict:
            action_dict[key](controller, val)
        else: 
            logging.info("Ignoring unrecognised action: {}".format(key))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "HomeFi main controller")
    parser.add_argument('scene', type=str, help="Scene to apply")
    parser.add_argument('--settings', type=str, default="homefi.conf", help="Main settings file")
    parser.add_argument('-l', '--log_level', required=False, default='INFO')
    args = parser.parse_args()

    # Set up logging
    level = logging.getLevelName(args.log_level)
    logging.getLogger().setLevel(level)
    
    # Pick up the settings
    settings.read(args.settings)

    # Connect to the controller
    ctl_settings = {k: v for k, v in settings.items('controller')}
    server, api_version, username, password = tuple(ctl_settings.get(k, None) for k in ('server', 'api_version', 'username', 'password'))
    controller = Controller(server, username, password, version=api_version)

    do_work(controller, settings, args)

