-- Grant permissions for anon and authenticated roles

-- Grant permissions for users table
GRANT SELECT, INSERT, UPDATE ON users TO authenticated;
GRANT SELECT ON users TO anon;

-- Grant permissions for datasets table
GRANT ALL PRIVILEGES ON datasets TO authenticated;
GRANT SELECT ON datasets TO anon;

-- Grant permissions for kline_data table
GRANT ALL PRIVILEGES ON kline_data TO authenticated;
GRANT SELECT ON kline_data TO anon;

-- Grant permissions for chart_configs table
GRANT ALL PRIVILEGES ON chart_configs TO authenticated;
GRANT SELECT ON chart_configs TO anon;

-- Enable RLS policies for better security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE datasets ENABLE ROW LEVEL SECURITY;
ALTER TABLE kline_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE chart_configs ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
-- Users can only see and modify their own data
CREATE POLICY "Users can view own profile" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE USING (auth.uid() = id);

-- Datasets policies
CREATE POLICY "Users can view own datasets" ON datasets
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create datasets" ON datasets
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own datasets" ON datasets
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own datasets" ON datasets
  FOR DELETE USING (auth.uid() = user_id);

-- Kline data policies
CREATE POLICY "Users can view kline data for own datasets" ON kline_data
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM datasets 
      WHERE datasets.id = kline_data.dataset_id 
      AND datasets.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert kline data for own datasets" ON kline_data
  FOR INSERT WITH CHECK (
    EXISTS (
      SELECT 1 FROM datasets 
      WHERE datasets.id = kline_data.dataset_id 
      AND datasets.user_id = auth.uid()
    )
  );

-- Chart configs policies
CREATE POLICY "Users can view own chart configs" ON chart_configs
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create chart configs" ON chart_configs
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own chart configs" ON chart_configs
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own chart configs" ON chart_configs
  FOR DELETE USING (auth.uid() = user_id);