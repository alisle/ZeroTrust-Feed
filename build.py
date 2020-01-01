from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("pypi:pybuilder_docker")

name="zerotrust-feed"
default_task="publish"


@init
def initialize(project):
	project.build_depends_on('OTXv2')
