#!/usr/bin/python
# Filename: ge_session.py

import boto3

def create_session(profile):
        session = boto3.session.Session(profile_name=profile)

        return session