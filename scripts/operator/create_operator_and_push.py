#! /usr/bin/python3

from sys import argv
from create_operator import createOperatorAndBuildOperatorImage
from subprocess import call


def createOperatorAndPushToDockerHub(operator_tag: str, monitor_tag: str, dockerhub_user: str, dockerhub_password: str) -> None:
    createOperatorAndBuildOperatorImage(operator_tag, monitor_tag)
    call(["docker", "login", "--username=" + dockerhub_user,
          "--password=" + dockerhub_password])
    operator_name_and_tag = "snyk/kubernetes-operator:" + operator_tag
    operator_bundle_name_and_tag = "snyk/kubernetes-operator-bundle:" + operator_tag
    call(["docker", "push", operator_name_and_tag])
    call(["docker", "push", operator_bundle_name_and_tag])


if __name__ == '__main__':
    _, operator_tag, monitor_tag, dockerhub_user, dockerhub_password = argv
    createOperatorAndPushToDockerHub(
        operator_tag, monitor_tag, dockerhub_user, dockerhub_password)
