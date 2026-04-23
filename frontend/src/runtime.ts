export type FrontendMode = 'server' | 'static';
export type RouterMode = 'hash' | 'history' | 'abstract';

const requestedMode = process.env.VUE_APP_MODE;

export const frontendMode: FrontendMode = requestedMode === 'static' ? 'static' : 'server';

export const runtimeCapabilities = {
  supportsAuth: frontendMode === 'server',
  supportsServerFiles: frontendMode === 'server',
  supportsPolling: frontendMode === 'server',
  supportsLocalFiles: true,
  supportsLocalAutoReload: true,
  routerMode: (frontendMode === 'static' ? 'hash' : 'history') as RouterMode,
  defaultRoute: '/main/dashboard',
};

export function supportsFileSystemAccessApi() {
  return typeof window !== 'undefined' && typeof window.showOpenFilePicker === 'function';
}
