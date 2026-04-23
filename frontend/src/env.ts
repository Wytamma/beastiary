const env = process.env.VUE_APP_ENV;
const mode = process.env.VUE_APP_MODE;

let envApiUrl = '';

if (mode === 'static') {
  envApiUrl = '';
} else if (process.env.NODE_ENV !== 'production') {
  envApiUrl = '';
} else if (env === 'production') {
  envApiUrl = `${process.env.VUE_APP_DOMAIN_PROD}`;
} else if (env === 'staging') {
  envApiUrl = `${process.env.VUE_APP_DOMAIN_STAG}`;
} else {
  envApiUrl = `${process.env.VUE_APP_DOMAIN_DEV}`;
}

export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;
