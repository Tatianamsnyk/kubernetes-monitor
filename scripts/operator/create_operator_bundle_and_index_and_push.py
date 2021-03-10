#! /usr/bin/python3

from sys import argv
from subprocess import call
from os import chdir, environ, getcwd
from shutil import copy


def createOperatorBundleAndIndexImagesAndPushToDockerHub(operator_path: str, operator_tag: str, dockerhub_user: str, dockerhub_password: str) -> None:
    current_path = getcwd()
    copy(current_path + "/" + "opm", operator_path + "/" + "opm")
    copy(current_path + "/" + "snyk-operator" + "/" + "bundle.Dockerfile",
         operator_path + "/" + "bundle.Dockerfile")
    copy(current_path + "/" + "snyk-operator" + "/" + "Makefile",
         operator_path + "/" + "Makefile")

    environ['VERSION'] = operator_tag
    call(["docker", "login", "--username=" + dockerhub_user,
          "--password=" + dockerhub_password])

    return_path = current_path
    chdir(operator_path)
    call(["make", "bundle-build"])
    operator_bundle_name_and_tag = "snyk/kubernetes-operator-bundle" + ":" + operator_tag
    call(["docker", "push", operator_bundle_name_and_tag])

    operator_index_name_and_tag = "snyk/kubernetes-operator-index" + ":" + operator_tag
    call([operator_path + "/" + "opm", "add", "-c", "docker", "--bundles",
          "snyk/kubernetes-operator-bundle" + ":" + operator_tag, "--tag", operator_index_name_and_tag])
    chdir(return_path)


if __name__ == '__main__':
    _, operator_path, operator_tag, dockerhub_user, dockerhub_password = argv
    createOperatorBundleAndIndexImagesAndPushToDockerHub(
        operator_path, operator_tag, dockerhub_user, dockerhub_password)
