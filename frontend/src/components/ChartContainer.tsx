import React, { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'
import { useQuery } from '@tanstack/react-query'
import { getChartData } from '../services/api'

interface ChartContainerProps {
  instrument: string
  refreshKey?: number
}

const ChartContainer: React.FC<ChartContainerProps> = ({ instrument, refreshKey }) => {
  const [chartType, setChartType] = useState<'candlestick' | 'line'>('candlestick')

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['chartData', instrument, refreshKey],
    queryFn: () => getChartData({ instrument }),
    enabled: !!instrument,
  })

  useEffect(() => {
    if (refreshKey) {
      refetch()
    }
  }, [refreshKey, refetch])

  const getOption = () => {
    if (!data?.data || data.data.length === 0) {
      return {
        title: {
          text: '暂无数据',
          left: 'center',
          top: 'center'
        }
      }
    }

    const baseOption = {
      title: {
        text: `${instrument} - ${chartType === 'candlestick' ? 'K线图' : '折线图'}`,
        left: 'left'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        formatter: function (params: any) {
          const data = params[0]
          if (chartType === 'candlestick') {
            return `
              时间: ${new Date(data.data[0]).toLocaleString()}<br/>
              开盘: ${data.data[1]}<br/>
              收盘: ${data.data[2]}<br/>
              最低: ${data.data[3]}<br/>
              最高: ${data.data[4]}<br/>
              成交量: ${data.data[5]}
            `
          } else {
            return `
              时间: ${new Date(data.data[0]).toLocaleString()}<br/>
              价格: ${data.data[1]}
            `
          }
        }
      },
      xAxis: {
        type: 'time',
        scale: true,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        splitNumber: 20,
        min: 'dataMin',
        max: 'dataMax'
      },
      yAxis: {
        scale: true,
        splitArea: {
          show: true
        }
      },
      dataZoom: [
        {
          type: 'inside',
          start: 50,
          end: 100
        },
        {
          show: true,
          type: 'slider',
          top: '90%',
          start: 50,
          end: 100
        }
      ],
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%'
      }
    }

    if (chartType === 'candlestick') {
      return {
        ...baseOption,
        series: [
          {
            name: 'K线',
            type: 'candlestick',
            data: data.data.map((item: number[]) => [
              item[0], // 时间
              item[1], // 开盘
              item[2], // 收盘
              item[3], // 最低
              item[4]  // 最高
            ]),
            itemStyle: {
              color: '#ef4444',
              color0: '#10b981',
              borderColor: '#ef4444',
              borderColor0: '#10b981'
            }
          }
        ]
      }
    } else {
      return {
        ...baseOption,
        series: [
          {
            name: '收盘价',
            type: 'line',
            data: data.data.map((item: number[]) => [item[0], item[2]]),
            smooth: true,
            lineStyle: {
              color: '#3b82f6'
            }
          }
        ]
      }
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-red-500 text-center">
          <p className="text-lg font-medium">加载失败</p>
          <p className="text-sm mt-2">{error.message}</p>
          <button
            onClick={() => refetch()}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            重试
          </button>
        </div>
      </div>
    )
  }

  return (
    <div>
      {/* 图表类型切换 */}
      <div className="mb-4 flex space-x-2">
        <button
          onClick={() => setChartType('candlestick')}
          className={`px-4 py-2 rounded ${
            chartType === 'candlestick'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          K线图
        </button>
        <button
          onClick={() => setChartType('line')}
          className={`px-4 py-2 rounded ${
            chartType === 'line'
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          折线图
        </button>
      </div>

      {/* 图表 */}
      <ReactECharts
        option={getOption()}
        style={{ height: '500px', width: '100%' }}
        opts={{ renderer: 'canvas' }}
      />
    </div>
  )
}

export default ChartContainer