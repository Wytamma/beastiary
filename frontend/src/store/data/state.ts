
export interface Run {
    path: string;
    headers_line: string;
    last_byte: number;
    first_byte: number;
    id: number;
}

export interface DataState {
    runs: Run[];
}
