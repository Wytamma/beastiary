export interface TraceCreate {
  path: string;
}

export type TraceSource = "local" | "server" | "url" | "combined";

export interface LocalTraceState {
  handleId?: string;
  autoReload: boolean;
  autoReloadSupported: boolean;
  lastModified?: number;
  size?: number;
}

// Set on the synthetic trace made by combining parameters that share a name across traces.
export interface CombinedTraceInfo {
  // IDs of every trace that contributes to at least one combined parameter.
  memberIDs: number[];
  // For each combined parameter: the traces combined into it and the thinning interval applied to each of them.
  parameters: { [param: string]: { memberIDs: number[]; thinning: number } };
}

export interface Trace {
  id: number;
  path: string;
  headers_line: string;
  delimiter: string;
  last_byte: number;
  source: TraceSource;
  parameters: { [key: string]: Data[] };
  activeParams: string[];
  isActive: boolean;
  burnIn: number;
  isLoading: boolean;
  localFile?: LocalTraceState;
  combined?: CombinedTraceInfo;
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
