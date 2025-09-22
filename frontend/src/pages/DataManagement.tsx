import React, { useState, useEffect } from 'react';
import { CloudArrowUpIcon, DocumentIcon, TrashIcon, EyeIcon } from '@heroicons/react/24/outline';
import { useAuthStore } from '../stores/authStore';
import axios from 'axios';

interface Dataset {
  id: string;
  name: string;
  description: string;
  file_path: string;
  created_at: string;
  record_count: number;
}

interface KlineData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

const DataManagement: React.FC = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewData, setPreviewData] = useState<KlineData[]>([]);
  const [showPreview, setShowPreview] = useState(false);
  const [previewDataset, setPreviewDataset] = useState<Dataset | null>(null);
  
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      fetchDatasets();
    }
  }, [isAuthenticated]);

  const fetchDatasets = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get('/data/datasets');
      setDatasets(response.data);
    } catch (error: any) {
      setError('获取数据集失败');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
        setError('请选择CSV格式的文件');
        return;
      }
      setSelectedFile(file);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('请先选择文件');
      return;
    }

    setUploadLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('name', selectedFile.name.replace('.csv', ''));
    formData.append('description', `从文件 ${selectedFile.name} 导入的数据`);

    try {
      await axios.post('/data/upload-csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      setSelectedFile(null);
      // 重置文件输入
      const fileInput = document.getElementById('file-upload') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
      await fetchDatasets();
    } catch (error: any) {
      setError(error.response?.data?.detail || '上传失败');
    } finally {
      setUploadLoading(false);
    }
  };

  const handleDelete = async (datasetId: string) => {
    if (!confirm('确定要删除这个数据集吗？此操作不可恢复。')) {
      return;
    }

    try {
      await axios.delete(`/data/datasets/${datasetId}`);
      await fetchDatasets();
    } catch (error: any) {
      setError('删除失败');
    }
  };

  const handlePreview = async (dataset: Dataset) => {
    setIsLoading(true);
    try {
      const response = await axios.get(`/data/datasets/${dataset.id}/kline-data?limit=100`);
      setPreviewData(response.data);
      setPreviewDataset(dataset);
      setShowPreview(true);
    } catch (error: any) {
      setError('获取预览数据失败');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('zh-CN');
  };

  const formatNumber = (num: number) => {
    return num.toLocaleString('zh-CN', { maximumFractionDigits: 2 });
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">请先登录</h2>
          <p className="text-gray-600">您需要登录后才能管理数据</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">数据管理</h1>
          <p className="mt-2 text-gray-600">上传和管理您的期货数据文件</p>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
            {error}
          </div>
        )}

        {/* 文件上传区域 */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">上传CSV数据文件</h2>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
            <div className="text-center">
              <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
              <div className="mt-4">
                <label htmlFor="file-upload" className="cursor-pointer">
                  <span className="mt-2 block text-sm font-medium text-gray-900">
                    {selectedFile ? selectedFile.name : '选择CSV文件或拖拽到此处'}
                  </span>
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    accept=".csv"
                    className="sr-only"
                    onChange={handleFileSelect}
                  />
                </label>
                <p className="mt-1 text-xs text-gray-500">
                  支持CSV格式，文件应包含：日期、开盘价、最高价、最低价、收盘价、成交量
                </p>
              </div>
              {selectedFile && (
                <div className="mt-4">
                  <button
                    onClick={handleUpload}
                    disabled={uploadLoading}
                    className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {uploadLoading ? '上传中...' : '开始上传'}
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 数据集列表 */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">我的数据集</h2>
          </div>
          
          {isLoading ? (
            <div className="p-6 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">加载中...</p>
            </div>
          ) : datasets.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              <DocumentIcon className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2">暂无数据集，请上传CSV文件</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      名称
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      描述
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      记录数
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      创建时间
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {datasets.map((dataset) => (
                    <tr key={dataset.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {dataset.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {dataset.description}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatNumber(dataset.record_count)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(dataset.created_at)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handlePreview(dataset)}
                            className="text-blue-600 hover:text-blue-900"
                            title="预览数据"
                          >
                            <EyeIcon className="h-5 w-5" />
                          </button>
                          <button
                            onClick={() => handleDelete(dataset.id)}
                            className="text-red-600 hover:text-red-900"
                            title="删除数据集"
                          >
                            <TrashIcon className="h-5 w-5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* 数据预览模态框 */}
        {showPreview && previewDataset && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  数据预览 - {previewDataset.name}
                </h3>
                <button
                  onClick={() => setShowPreview(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="overflow-x-auto max-h-96">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">日期</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">开盘</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">最高</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">最低</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">收盘</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">成交量</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {previewData.map((row, index) => (
                      <tr key={index} className="hover:bg-gray-50">
                        <td className="px-4 py-2 text-sm text-gray-900">{row.date}</td>
                        <td className="px-4 py-2 text-sm text-gray-900">{formatNumber(row.open)}</td>
                        <td className="px-4 py-2 text-sm text-gray-900">{formatNumber(row.high)}</td>
                        <td className="px-4 py-2 text-sm text-gray-900">{formatNumber(row.low)}</td>
                        <td className="px-4 py-2 text-sm text-gray-900">{formatNumber(row.close)}</td>
                        <td className="px-4 py-2 text-sm text-gray-900">{formatNumber(row.volume)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="mt-4 text-sm text-gray-500 text-center">
                显示前100条记录，总计 {formatNumber(previewDataset.record_count)} 条
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataManagement;