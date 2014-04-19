HGTP - HTTP Get to Post
=======================
A diminutive tool to make HTTP POST requests from HTTP GET requests.

https://github.com/duozmo/hgtp

Why?
----

Some information on the web is only available through submitting a form that uses the HTTP POST verb. As a result, one can't get a permanent URL to said information. Permanent URLs are useful for sending links to friends, making bookmarks, automatically monitoring for changes, and other uses. This tool converts an ordinary HTTP GET request to a POST request and returns the results, so you can get a permanent URL to the form's results.

Instructions
------------

__Prerequisites__

You need a free [Google App Engine](https://developers.google.com/appengine/) account, with the development server running on your local system.

__Setup__

2. Register the app to your account at [https://appengine.google.com](https://appengine.google.com). You will need to pick a unique app name that no one has ever used before (e.g. "hgtp-01" or "hgtp-dave" or "foobar63"). In `app.yaml`, replace the `application:` name `change_me` with your app name.
3. In `main.py`, change the constant `PASSWORD` to a password of your choice. Since your instance of HGTP needs to be visible to the whole Internet, you want to prevent anyone but you using the service (and eating up your free bandwidth).
1. Add this application to Google App Engine Launcher with File → Add Existing Application. 
4. When you are satisfied things are working, deploy the app from Google App Engine Launcher. For deployment help, read the [official docs](https://developers.google.com/appengine/docs/python/gettingstartedpython27/uploading).
  
__Crafting a URL__

A fictitious but concrete example is:

    http://myhgtpinstance.appspot.com/forward?url=http%3A%2F%2Flevel3.com%2Ffiberform&password=12345&fields=favcolor%3Dred%26favnumber%3D37

Broken down:
    
    URL = HGTP_ADDRESS + "?url=" + REMOTE_URL + "&password=" + PASSWORD + "&fields=" + FIELDS

`HGTP_ADDRESS` is the URL to your instance of this tool. All Google App Engine apps run as http://*your-app-id*.appspot.com. Append the path `/forward`.

`REMOTE_URL` is the form submission address on the remote site. It must be URL encoded. You can quickly encode any string at [meyerweb.com](http://meyerweb.com/eric/tools/dencoder/).

`PASSWORD` is the password you configured during installation.

`FIELDS` are the fields you want to send to the form. You can get these via [Wireshark](http://www.wireshark.org), your web browser's development console, or whatever other means you deem fit. These need to be in standard `key=value` form, joined by `&`, and then [URL encoded](http://meyerweb.com/eric/tools/dencoder/).

__Execution__

With the crafted URL, try running the request through your development server. If that works, you can upload the app to App Engine and use it live on appspot.com.

__Troubleshooting__

You may need to tweak the form fields you send in order to get the remote service to respond correctly. For example, you may need to omit a session identifier from an old session with the remote service (which could be causing an error). Use your best judgement.

To see what you are sending to the remote service, set the `url` query parameter to `http%3A%2F%2Flocalhost%3A[localport]%2Fblackmirror`. (Be sure to replace `[localport]` with your actual local port, e.g. 8080.) A diagnostic page will print out the headers and form fields it receives.

Note that not all remote services will operate normally with this tool. Some services require session tracking as a prerequisite to return form results. You are also [compelled](https://developers.google.com/appengine/docs/python/urlfetch/#Python_Request_headers) (rightly so) to send a `User-Agent` indicating you are using Google App Engine, which some services may balk at.

Limitations
-----------

* __Security warning:__ this tool will happily retrieve data with Secure HTTP (HTTPS) and then retransmit it with clear HTTP. Obviously, do not do this if you are accessing sensitive information.
* Does not maintain state between requests, so any requirement the remote service has for session tracking/cookie setting/referrer/etc. will cause failure.
* Only does GET → POST. Does not convert POST → GET or any other HTTP verbs (PUT, DELETE, etc.).
* Won't load iframes or XHRs in the destination page.
* Does not rewrite relative addresses in the destination page, so images, embeds, includes, etc. will not resolve.
* Does not observe robots.txt.
* Does not validate SSL certs on remote servers. This is to keep life simple as so many ERP systems have misconfigured certs. Again, do not use this tool when security matters.

Discussion
----------

**Why publish this as source code and not a service on the live web?**

Unfortunately, the economics of a live service are terrible and the possibility for abuse is very high. Because the tool just forwards content from one server to another, there's no opportunity to recoup expenses from ads or similar.

Additionally, abusing a service like this is trivial. Several past attempts at creating public GET to POST gateways have been taken offline, possibly due to abuse.

Making each user responsible for his or her own instance of the tool alleviates these problems.


License
-------
Public domain. Do what you want.