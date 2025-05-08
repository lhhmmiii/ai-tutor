def delete_meaningless_columns(df):
    columns = df.columns
    for column in columns:
        if df[column].isna().all():
            df = df.drop(column, axis=1)
    return df


def delete_meaningless_rows(df):
    df = df.dropna(how="all")
    return df
