Cloud Storage Examples
======================

*Google Realtime Database and Firestore Database*

The directory contains three examples, two client examples and one admin example.

For Realtime Database use pyrebase4_example. For Firestore use rest_firestore_example, this used firestore4kivy a Python API around Firestore's REST API. 

The third example is for admin, and it is a security risk to include this in apps shared with untrusted users.

The Firestore example is platform independent. The Pyrebase4 example and the Firebase-admin example work on the desktop and on Android, but not on iOS. 

## Client Examples

The client examples demonstrate the same behavior using different databases. This behavior is: create a user, sign in a user, CRUD operations, resume/restart a user, delete a user, and delete all user data.

In each client example main.py must be edited to define APIKEY and PROJECTID.

These examples should be run twice. After the first pass, exit (desktop or mobile) or pause (mobile). Then restart or resume the app to see the additional behaviors. A third run repeats the initial behavior, and so on.

## Admin Example

The admin example [firebase_admin_example]() demonstrates a simple admin task, listing all users.

For security, firebase_admin should never be included in an app distributed to untrusted users. Because the required 'service token key' file enables admin access to the Firebase project. 

## Firebase Setup Checklist

This checklist is not a substitute for reading the Firebase documentation. See the [Firebase quick start](https://firebase.google.com/docs/firestore/quickstart), and [Firebase documentation](https://firebase.google.com/docs).

 - Create a Firebase account and project.
   - This generates the Project ID you will need for client apps.

 - Build->Authentication->Get started->sign-in method->Email/Password->Enable->Save
   - This generates the ApiKey you will need for client apps.

 - Realtime Database->Create Database
   - Select a geographic location for the server.
   - Select default security rules (it doesn't matter).
   - Edit and publish new security rules, use the [Pyrebase4 Example Rules]().

 - Firestore Database->Create Database
   - Select security rules (it doesn't matter).
   - Edit and publish new security rules, use the [Firestore Example Rules]().
   - Select a geographic location for the server.
   - Allow a few minutes for changes to propagate.

 - Firebase Admin
   - Get a service account key from "Firebase->Project Overview->Project Settings->Service Accounts->Generate new private key->Generate key" and save the downloaded file. See [Firebase Admin Example]().














