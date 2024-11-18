import pandas as pd
from datetime import datetime, timedelta

# Setting up pandas display options
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', 100)

def search_keyword(df, keyword):    
    # Search for the keyword in the 'title' column    
    matched_rows = df[df['公告标题'].str.contains(keyword, case=False)]    
    return matched_rows

def get_notice_data(symbol="全部", start_date=None, end_date=None):
    try:    
        import akshare as ak
        # 默认时间范围为最近一周
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y%m%d')
        
        # 获取公告数据
        df = ak.stock_notice_report(symbol=symbol, date=start_date)
        
        # 如果有多个日期，循环获取数据并合并
        current_date = datetime.strptime(start_date, '%Y%m%d')
        end_date_dt = datetime.strptime(end_date, '%Y%m%d')
        
        while current_date <= end_date_dt:
            date_str = current_date.strftime('%Y%m%d')
            print(f"Fetching data for date: {date_str}")
            daily_df = ak.stock_notice_report(symbol=symbol, date=date_str)
            df = pd.concat([df, daily_df], ignore_index=True)
            current_date += timedelta(days=1)
        
        return df
    
    except ImportError:    
        print("akshare is not available")
        return None

# Main execution
start_date = "20241115"  # 设置开始日期
end_date = "20241118"    # 设置结束日期
df = get_notice_data(symbol="全部", start_date=start_date, end_date=end_date)

if df is not None:
    # Save to Excel
    spath = f"./{start_date}_{end_date}_公告.xlsx"
    df.to_excel(spath, engine='xlsxwriter', index=False)
    print(f"Data saved to {spath}")

    # Search for a keyword
    # keyword = "变更公司名称"
    keyword = "证券简称"
    # keyword = "中标"
    result = search_keyword(df, keyword)
    
    print(f"\nRows containing the keyword '{keyword}':")
    print(result[['代码', '名称', '公告标题', '网址']])
