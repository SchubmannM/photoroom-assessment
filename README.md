# Technical assessment for PhotoRoom.

Some demo to make testing easier: https://nextcloud.schubmann.dev/s/p4LFCKQjow8rG6k/download/Insomnia_d4pdDTtv5X.mp4

All use cases were covered as far as I see - but I ran out of time so decided to clean up the code instead of writing tests (not a lot of custom logic in there either way). This is obviously not ready to be deployed on a production server (-> SECRET_KEY is in there!).

For the bonus question 9: I would use Django Channels to create websocket connections with the clients and server - and then publish events to all clients whenever a change to a palette was done on the server side.
