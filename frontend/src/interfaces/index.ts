export interface TraceCreate {
    path: string;
}

export interface Trace {
    id: number;
    path: string;
    headers_line: string;
    last_byte: number;
    parameters: {[key: string]: Data[]};
}

export interface Data {
    state: number;
    value: number | null;
}

export interface Parameter {
    name: string;
    data: Data[];
}

export interface inSample {
    id: number;
    trace_id: number;
    state: number;
    data: inSampleData;
}

export interface inSampleData {
    [key: string]: number | null;
}

export interface SetSample {
    trace: Trace;
    data: inSample[];
}
