-- 创建用户扩展信息表
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    username VARCHAR(50) UNIQUE,
    full_name VARCHAR(100),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id)
);

-- 创建数据集表
CREATE TABLE IF NOT EXISTS datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_name VARCHAR(255),
    file_size INTEGER,
    file_type VARCHAR(50),
    upload_path TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建K线数据表
CREATE TABLE IF NOT EXISTS kline_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,
    time_stamp TIMESTAMPTZ NOT NULL,
    open_price DECIMAL(15, 6) NOT NULL,
    high_price DECIMAL(15, 6) NOT NULL,
    low_price DECIMAL(15, 6) NOT NULL,
    close_price DECIMAL(15, 6) NOT NULL,
    volume DECIMAL(20, 6) DEFAULT 0,
    symbol VARCHAR(20),
    interval_type VARCHAR(10) DEFAULT '1m',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建图表配置表
CREATE TABLE IF NOT EXISTS chart_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    config_data JSONB NOT NULL,
    chart_type VARCHAR(50) DEFAULT 'candlestick',
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_datasets_user_id ON datasets(user_id);
CREATE INDEX IF NOT EXISTS idx_datasets_created_at ON datasets(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_kline_data_dataset_id ON kline_data(dataset_id);
CREATE INDEX IF NOT EXISTS idx_kline_data_time_stamp ON kline_data(time_stamp);
CREATE INDEX IF NOT EXISTS idx_kline_data_symbol ON kline_data(symbol);
CREATE INDEX IF NOT EXISTS idx_chart_configs_user_id ON chart_configs(user_id);
CREATE INDEX IF NOT EXISTS idx_chart_configs_dataset_id ON chart_configs(dataset_id);

-- 启用行级安全策略 (RLS)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE datasets ENABLE ROW LEVEL SECURITY;
ALTER TABLE kline_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE chart_configs ENABLE ROW LEVEL SECURITY;

-- 用户扩展信息表的RLS策略
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON user_profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (auth.uid() = user_id);

-- 数据集表的RLS策略
CREATE POLICY "Users can view own datasets" ON datasets
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own datasets" ON datasets
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own datasets" ON datasets
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own datasets" ON datasets
    FOR DELETE USING (auth.uid() = user_id);

-- K线数据表的RLS策略
CREATE POLICY "Users can view kline data of own datasets" ON kline_data
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM datasets 
            WHERE datasets.id = kline_data.dataset_id 
            AND datasets.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert kline data to own datasets" ON kline_data
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM datasets 
            WHERE datasets.id = kline_data.dataset_id 
            AND datasets.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update kline data of own datasets" ON kline_data
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM datasets 
            WHERE datasets.id = kline_data.dataset_id 
            AND datasets.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete kline data of own datasets" ON kline_data
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM datasets 
            WHERE datasets.id = kline_data.dataset_id 
            AND datasets.user_id = auth.uid()
        )
    );

-- 图表配置表的RLS策略
CREATE POLICY "Users can view own chart configs" ON chart_configs
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own chart configs" ON chart_configs
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own chart configs" ON chart_configs
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own chart configs" ON chart_configs
    FOR DELETE USING (auth.uid() = user_id);