REST Firestore Example
=======================

# Overview

The example is as much for reading as executing. The example depends on [firestore4kivy](https://github.com/Android-for-Python/firestore4kivy).

The example executes in two passes.

The first pass validates user creation, login, and basic Firestore operations, and saves public and private documents. Close or pause the app. You can view the contents of saved documents in Firebase.

The second pass validates login via a token, and validates some complex update operations. All documents and the user are removed from Firestore.

# Setup

Assuming you have created and initialized a Firebase project 
 - Specify the project ID and Key in main.py.
 - Specify the Firestore Database Rules.
 - Install the dependencies.

## Specify the project ID and Key

Get the `apiKey` and `Project ID` for your project from `Firebase->Project Overview->Project settings->General` and replace these placeholders in `main.py`:
```
APIKEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
PROJECT_ID = 'bbbbbbbbbb'
```

## Specify the Firestore Database Rules:

In `Firebase->Build->Firestore Database->Rules` replace the default rules with these rules, then publish.

```
service cloud.firestore {
  match /databases/{database}/documents {
    match /id/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId
    }
    match /data/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId
    }
    match /shared/configuration {
      allow read, write: if request.auth != null
    }
  }
}
```

## Install the dependencies

### Desktop 

```
pip3 install firestore4kivy
```

### Buildozer 

```
requirements = python3, kivy, firestore4kivy, requests, urllib3, charset-normalizer==2.1.1, idna, certifi

android.permissions = INTERNET
```

### kivy-ios

```
toolchain pip install firestore4kivy
```

