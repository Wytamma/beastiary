# Web App

The browser-only Beastiary app is available at [http://beastiary.wytamma.com/web](http://beastiary.wytamma.com/web).

This version is designed for quick inspection and sharing of trace files without running a Beastiary server.

## Client-side loading

When you load a local log file in the web app, the file is parsed directly in your browser.

Your files do not leave your computer:

- local files are read from your machine by the browser
- parsing happens client-side in the web app
- the file contents are not uploaded to a Beastiary backend

This makes the hosted web version useful for private or ad hoc inspection when you do not want to start a server.

## URL-based traces

The web app can also load trace files from a public URL.

Open the `Add trace` dialog and use the `URL files` section to add a link to a `.log` or `.csv` trace file. Beastiary will fetch that file in the browser and parse it client-side.

This works well for files hosted on GitHub, object storage, or other static file hosts, as long as the URL can be fetched by the browser.

## Shareable links

URL traces are synced into the page URL using the `traces` query parameter.

For example:

[https://beastiary.wytamma.com/web/#/main/dashboard?traces=https://raw.githubusercontent.com/Wytamma/beastiary/refs/heads/master/backend/tests/data/hcv_coal.log](https://beastiary.wytamma.com/web/#/main/dashboard?traces=https://raw.githubusercontent.com/Wytamma/beastiary/refs/heads/master/backend/tests/data/hcv_coal.log)

You can include [multiple trace URLs](https://beastiary.wytamma.com/web/#/main/dashboard?traces=https://raw.githubusercontent.com/Wytamma/beastiary/refs/heads/master/backend/tests/data/hcv_coal.log&traces=https://raw.githubusercontent.com/Wytamma/beastiary/refs/heads/master/backend/tests/data/beast1.log) by repeating the parameter.

When someone opens that link, Beastiary will automatically import those trace files into the app.

## Notes

- Local files are not shareable through the page URL because they only exist on your computer.
- URL traces can be shared because the file can be fetched again by anyone who opens the link.
- URL loading depends on the remote host allowing browser access to the file.
