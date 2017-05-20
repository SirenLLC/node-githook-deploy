# ~~Node Githook Deployment~~ (Obsolete)

This project makes git hooks for deployment to a remote server. It generates a target folder with git configuration and upon newly pushed data it will run the commands `npm install`, `bower install` and `grunt build` as well as restarting the node server run by forever.

You can specify the `NODE_ENV` and other desired environmental variables such as `PORT` and different API keys.

## Usage

### Install

You only need to clone this repository on your remote machine.
``` bash
git clone https://github.com/Ali92hm/node-githook-deploy.git
```

### Execution

#### Remote
Run the following command on your server
```bash
python deploy-hook.py [app-name]
```
For example you can run
```bash
python deploy-hook.py /var/www/my-app

```
Then you will be asked a series of question such as `NODE_ENV`, other optional environmental variables and the relative path to your applications main script.


#### Your machine

To add a remote to a git repository navigate to the repository and run the following command
```bash
git remote add [remote-name] [username]@[remote-address]:[path-to-remote-folder]

```
For example you can run
```bash
git remote add deploy-ec2 ubuntu@ec2_address:/var/www/my-app

```

Run the following command to push to this repository from your machine
```bash
git push [remote-name] master

```
This command will push your changes to the remote server, download the newly added npm and bower modules, build the distribution version using grunt and restart the node application run by forever.

## Dependencies
* [Python2.7](https://www.python.org/download/releases/2.7/)
* [Git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [npm](https://www.npmjs.com)
* [bower](https://github.com/bower/bower)
* [grunt](http://gruntjs.com)
* [Forever](https://github.com/foreverjs/forever.git)

## Structure
	node-githook-deploy
	├── LICENSE-MIT
	├── README.md
	└── lib
		└── deploy-hook.py		- Generator script

##[Potential Bugs](https://github.com/Ali92hm/node-githook-deploy/issues)
* This script might not work under the Windows operating system.

## [To do](https://github.com/Ali92hm/node-githook-deploy/milestones)
* Test on windows.
* Make an npm module and put on npm

## License
[MIT license](http://opensource.org/licenses/MIT)
