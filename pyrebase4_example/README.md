Pyrebase4 Example
=================

# Setup

Assuming you have created and initialized a Firebase project:
 - Specify the project ID and Key in `main.py`.
 - Specify the Realtime Database Rules.
 - Install the dependencies.

## Specify the project ID and Key

Get the "apiKey" and "Project ID" for your project from `Firebase->Project Overview->Project settings->General` and replace these placeholders in `main.py`:
```
APIKEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
PROJECT_ID = 'bbbbbbbbbb'
```

## Specify the Realtime Database Rules:

In "Firebase->Build->Realtime Database->Rules" replace the default rules with these rules, then publish.

```
{
  "rules": {
    "id": {	
      "$uid" : {
          ".read": "$uid === auth.uid",
    	  ".write": "$uid === auth.uid"
      }		
    },	
    "data": {	
      "$uid" : {
        ".read": "$uid === auth.uid",
    	".write": "$uid === auth.uid"
      }		
    },
    "more_data": {	
      "$uid" : {
    	".read": "$uid === auth.uid",
    	".write": "$uid === auth.uid"
      }		
    }	    
  }
}

```
This example uses the "Production-ready rules", for "content-owner only access".
[Google Docs](https://firebase.google.com/docs/rules/basics#content-owner_only_access).

To see the database contents, go to "Firebase->Build->Realtime Database->Data"

## Install the dependencies

### Desktop

```
pip3 install pyrebase4
```

### Buildozer

```
requirements = python3,kivy, pyrebase4, gcloud, googleapis-common-protos, protobuf, httplib2, pyparsing, oauth2client, pyasn1, pyasn1-modules, rsa, pycryptodome, python-jwt, jws, requests, certifi, charset-normalizer, idna, urllib3, requests-toolbelt , jwcrypto, cryptography, deprecated, wrapt

android.permissions = INTERNET
```

### kivy-ios

As of 2022/08 the Pyrebase4 does not run on kivy-ios. The error message is `OSError: Cannot load native module 'Crypto.Hash._SHA256'.....` and it is due to the loack of a pycryptodome recipe.
