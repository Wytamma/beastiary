import { apiUrl } from '@/env';
import { InSample, Trace, TraceCreate } from '@/interfaces';
import axios from 'axios';
import { config } from 'vue/types/umd';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    params: {},
  };
}

export const api = {
  async getToken(token: string) {
    return axios.get(`${apiUrl}/api/security/token`, authHeaders(token));
  },
  async getTraces(token: string) {
    return axios.get<Trace[]>(`${apiUrl}/api/traces/`, authHeaders(token));
  },
  async createTrace(token: string,  data: TraceCreate) {
    return axios.post<Trace>(`${apiUrl}/api/traces/`, data, authHeaders(token));
  },
  async getSamples(token: string, trace: Trace, skip: number = 0, limit: number = 100) {
    const options = authHeaders(token);
    options.params = {trace_id: trace.id, skip, limit};
    return axios.get<InSample[]>(`${apiUrl}/api/samples/`, options);
  },
  async listDirectory(token: string, path: string) {
    const options = authHeaders(token);
    options.params = {path};
    return axios.get(`${apiUrl}/api/explorer/`, options);
  },
};
