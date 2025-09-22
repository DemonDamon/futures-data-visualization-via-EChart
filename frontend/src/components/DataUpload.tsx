import React, { useState, useRef } from 'react'
import { uploadCsvFile } from '../services/api'
import { CloudArrowUpIcon, DocumentIcon } from '@heroicons/react/24/outline'

interface DataUploadProps {
  onUploadSuccess: () => void
}

const DataUpload: React.FC<DataUploadProps> = ({ onUploadSuccess }) => {
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<{
    type: 'success' | 'error' | null
    message: string
  }>({ type: null, message: '' })
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    if (!file.name.endsWith('.csv')) {
      setUploadStatus({
        type: 'error',
        message: '请选择CSV格式的文件'
      })
      return
    }

    await handleUpload(file)
  }

  const handleDrop = async (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    
    if (!file) return

    if (!file.name.endsWith('.csv')) {
      setUploadStatus({
        type: 'error',
        message: '请选择CSV格式的文件'
      })
      return
    }

    await handleUpload(file)
  }

  const handleUpload = async (file: File) => {
    setIsUploading(true)
    setUploadStatus({ type: null, message: '' })

    try {
      const result = await uploadCsvFile(file)
      setUploadStatus({
        type: 'success',
        message: `上传成功！文件: ${result.filename}，导入 ${result.records_count} 条记录`
      })
      onUploadSuccess()
      
      // 清空文件输入
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    } catch (error) {
      setUploadStatus({
        type: 'error',
        message: error instanceof Error ? error.message : '上传失败'
      })
    } finally {
      setIsUploading(false)
    }
  }

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
  }

  return (
    <div className="space-y-4">
      {/* 拖拽上传区域 */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors cursor-pointer"
        onClick={() => fileInputRef.current?.click()}
      >
        <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
        <div className="mt-4">
          <p className="text-sm text-gray-600">
            <span className="font-medium text-blue-600 hover:text-blue-500">
              点击上传
            </span>
            {' '}或拖拽文件到此处
          </p>
          <p className="text-xs text-gray-500 mt-1">
            支持CSV格式文件，最大10MB
          </p>
        </div>
      </div>

      {/* 隐藏的文件输入 */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileSelect}
        className="hidden"
      />

      {/* 上传状态 */}
      {isUploading && (
        <div className="flex items-center justify-center space-x-2 text-blue-600">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          <span className="text-sm">正在上传...</span>
        </div>
      )}

      {/* 上传结果 */}
      {uploadStatus.type && (
        <div
          className={`p-3 rounded-md text-sm ${
            uploadStatus.type === 'success'
              ? 'bg-green-50 text-green-800 border border-green-200'
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}
        >
          <div className="flex items-start space-x-2">
            <DocumentIcon className="h-4 w-4 mt-0.5 flex-shrink-0" />
            <span>{uploadStatus.message}</span>
          </div>
        </div>
      )}

      {/* 数据格式说明 */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
        <h4 className="text-sm font-medium text-blue-800 mb-2">CSV文件格式要求：</h4>
        <ul className="text-xs text-blue-700 space-y-1">
          <li>• 必须包含列：instrument, time, interface, open, high, low, close, volume</li>
          <li>• time格式：YYYY-MM-DD HH:MM:SS</li>
          <li>• 价格字段为数值类型</li>
          <li>• 文件编码：UTF-8</li>
        </ul>
      </div>
    </div>
  )
}

export default DataUpload