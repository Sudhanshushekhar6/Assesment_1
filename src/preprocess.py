# src/preprocess.py
import pandas as pd
import numpy as np

def read_csv_safe(path, channel_name=None):
    """
    Read CSV safely:
    - Handles utf-8 and latin-1 encodings
    - Strips extra spaces from columns and data
    - Parses 'date' in multiple formats (dd-mm-yyyy, yyyy-mm-dd)
    - Normalizes column names
    - Adds 'channel' column if provided
    """
    try:
        df = pd.read_csv(path, encoding="utf-8", sep=None, engine="python")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1", sep=None, engine="python")

    # Strip column names
    df.columns = df.columns.str.strip()

    # Normalize column names
    df = df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"))
    df = df.rename(columns={
        "impression": "impressions",
        "attributed_revenue": "attributed_revenue",  # keep consistent
        "attributed revenue": "attributed_revenue",
        "#_of_orders": "orders",
        "#_of_new_orders": "new_orders",
        "cogs": "cost_of_goods_sold"
    })

    # Strip whitespace in string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Parse dates - try multiple formats
    if "date" in df.columns:
        # Try different date formats
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        if df["date"].isna().all():
            # Try specific formats
            try:
                df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
            except:
                try:
                    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
                except:
                    pass
        
        if df["date"].isna().all():
            raise ValueError(f"All dates in {path} could not be parsed. Check your file!")

    # Add channel column
    if channel_name:
        df["channel"] = channel_name.lower()

    return df

def load_and_merge(fb_path, gg_path, tt_path, biz_path, from_upload=False):
    """Load marketing (FB, Google, TikTok) and business CSVs and merge."""
    fb = read_csv_safe(fb_path, "facebook")
    gg = read_csv_safe(gg_path, "google")
    tt = read_csv_safe(tt_path, "tiktok")
    biz = read_csv_safe(biz_path)

    # Combine marketing data
    mkt = pd.concat([fb, gg, tt], ignore_index=True)
    return mkt, biz

def aggregate_daily(mkt, biz):
    """Aggregate marketing and business data by day with enhanced metrics."""
    # Ensure dates are properly formatted
    mkt["date"] = pd.to_datetime(mkt["date"])
    biz["date"] = pd.to_datetime(biz["date"])
    
    # Aggregate marketing data by date
    df = mkt.groupby("date", as_index=False).agg({
        "spend": "sum",
        "impressions": "sum", 
        "clicks": "sum",
        "attributed_revenue": "sum",
        "channel": lambda x: ", ".join(sorted(x.unique())),  # List channels active on each day
        "state": lambda x: ", ".join(sorted(x.unique())),    # List states active on each day
        "tactic": lambda x: ", ".join(sorted(x.unique())),  # List tactics active on each day
        "campaign": "nunique"  # Count unique campaigns
    })
    
    # Merge with business data - use outer join to include all dates
    df = df.merge(biz, on="date", how="outer")
    
    # Fill missing values with 0 for numeric columns
    numeric_cols = ["spend", "impressions", "clicks", "attributed_revenue", "orders", "new_orders", "new_customers", "total_revenue", "gross_profit", "cost_of_goods_sold"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    # Add derived metrics
    df["ctr"] = df["clicks"] / df["impressions"].replace(0, np.nan)
    df["cpc"] = df["spend"] / df["clicks"].replace(0, np.nan)
    df["cpm"] = df["spend"] / (df["impressions"] / 1000).replace(0, np.nan)
    df["roas"] = df["attributed_revenue"] / df["spend"].replace(0, np.nan)
    df["conversion_rate"] = df["orders"] / df["clicks"].replace(0, np.nan)
    df["revenue_per_order"] = df["total_revenue"] / df["orders"].replace(0, np.nan)
    df["profit_margin"] = df["gross_profit"] / df["total_revenue"].replace(0, np.nan)
    
    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)
    
    return df

def campaign_table(df):
    """Return enhanced campaign-level summary table."""
    campaign_data = (
        df.groupby(["campaign", "channel", "tactic", "state"], as_index=False)
          .agg({
              "spend": "sum",
              "impressions": "sum",
              "clicks": "sum",
              "attributed_revenue": "sum",
              "orders": "sum",
              "total_revenue": "sum",
              "gross_profit": "sum"
          })
    )
    
    # Add calculated metrics
    campaign_data["roas"] = campaign_data["attributed_revenue"] / campaign_data["spend"].replace(0, np.nan)
    campaign_data["ctr"] = campaign_data["clicks"] / campaign_data["impressions"].replace(0, np.nan)
    campaign_data["cpc"] = campaign_data["spend"] / campaign_data["clicks"].replace(0, np.nan)
    campaign_data["cpm"] = campaign_data["spend"] / (campaign_data["impressions"] / 1000).replace(0, np.nan)
    campaign_data["conversion_rate"] = campaign_data["orders"] / campaign_data["clicks"].replace(0, np.nan)
    campaign_data["revenue_per_order"] = campaign_data["total_revenue"] / campaign_data["orders"].replace(0, np.nan)
    campaign_data["profit_margin"] = campaign_data["gross_profit"] / campaign_data["total_revenue"].replace(0, np.nan)
    
    return campaign_data.sort_values("spend", ascending=False)

def funnel_agg(df):
    """Create enhanced funnel summary (Impressions -> Clicks -> Orders -> Revenue)."""
    funnel = pd.DataFrame({
        "stage": ["Impressions", "Clicks", "Orders", "Revenue"],
        "value": [
            df.get("impressions", pd.Series(dtype=float)).sum(),
            df.get("clicks", pd.Series(dtype=float)).sum(),
            df.get("orders", pd.Series(dtype=float)).sum() if "orders" in df.columns else 0,
            df.get("attributed_revenue", pd.Series(dtype=float)).sum()
        ]
    })
    funnel["pct"] = (
        (funnel["value"] / funnel["value"].max() * 100)
        .round(1).astype(str) + "%"
    )
    
    # Add conversion rates between stages
    funnel["conversion_rate"] = [
        100.0,  # Impressions to clicks
        (funnel.loc[1, "value"] / funnel.loc[0, "value"] * 100) if funnel.loc[0, "value"] > 0 else 0,
        (funnel.loc[2, "value"] / funnel.loc[1, "value"] * 100) if funnel.loc[1, "value"] > 0 else 0,
        (funnel.loc[3, "value"] / funnel.loc[2, "value"] * 100) if funnel.loc[2, "value"] > 0 else 0
    ]
    
    return funnel

def channel_performance(df):
    """Return detailed channel performance analysis."""
    channel_data = (
        df.groupby("channel", as_index=False)
          .agg({
              "spend": "sum",
              "impressions": "sum",
              "clicks": "sum",
              "attributed_revenue": "sum",
              "orders": "sum",
              "total_revenue": "sum",
              "gross_profit": "sum",
              "new_customers": "sum"
          })
    )
    
    # Add calculated metrics
    channel_data["roas"] = channel_data["attributed_revenue"] / channel_data["spend"].replace(0, np.nan)
    channel_data["ctr"] = channel_data["clicks"] / channel_data["impressions"].replace(0, np.nan)
    channel_data["cpc"] = channel_data["spend"] / channel_data["clicks"].replace(0, np.nan)
    channel_data["cpm"] = channel_data["spend"] / (channel_data["impressions"] / 1000).replace(0, np.nan)
    channel_data["conversion_rate"] = channel_data["orders"] / channel_data["clicks"].replace(0, np.nan)
    channel_data["cac"] = channel_data["spend"] / channel_data["new_customers"].replace(0, np.nan)
    channel_data["ltv"] = channel_data["total_revenue"] / channel_data["new_customers"].replace(0, np.nan)
    channel_data["ltv_cac_ratio"] = channel_data["ltv"] / channel_data["cac"].replace(0, np.nan)
    
    return channel_data.sort_values("spend", ascending=False)

def state_performance(df):
    """Return state-level performance analysis."""
    if "state" not in df.columns:
        return pd.DataFrame()
    
    state_data = (
        df.groupby("state", as_index=False)
          .agg({
              "spend": "sum",
              "impressions": "sum",
              "clicks": "sum",
              "attributed_revenue": "sum",
              "orders": "sum",
              "total_revenue": "sum",
              "gross_profit": "sum",
              "new_customers": "sum"
          })
    )
    
    # Add calculated metrics
    state_data["roas"] = state_data["attributed_revenue"] / state_data["spend"].replace(0, np.nan)
    state_data["ctr"] = state_data["clicks"] / state_data["impressions"].replace(0, np.nan)
    state_data["cpc"] = state_data["spend"] / state_data["clicks"].replace(0, np.nan)
    state_data["conversion_rate"] = state_data["orders"] / state_data["clicks"].replace(0, np.nan)
    state_data["cac"] = state_data["spend"] / state_data["new_customers"].replace(0, np.nan)
    
    return state_data.sort_values("spend", ascending=False)

def tactic_performance(df):
    """Return tactic-level performance analysis."""
    if "tactic" not in df.columns:
        return pd.DataFrame()
    
    tactic_data = (
        df.groupby("tactic", as_index=False)
          .agg({
              "spend": "sum",
              "impressions": "sum",
              "clicks": "sum",
              "attributed_revenue": "sum",
              "orders": "sum",
              "total_revenue": "sum",
              "gross_profit": "sum",
              "new_customers": "sum"
          })
    )
    
    # Add calculated metrics
    tactic_data["roas"] = tactic_data["attributed_revenue"] / tactic_data["spend"].replace(0, np.nan)
    tactic_data["ctr"] = tactic_data["clicks"] / tactic_data["impressions"].replace(0, np.nan)
    tactic_data["cpc"] = tactic_data["spend"] / tactic_data["clicks"].replace(0, np.nan)
    tactic_data["conversion_rate"] = tactic_data["orders"] / tactic_data["clicks"].replace(0, np.nan)
    tactic_data["cac"] = tactic_data["spend"] / tactic_data["new_customers"].replace(0, np.nan)
    
    return tactic_data.sort_values("spend", ascending=False)

def weekly_trends(df):
    """Return weekly aggregated trends."""
    df_weekly = df.copy()
    df_weekly["week"] = df_weekly["date"].dt.to_period("W")
    
    weekly_data = (
        df_weekly.groupby("week", as_index=False)
          .agg({
              "spend": "sum",
              "impressions": "sum",
              "clicks": "sum",
              "attributed_revenue": "sum",
              "orders": "sum",
              "total_revenue": "sum",
              "gross_profit": "sum",
              "new_customers": "sum"
          })
    )
    
    # Add calculated metrics
    weekly_data["roas"] = weekly_data["attributed_revenue"] / weekly_data["spend"].replace(0, np.nan)
    weekly_data["ctr"] = weekly_data["clicks"] / weekly_data["impressions"].replace(0, np.nan)
    weekly_data["conversion_rate"] = weekly_data["orders"] / weekly_data["clicks"].replace(0, np.nan)
    
    return weekly_data.sort_values("week")
