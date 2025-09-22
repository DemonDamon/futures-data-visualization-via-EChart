import React from 'react';
import ReactECharts from 'echarts-for-react';

const DemoChart: React.FC = () => {
  // 模拟期货K线数据 (日期, 开盘, 收盘, 最低, 最高)
  const demoData = [
    ['2024-01-01', 2320.26, 2320.26, 2287.3, 2362.94],
    ['2024-01-02', 2300, 2291.3, 2288.26, 2308.38],
    ['2024-01-03', 2295.35, 2346.5, 2295.35, 2346.92],
    ['2024-01-04', 2347.22, 2358.98, 2337.35, 2363.8],
    ['2024-01-05', 2360.75, 2382.48, 2347.89, 2383.76],
    ['2024-01-08', 2383.43, 2385.42, 2371.23, 2391.82],
    ['2024-01-09', 2377.41, 2419.02, 2369.57, 2421.15],
    ['2024-01-10', 2425.92, 2428.15, 2417.58, 2440.38],
    ['2024-01-11', 2411, 2433.13, 2403.3, 2437.42],
    ['2024-01-12', 2432.68, 2434.48, 2427.7, 2441.73],
    ['2024-01-15', 2430.69, 2418.53, 2394.22, 2433.89],
    ['2024-01-16', 2416.62, 2432.4, 2414.4, 2443.03],
    ['2024-01-17', 2441.91, 2421.56, 2415.43, 2444.8],
    ['2024-01-18', 2420.26, 2382.91, 2373.53, 2427.07],
    ['2024-01-19', 2383.49, 2397.18, 2370.61, 2397.94],
    ['2024-01-22', 2378.82, 2325.95, 2309.17, 2378.82],
    ['2024-01-23', 2322.94, 2314.16, 2308.76, 2330.88],
    ['2024-01-24', 2320.62, 2325.82, 2315.01, 2338.78],
    ['2024-01-25', 2313.74, 2293.34, 2289.89, 2340.71],
    ['2024-01-26', 2297.77, 2313.22, 2292.03, 2324.63],
    ['2024-01-29', 2322.32, 2365.59, 2308.92, 2366.16],
    ['2024-01-30', 2364.54, 2359.51, 2330.86, 2369.65],
    ['2024-01-31', 2332.08, 2273.4, 2259.25, 2333.54],
    ['2024-02-01', 2274.81, 2326.31, 2270.1, 2328.14],
    ['2024-02-02', 2333.61, 2347.18, 2321.6, 2351.44],
    ['2024-02-05', 2340.44, 2324.29, 2304.27, 2352.02],
    ['2024-02-06', 2326.42, 2318.61, 2314.59, 2333.67],
    ['2024-02-07', 2314.68, 2310.59, 2296.58, 2320.96],
    ['2024-02-08', 2309.16, 2286.6, 2264.83, 2333.29],
    ['2024-02-09', 2282.17, 2263.97, 2253.25, 2286.33]
  ];

  // 计算移动平均线
  const calculateMA = (data: number[][], period: number) => {
    const result = [];
    for (let i = 0; i < data.length; i++) {
      if (i < period - 1) {
        result.push('-');
      } else {
        let sum = 0;
        for (let j = 0; j < period; j++) {
          sum += data[i - j][2]; // 收盘价
        }
        result.push((sum / period).toFixed(2));
      }
    }
    return result;
  };

  const ma5 = calculateMA(demoData, 5);
  const ma10 = calculateMA(demoData, 10);
  const ma20 = calculateMA(demoData, 20);

  const option = {
    title: {
      text: '期货合约 - 沪深300指数',
      left: 0,
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      backgroundColor: 'rgba(245, 245, 245, 0.8)',
      borderWidth: 1,
      borderColor: '#ccc',
      textStyle: {
        color: '#000'
      },
      formatter: function (params: any) {
        const data = params[0];
        const klineData = data.data;
        return [
          '日期: ' + data.name,
          '开盘: ' + klineData[1],
          '收盘: ' + klineData[2],
          '最低: ' + klineData[3],
          '最高: ' + klineData[4]
        ].join('<br/>');
      }
    },
    legend: {
      data: ['K线', 'MA5', 'MA10', 'MA20'],
      top: 30
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%'
    },
    xAxis: {
      type: 'category',
      data: demoData.map(item => item[0]),
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
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
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: demoData,
        itemStyle: {
          color: '#ef4444',
          color0: '#22c55e',
          borderColor: '#ef4444',
          borderColor0: '#22c55e'
        },
        markPoint: {
          label: {
            formatter: function (param: any) {
              return param != null ? Math.round(param.value) + '' : '';
            }
          },
          data: [
            {
              name: '最高值',
              type: 'max',
              valueDim: 'highest'
            },
            {
              name: '最低值',
              type: 'min',
              valueDim: 'lowest'
            }
          ],
          tooltip: {
            formatter: function (param: any) {
              return param.name + '<br>' + (param.data.coord || '');
            }
          }
        }
      },
      {
        name: 'MA5',
        type: 'line',
        data: ma5,
        smooth: true,
        lineStyle: {
          opacity: 0.8,
          width: 1
        },
        itemStyle: {
          color: '#3b82f6'
        }
      },
      {
        name: 'MA10',
        type: 'line',
        data: ma10,
        smooth: true,
        lineStyle: {
          opacity: 0.8,
          width: 1
        },
        itemStyle: {
          color: '#f59e0b'
        }
      },
      {
        name: 'MA20',
        type: 'line',
        data: ma20,
        smooth: true,
        lineStyle: {
          opacity: 0.8,
          width: 1
        },
        itemStyle: {
          color: '#8b5cf6'
        }
      }
    ]
  };

  return (
    <div className="w-full">
      <ReactECharts
        option={option}
        style={{ height: '500px', width: '100%' }}
        opts={{ renderer: 'canvas' }}
      />
      <div className="mt-4 text-sm text-gray-600 text-center">
        <p>演示数据 - 支持鼠标滚轮缩放、拖拽平移，底部滑块调节时间范围</p>
      </div>
    </div>
  );
};

export default DemoChart;