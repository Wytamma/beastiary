import { Trace } from '@/interfaces';

export interface DataState {
    traces: Trace[];
    activeTraceID: number | null;
    activeParam: string | null;
    burnIn: number;
    loadingSamples: boolean;
}
