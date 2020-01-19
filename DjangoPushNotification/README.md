# Push Notification Backend Implementation in Django

Push Notification system is divided into 3 parts: 
* **Backend Service:**
  - Handles the subscription information returned by the client and saves that information in the SubscriptionInformation Model.
  - Generates the push requests to the ServiceWorker.js which is listening for the push events.
  
* **Service Worker:**
  - Handles the push events generated from the Backend Service using webpush python library.
  - Creates the Notification.
  
* **Client (Browser):** 
  - Checks the support for the serviceworker.
  - Asks the user to give the permission for notifications.
  - Gets the subscription info for the web application based on the VAPID Key.
  - Sends the subscription info to the backend service to persist it in the database relative to the user.

 
![flow diagram](https://github.com/harshul1610/WebBackend-Boilerplates/blob/master/DjangoPushNotification/pushnotification-flow.png)

### Instructions to run the App

```
python manage.py migrate
python manage.py runserver
```
```
Get the Vapid ey from https://tools.reactpwa.com/vapid
update the update the VAPID key in settings.py
```
```
Go to http://localhost:8000 and give the permissions to receive the notifications.
```
```
Go to http://localhost:8000/sendnotification to generate the notification to the user.
```

### Author
[Harshul Jain](https://github.com/harshul1610)
