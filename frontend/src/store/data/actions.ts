import { api } from '@/api';
import {
    parseLogFile,
    readFileAsText,
    readRegisteredFile,
} from '@/logParser';
import { runtimeCapabilities } from '@/runtime';
import { Trace, TraceCreate } from '@/interfaces';
import { AxiosResponse } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';
import { State } from '../state';
import {
    commitAddParsedTrace,
    commitReloadParsedTrace,
    commitSetActiveParams,
    commitSetActiveTrace,
    commitSetBurnIn,
    commitSetLocalTraceState,
    commitSetLoadingSamples,
    commitSetSamples,
    commitSetTrace,
    commitSetTraces,
} from './mutations';
import { DataState } from './state';

type MainContext = ActionContext<DataState, State>;

async function readLocalTracePayload(payload: { file: File; localFile?: Trace['localFile'] }) {
    const content = await readFileAsText(payload.file);
    return parseLogFile(payload.file, content, payload.localFile);
}

export const actions = {
    async actionGetTraces(context: MainContext) {
        if (!runtimeCapabilities.supportsServerFiles) {
            return;
        }
        let response: AxiosResponse | null = null;
        try {
            response = await api.getTraces(context.rootState.main.token);
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
        if (response) {
            commitSetTraces(context, response.data);
        }
    },
    async actionCreateTrace(context: MainContext, payload: TraceCreate) {
        if (!runtimeCapabilities.supportsServerFiles) {
            return;
        }
        const loadingNotification = { content: 'saving', showProgress: true };
        commitAddNotification(context, loadingNotification);
        let response: AxiosResponse | null = null;
        try {
            response = await api.createTrace(context.rootState.main.token, payload);
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
        commitRemoveNotification(context, loadingNotification);
        if (response != null) {
            commitSetTrace(context, response.data);
            commitAddNotification(context, { content: 'Trace successfully created', color: 'success' });
        }
    },
    async actionCreateLocalTrace(context: MainContext, payload: { file: File; localFile?: Trace['localFile'] }) {
        const loadingNotification = { content: `Loading ${payload.file.name}...`, showProgress: true };
        commitAddNotification(context, loadingNotification);
        try {
            const trace = await readLocalTracePayload(payload);
            commitAddParsedTrace(context, trace);
            commitSetActiveTrace(context, trace);
            commitAddNotification(context, { content: `${payload.file.name} loaded`, color: 'success' });
        } catch (error) {
            commitAddNotification(context, { content: `Error: ${(error as Error).message}`, color: 'error' });
        }
        commitRemoveNotification(context, loadingNotification);
    },
    async actionSetActiveTrace(context: MainContext, payload: Trace) {
        commitSetActiveTrace(context, payload);
    },
    async actionSetActiveParams(context: MainContext, payload: {traceID: number, params: string[]}) {
        commitSetActiveParams(context, payload);
    },
    async actionGetSamples(
        context: MainContext,
        payload: {trace: Trace,
            skip?: number,
            limit?: number,
            all?: boolean}) {
        if (payload.trace.source === 'local') {
            return;
        }
        const trace = payload.trace;
        const skip = payload.skip ? payload.skip : 0;
        const limit = payload.limit ? payload.limit : 100;
        const all = payload.all ? payload.all : false;
        const loadingNotification = { content: 'Loading samples...', showProgress: true };
        if (skip === 0) {
            commitAddNotification(context, loadingNotification);
        }
        let response: AxiosResponse | null = null;
        try {
            response = await api.getSamples(context.rootState.main.token, trace, skip, limit);
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
        if (response != null) {
            commitSetSamples(context, {traceID: trace.id, data: response.data});
            if (all === true && response.data.length === limit) {
                // if you get back what you request go again
                await dispatchGetSamples(context, {trace, skip: skip + limit, limit, all: true});
            }
        }
        commitRemoveNotification(context, loadingNotification);
    },
    async actionReloadLocalTrace(
        context: MainContext,
        payload: { traceID: number; file?: File; suppressNotification?: boolean },
    ) {
        const trace = context.state.traces[payload.traceID];
        if (!trace || trace.source !== 'local') {
            return;
        }

        const loadingNotification = { content: `Reloading ${trace.path}...`, showProgress: true };
        if (!payload.suppressNotification) {
            commitAddNotification(context, loadingNotification);
        }
        commitSetLoadingSamples(context, { traceID: trace.id, loading: true });
        try {
            const nextFile = payload.file || (trace.localFile?.handleId ? (await readRegisteredFile(trace.localFile.handleId)).file : null);
            if (!nextFile) {
                throw new Error('Choose a local file to reload this trace');
            }
            const localFile = trace.localFile?.handleId ? {
                ...trace.localFile,
                lastModified: nextFile.lastModified,
                size: nextFile.size,
            } : undefined;
            const parsed = await readLocalTracePayload({ file: nextFile, localFile });
            parsed.id = trace.id;
            commitReloadParsedTrace(context, parsed);
            if (!payload.suppressNotification) {
                commitAddNotification(context, { content: `${trace.path} reloaded`, color: 'success' });
            }
        } catch (error) {
            if (trace.localFile?.handleId) {
                commitSetLocalTraceState(context, {
                    traceID: trace.id,
                    localFile: { autoReload: false },
                });
            }
            commitAddNotification(context, { content: `Error: ${(error as Error).message}`, color: 'error' });
        }
        commitSetLoadingSamples(context, { traceID: trace.id, loading: false });
        if (!payload.suppressNotification) {
            commitRemoveNotification(context, loadingNotification);
        }
    },
    async actionPollTraces(context: MainContext) {
        for (const trace of Object.values(context.state.traces)) {
            if (trace.source === 'server') {
                if (!runtimeCapabilities.supportsPolling || trace.isActive !== true || context.state.loadingSamples) {
                    continue;
                }
                const skip = 'state' in trace.parameters ? trace.parameters.state.length : 0;
                await dispatchGetSamples(context, { trace, skip, limit: 10000 });
                continue;
            }

            if (
                !runtimeCapabilities.supportsLocalAutoReload ||
                !trace.localFile ||
                !trace.localFile.handleId ||
                !trace.localFile.autoReload ||
                trace.isLoading
            ) {
                continue;
            }

            try {
                const fileState = await readRegisteredFile(trace.localFile.handleId);
                const hasChanged = fileState.file.lastModified !== trace.localFile.lastModified
                    || fileState.file.size !== trace.localFile.size;
                if (hasChanged) {
                    await dispatchReloadLocalTrace(context, {
                        traceID: trace.id,
                        file: fileState.file,
                        suppressNotification: true,
                    });
                }
            } catch (error) {
                commitSetLocalTraceState(context, {
                    traceID: trace.id,
                    localFile: { autoReload: false },
                });
                commitAddNotification(context, {
                    content: `Auto-reload stopped for ${trace.path}: ${(error as Error).message}`,
                    color: 'warning',
                });
            }
        }
    },
    async actionSetBurnIn(context: MainContext, payload: {traceID: number, burnIn: number}) {
        commitSetBurnIn(context, payload);
    },
    async actionSetLoadingSamples(context: MainContext, payload: {traceID: number, loading: boolean}) {
        commitSetLoadingSamples(context, payload);
    },
};

const { dispatch } = getStoreAccessors<DataState | any, State>('');

export const dispatchGetTraces = dispatch(actions.actionGetTraces);
export const dispatchCreateTrace = dispatch(actions.actionCreateTrace);
export const dispatchCreateLocalTrace = dispatch(actions.actionCreateLocalTrace);
export const dispatchSetActiveTrace = dispatch(actions.actionSetActiveTrace);
export const dispatchGetSamples = dispatch(actions.actionGetSamples);
export const dispatchReloadLocalTrace = dispatch(actions.actionReloadLocalTrace);
export const dispatchPollTraces = dispatch(actions.actionPollTraces);
export const dispatchSetActiveParams = dispatch(actions.actionSetActiveParams);
export const dispatchSetBurnIn = dispatch(actions.actionSetBurnIn);
export const dispatchSetLoadingSamples = dispatch(actions.actionSetLoadingSamples);
