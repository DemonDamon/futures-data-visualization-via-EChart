import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { getInstruments } from '../services/api'

interface InstrumentSelectorProps {
  selectedInstrument: string
  onInstrumentChange: (instrument: string) => void
  refreshKey?: number
}

const InstrumentSelector: React.FC<InstrumentSelectorProps> = ({
  selectedInstrument,
  onInstrumentChange,
  refreshKey
}) => {
  const { data: instruments, isLoading, error } = useQuery({
    queryKey: ['instruments', refreshKey],
    queryFn: getInstruments,
  })

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-10 bg-gray-200 rounded"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-red-500 text-sm">
        加载合约列表失败: {error.message}
      </div>
    )
  }

  if (!instruments || instruments.length === 0) {
    return (
      <div className="text-gray-500 text-sm">
        暂无可用合约，请先上传数据
      </div>
    )
  }

  return (
    <div>
      <label htmlFor="instrument-select" className="block text-sm font-medium text-gray-700 mb-2">
        选择合约代码
      </label>
      <select
        id="instrument-select"
        value={selectedInstrument}
        onChange={(e) => onInstrumentChange(e.target.value)}
        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
      >
        <option value="">请选择合约</option>
        {instruments.map((instrument) => (
          <option key={instrument} value={instrument}>
            {instrument}
          </option>
        ))}
      </select>
      
      {instruments.length > 0 && (
        <p className="mt-2 text-sm text-gray-500">
          共 {instruments.length} 个可用合约
        </p>
      )}
    </div>
  )
}

export default InstrumentSelector