# frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles the server-backed frontend into the backend bundle
```
npm run build
```

### Compiles the static frontend bundle
```
npm run build:static
```

This writes the static site into `../docs/web` and sets its asset base path to `/web/`, so it is published as `https://<docs-site>/web/` when the MkDocs site is deployed.

The merged frontend now supports two runtime modes:

- `server`: login, remote server file browsing, API-backed polling, and local client-side file loading
- `static`: browser-only mode with local file loading and hash routing for static hosting

Local traces work in both modes. When the browser supports the File System Access API and files are opened with the auto-reload picker, Beastiary can re-read those local files automatically. Drag-and-drop and plain file input remain available as a fallback and support manual reload only.

### Run your tests
```
npm run test
```

### Lints and fixes files
```
npm run lint
```

### Run your unit tests
```
npm run test:unit
```
