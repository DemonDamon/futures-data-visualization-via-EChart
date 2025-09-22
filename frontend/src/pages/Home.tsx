import React from 'react';
import { Link } from 'react-router-dom';
import { ChartBarIcon, CloudArrowUpIcon, CogIcon, UserGroupIcon } from '@heroicons/react/24/outline';
import DemoChart from '../components/DemoChart';

const Home: React.FC = () => {
  const features = [
    {
      icon: ChartBarIcon,
      title: '专业K线图表',
      description: '基于ECharts的高性能K线图表，支持多种技术指标和自定义配置'
    },
    {
      icon: CloudArrowUpIcon,
      title: 'CSV数据导入',
      description: '支持CSV格式的期货数据导入，快速构建您的数据分析环境'
    },
    {
      icon: CogIcon,
      title: '灵活配置',
      description: '丰富的图表配置选项，满足不同的分析需求和个性化展示'
    },
    {
      icon: UserGroupIcon,
      title: '用户管理',
      description: '完善的用户认证和权限管理，保护您的数据安全'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              期货数据
              <span className="text-blue-600">可视化平台</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              专业的期货数据分析工具，提供实时K线图表、数据管理和智能分析功能，
              助您洞察市场趋势，把握投资机会。
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/dashboard"
                className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                立即开始
              </Link>
              <Link
                to="/login"
                className="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
              >
                登录账户
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Demo Chart Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">实时K线图表演示</h2>
          <p className="text-lg text-gray-600">
            体验我们强大的图表功能，支持缩放、平移和多种技术指标
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-lg p-6">
          <DemoChart />
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">核心功能</h2>
          <p className="text-lg text-gray-600">
            为期货交易者和分析师量身打造的专业工具
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => {
            const IconComponent = feature.icon;
            return (
              <div key={index} className="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <IconComponent className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Quick Start Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">快速开始</h2>
            <p className="text-lg text-gray-600">
              三步即可开始您的数据分析之旅
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">注册账户</h3>
              <p className="text-gray-600">
                创建您的专属账户，享受个性化的数据分析体验
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">上传数据</h3>
              <p className="text-gray-600">
                导入您的期货数据文件，支持CSV格式，快速建立数据集
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">开始分析</h3>
              <p className="text-gray-600">
                使用强大的图表工具分析数据，发现市场机会
              </p>
            </div>
          </div>
          <div className="text-center mt-12">
            <Link
              to="/register"
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors inline-block"
            >
              立即注册
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold mb-4">期货数据可视化平台</h3>
            <p className="text-gray-400 mb-6">
              专业、可靠、易用的期货数据分析工具
            </p>
            <div className="flex justify-center space-x-6">
              <Link to="/about" className="text-gray-400 hover:text-white transition-colors">
                关于我们
              </Link>
              <Link to="/contact" className="text-gray-400 hover:text-white transition-colors">
                联系我们
              </Link>
              <Link to="/privacy" className="text-gray-400 hover:text-white transition-colors">
                隐私政策
              </Link>
            </div>
            <div className="mt-8 pt-8 border-t border-gray-800">
              <p className="text-gray-400">
                © 2024 期货数据可视化平台. 保留所有权利.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;