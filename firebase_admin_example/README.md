Firebase_admin Example
======================

## Setup

Get a service account key from "Firebase->Project Overview->Project Settings->Service Accounts->Generate new private key->Generate key" and save the downloaded file as './service_account_key.json'.

Google tells you: **Your private key gives access to your project's Firebase services. Keep it confidential and never store it in a public repository.**

**This key grants admin privileges.** It is a major security issue to share this file with untrusted users. From your point of view, everybody is an untrusted user except you.

## Python api documentation

https://firebase.google.com/docs/reference/admin/python

## Install the dependencies

### Desktop

```
pip3 install firebase-admin
```

### Buildozer

```
source.include_exts = py,png,jpg,kv,atlas,json

requirements = python3,kivy, firebase-admin, cachecontrol, msgpack, requests, certifi, charset-normalizer, idna, urllib3, google-api-core, google-auth, cachetools, pyasn1-modules, pyasn1, rsa, pyasn1, googleapis-common-protos, protobuf, google-api-python-client, google-auth-httplib2, httplib2, pyparsing, uritemplate, google-cloud-firestore, google-cloud-core, proto-plus, google-cloud-storage, google-resumable-media, google-crc32c

android.permissions = INTERNET
```

### kivy-ios

firebase-admin does not run on ios, `ModuleNotFoundError: No module named 'mmap'`.