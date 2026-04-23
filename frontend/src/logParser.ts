import { LocalTraceState, Trace, TraceSource } from '@/interfaces';

let nextLocalTraceId = -1;
let nextHandleId = 0;

const fileHandleRegistry = new Map<string, FileSystemFileHandle>();

export interface LocalFileSelection {
    file: File;
    localFile: LocalTraceState;
}

interface ParsedTraceOptions {
    localFile?: LocalTraceState;
    path?: string;
    source?: TraceSource;
}

async function yieldToBrowser() {
    await new Promise((resolve) => window.setTimeout(resolve, 0));
}

export function parseLogText(name: string, content: string, options: ParsedTraceOptions = {}): Trace {
    const delimiter = '\t';
    const lines = content.split('\n');

    let headers: string[] = [];
    let headersParsed = false;
    const rawSamples: Array<{ state: number; data: { [key: string]: number | null } }> = [];

    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        if (trimmed.startsWith('#') || trimmed.startsWith('[')) continue;

        if (!headersParsed) {
            headers = trimmed.split(delimiter);
            headers[0] = 'state';
            headersParsed = true;
            continue;
        }

        const values = trimmed.split(delimiter);
        if (values.length < headers.length) continue;

        const data: { [key: string]: number | null } = {};
        for (let i = 0; i < headers.length; i++) {
            const parsed = parseFloat(values[i]);
            data[headers[i]] = isFinite(parsed) ? parsed : null;
        }
        rawSamples.push({ state: data.state as number, data });
    }

    if (!headersParsed || headers.length < 2) {
        throw new Error(`Could not parse headers from ${name}`);
    }

    const parameters: { [key: string]: { state: number; value: number | null }[] } = {};
    for (const header of headers) {
        parameters[header] = rawSamples.map((sample) => ({ state: sample.state, value: sample.data[header] }));
    }

    return {
        id: nextLocalTraceId--,
        path: options.path || name,
        headers_line: headers.join(delimiter),
        delimiter,
        last_byte: content.length,
        source: options.source || 'local',
        parameters,
        activeParams: headers.filter((header) => header !== 'state').slice(0, 1),
        isActive: true,
        burnIn: 10,
        isLoading: false,
        localFile: options.localFile,
    };
}

export async function parseLogTextAsync(name: string, content: string, options: ParsedTraceOptions = {}): Promise<Trace> {
    const delimiter = '\t';
    const lines = content.split('\n');

    let headers: string[] = [];
    let headersParsed = false;
    const rawSamples: Array<{ state: number; data: { [key: string]: number | null } }> = [];

    for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
        if (lineIndex > 0 && lineIndex % 2000 === 0) {
            await yieldToBrowser();
        }

        const trimmed = lines[lineIndex].trim();
        if (!trimmed) continue;
        if (trimmed.startsWith('#') || trimmed.startsWith('[')) continue;

        if (!headersParsed) {
            headers = trimmed.split(delimiter);
            headers[0] = 'state';
            headersParsed = true;
            continue;
        }

        const values = trimmed.split(delimiter);
        if (values.length < headers.length) continue;

        const data: { [key: string]: number | null } = {};
        for (let i = 0; i < headers.length; i++) {
            const parsed = parseFloat(values[i]);
            data[headers[i]] = isFinite(parsed) ? parsed : null;
        }
        rawSamples.push({ state: data.state as number, data });
    }

    if (!headersParsed || headers.length < 2) {
        throw new Error(`Could not parse headers from ${name}`);
    }

    const parameters: { [key: string]: { state: number; value: number | null }[] } = {};
    for (let headerIndex = 0; headerIndex < headers.length; headerIndex++) {
        if (headerIndex > 0 && headerIndex % 25 === 0) {
            await yieldToBrowser();
        }

        const header = headers[headerIndex];
        parameters[header] = rawSamples.map((sample) => ({ state: sample.state, value: sample.data[header] }));
    }

    return {
        id: nextLocalTraceId--,
        path: options.path || name,
        headers_line: headers.join(delimiter),
        delimiter,
        last_byte: content.length,
        source: options.source || 'local',
        parameters,
        activeParams: headers.filter((header) => header !== 'state').slice(0, 1),
        isActive: true,
        burnIn: 10,
        isLoading: false,
        localFile: options.localFile,
    };
}

export function parseLogFile(file: File, content: string, localFile?: LocalTraceState): Trace {
    return parseLogText(file.name, content, {
        localFile,
        path: file.name,
        source: 'local',
    });
}

export async function parseLogFileAsync(file: File, content: string, localFile?: LocalTraceState): Promise<Trace> {
    return parseLogTextAsync(file.name, content, {
        localFile,
        path: file.name,
        source: 'local',
    });
}

export function readFileAsText(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => resolve(event.target!.result as string);
        reader.onerror = () => reject(new Error(`Failed to read ${file.name}`));
        reader.readAsText(file);
    });
}

export function urlFileName(url: string) {
    try {
        const parsed = new URL(url);
        const path = parsed.pathname.split('/').filter(Boolean).pop();
        return path || parsed.hostname || url;
    } catch (error) {
        const sanitized = url.split('#')[0].split('?')[0];
        return sanitized.substring(sanitized.lastIndexOf('/') + 1) || url;
    }
}

export function registerFileHandle(handle: FileSystemFileHandle) {
    const handleId = `local-handle-${nextHandleId++}`;
    fileHandleRegistry.set(handleId, handle);
    return handleId;
}

export async function readRegisteredFile(handleId: string) {
    const handle = fileHandleRegistry.get(handleId);
    if (!handle) {
        throw new Error('Missing file handle for local trace');
    }
    const file = await handle.getFile();
    return {
        file,
        localFile: {
            handleId,
            autoReload: true,
            autoReloadSupported: true,
            lastModified: file.lastModified,
            size: file.size,
        } as LocalTraceState,
    };
}

export async function pickFilesWithHandles() {
    if (typeof window === 'undefined' || typeof window.showOpenFilePicker !== 'function') {
        throw new Error('File System Access API is not available');
    }
    const handles = await window.showOpenFilePicker({
        multiple: true,
        types: [
            {
                description: 'Beast log files',
                accept: {
                    'text/plain': ['.log', '.txt', '.tsv', '.csv'],
                },
            },
        ],
    });

    return Promise.all(handles.map(async (handle) => {
        const handleId = registerFileHandle(handle);
        const file = await handle.getFile();
        return {
            file,
            localFile: {
                handleId,
                autoReload: true,
                autoReloadSupported: true,
                lastModified: file.lastModified,
                size: file.size,
            } as LocalTraceState,
        };
    }));
}
