#! /usr/bin/python3

"""Set up a local OpenShift environment.

Does the following steps:
- build an Operator image and push to Docker Hub
- package an Operator bundle and its index and push to Docker Hub

PREREQUISITES:
The following environment variables:
- DOCKERHUB_USER (to push the Operator image)
- DOCKERHUB_PASSWORD

The following tools:
- make
- docker
"""

from os import environ
from hashlib import sha1
from datetime import datetime
from shutil import rmtree
from subprocess import call
from create_operator_and_push import createOperatorAndPushToDockerHub
from create_operator_bundle_and_index_and_push import createOperatorBundleAndIndexImagesAndPushToDockerHub
from package_operator_bundle import createOperatorBundleFromTemplate
from download_operator_sdk import downloadOperatorSdk
from download_operator_package_manager import downloadOperatorPackageManager

if __name__ == '__main__':
    random_digest = sha1(str(datetime.now()).encode("utf-8")).hexdigest()
    operator_version = "0.0.1-" + random_digest

    try:
        new_monitor_tag = environ['KUBERNETES_MONITOR_IMAGE_TAG']
    except:
        print("Missing environment variable KUBERNETES_MONITOR_IMAGE_TAG")
        print("Building kubernetes-monitor image and pushing to DockerHub")
        new_monitor_tag = operator_version
        monitor_name_and_tag = "snyk/kubernetes-monitor:" + new_monitor_tag
        call(["docker", "build", "-t", monitor_name_and_tag, "."])
        call(["docker", "push", monitor_name_and_tag])

    print("Downloading Operator SDK")
    downloadOperatorSdk()
    print("Downloading Operator Package Manager")
    downloadOperatorPackageManager()

    print("Creating Operator image and pushing to Docker Hub")
    dockerhub_user = environ['DOCKERHUB_USER']
    dockerhub_password = environ['DOCKERHUB_PASSWORD']
    createOperatorAndPushToDockerHub(
        operator_version, new_monitor_tag, dockerhub_user, dockerhub_password)

    new_version = new_operator_tag = operator_version

    print("Creating Operator bundle")
    operator_path = createOperatorBundleFromTemplate(
        operator_version, new_operator_tag, new_monitor_tag)
    print("Creating and pushing Operator bundle and index images")
    createOperatorBundleAndIndexImagesAndPushToDockerHub(
        operator_path, operator_version, dockerhub_user, dockerhub_password)
    print("Operator version " + operator_version +
          " and its related files have been pushed to Docker Hub")

    rmtree(operator_path)
