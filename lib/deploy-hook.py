"""
Author: Ali Hajimirza (ali@alihm.net)
"""
#!/usr/bin/env python
import os
import sys
import argparse
import shutil
import stat 

post_receive_template = """#!/bin/sh
DEPLOY_DIR='{abs_path}'
GIT_WORK_TREE=$DEPLOY_DIR git checkout -f master
cd $DEPLOY_DIR; npm install
bower install
grunt build
forever stop {app_path} || true
{env_vars}forever start {app_path}
"""

GIT_DEPLOY_NAME = 'deploy'
APP_PATH = os.path.join('$DEPLOY_DIR','dist', 'server','app.js')
ENV_VARS = ''

parser = argparse.ArgumentParser(description='Sets up directory for git hooks deployment')
parser.add_argument('directory', type=None, help='Name of the Node Application')
args = parser.parse_args()

try:
    # Check to see if the directory exists
    abs_path = os.path.abspath(args.directory)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)
    else:
        sys.stderr.write('Directory "{}" exists. Would you like to replace it? [y/n]'.format(abs_path))
        if (raw_input('').lower() == 'y'):
            shutil.rmtree(abs_path)
        else:
            sys.stderr.write('\nTerminating...\n')

    # Making the git hook
    deploy_dir = os.path.join(abs_path, GIT_DEPLOY_NAME)
    os.makedirs(deploy_dir)
    os.system('cd {}; git init --bare'.format(deploy_dir))
    post_receive_path = os.path.join(deploy_dir, 'hooks', 'post-receive')
    # Gathering information for the post-receive file
    mode_var = raw_input('Enter execution mode (Default production): ')
    env_vars = raw_input('Enter optional environmental variables (Example PORT=8080): ')
    app_path = raw_input('Enter server main script (Default {}): '.format(APP_PATH))
    if mode_var != '':
        ENV_VARS = "NODE_ENV='{}' ".format(mode_var)
    else:
        ENV_VARS = "NODE_ENV='production' "
    if env_vars != '':
        ENV_VARS += ' '.join(env_vars.split()) + ' '
    if app_path != '':
        APP_PATH = os.path.join('$DEPLOY_DIR' , app_path)

    # Writing the post-receive file
    with open(post_receive_path, 'wb') as post_recv_file:
        post_recv_file.write(post_receive_template.format(abs_path=abs_path, app_path=APP_PATH, env_vars=ENV_VARS))

except KeyboardInterrupt:
    sys.stdout.write('\nTerminating...\n')
    sys.exit(-1)
# Make post receive file an executable
st = os.stat(post_receive_path)
os.chmod(post_receive_path, st.st_mode | stat.S_IEXEC)
sys.stdout.write('Successfully created your githook at {}\n'.format(post_receive_path))
