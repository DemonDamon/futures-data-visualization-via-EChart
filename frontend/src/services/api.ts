import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// 数据类型定义
export interface FuturesData {
  instrument: string
  time: string
  interface: string
  open: number
  high: number
  low: number
  close: number
  volume: number
  open_interest?: number
}

export interface FuturesDataResponse {
  data: FuturesData[]
  total: number
  page: number
  page_size: number
}

export interface ChartDataRequest {
  instrument: string
  start_time?: string
  end_time?: string
  interval?: string
}

export interface ChartDataResponse {
  instrument: string
  data: number[][] // [timestamp, open, close, low, high, volume]
}

export interface UploadResponse {
  message: string
  filename: string
  records_count: number
}

// API函数
export const getFuturesData = async (params: {
  instrument?: string
  start_time?: string
  end_time?: string
  page?: number
  page_size?: number
}): Promise<FuturesDataResponse> => {
  return api.get('/futures/data', { params })
}

export const getChartData = async (request: ChartDataRequest): Promise<ChartDataResponse> => {
  return api.post('/futures/chart-data', request)
}

export const getInstruments = async (): Promise<string[]> => {
  return api.get('/futures/instruments')
}

export const uploadCsvFile = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)
  
  return api.post('/futures/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export const clearData = async (instrument?: string): Promise<{ message: string; deleted_count: number }> => {
  return api.delete('/futures/data', {
    params: instrument ? { instrument } : {},
  })
}

export default api