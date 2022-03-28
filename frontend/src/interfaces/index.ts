export interface TraceCreate {
    path: string;
}

export interface Trace {
    id: number;
    path: string;
    headers_line: string;
    delimiter: string;
    last_byte: number;
    parameters: {[key: string]: Data[]};
    activeParams: string[];
    isActive: boolean;
    burnIn: number;
}

export interface Traces {
    [id: number]: Trace;
}


export interface Data {
    state: number;
    value: number | null;
}

export interface Parameter {
    name: string;
    data: Data[];
}

export interface InSample {
    id: number;
    trace_id: number;
    state: number;
    data: InSampleData;
}

export interface InSampleData {
    [key: string]: number | null;
}

export interface SetSample {
    trace: Trace;
    data: InSample[];
}
