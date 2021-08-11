import axios from 'axios';
import { apiUrl } from '@/env';
import { TraceCreate } from '@/interfaces';
import { Trace } from './store/data/state';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
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
    return axios.post(`${apiUrl}/api/traces/`, data, authHeaders(token));
  },
};
