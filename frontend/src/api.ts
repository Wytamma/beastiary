import axios from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate } from './interfaces';
import { Run } from './store/data/state';

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
  async getRuns(token: string) {
    return axios.get<Run[]>(`${apiUrl}/api/runs/`, authHeaders(token));
  },
};
