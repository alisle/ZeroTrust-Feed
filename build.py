from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
#use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("pypi:pybuilder_docker")

name="zerotrust-feed"
default_task="publish"


@init
def initialize(project):
    project.depends_on("OTXv2")
    project.depends_on("Boto3")
    project.depends_on("aws")
    project.set_property("docker_package_image_maintainer", "Alex Lisle <alex.lisle@gmai.com>")
