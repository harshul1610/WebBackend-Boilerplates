// checks the support for the serviceworker
const registerSw = async () => {
    if ('serviceWorker' in navigator) {
        const reg = await navigator.serviceWorker.register('serviceworker.js');
        initialiseState(reg);
    } else {
        alert("You can't receive push notifications")
    }
};

// Get the User Permission if notification should be allowed or not.
const initialiseState = (reg) => {
    console.log('User Permission: ' + Notification.permission);
    if (!reg.showNotification) {
        console.log('Showing notifications isn\'t supported');
        return
    }
    if (Notification.permission === 'denied') {
        console.log('You prevented us from showing notifications');
        return
    }
    if (!'PushManager' in window) {
        console.log("Push isn't allowed in your browser");
        return
    }
    subscribe(reg);
}

// encoding Algorithm
function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    const outputData = outputArray.map((output, index) => rawData.charCodeAt(index));

    return outputData;
}

// Once the User grants permission, subscribe the application with the application VAPID Key.
// Send the Application subscription info to the database for that user.
const subscribe = async (reg) => {
    const subscription = await reg.pushManager.getSubscription();
    if (subscription) {
        console.log('subscription already done');
        sendSubData(subscription, 'subscribe');
        return;
    }

    console.log('subscribing the application');
    const vapidMeta = document.querySelector('meta[name="vapid-key"]');
    const key = vapidMeta.content;
    const options = {
        userVisibleOnly: true,
        ...(key && {applicationServerKey: urlB64ToUint8Array(key)}),
    };
    const sub = await reg.pushManager.subscribe(options);
    sendSubData(sub, 'subscribe');
}

const sendSubData = async (subscription, status_type) => {
    const browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase();
    const data = {
        status_type: status_type,
        subscription: subscription.toJSON(),
        browser: browser,
    };

    const res = await fetch('/saveinformation', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'content-type': 'application/json'
        },
        credentials: "include"
    });

    handleResponse(res);
};

const handleResponse = (res) => {
    console.log(res.status);
};

registerSw();