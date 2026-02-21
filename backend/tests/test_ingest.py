from app.ingestion.csv_parser import parse_csv_bytes


def test_parse_csv_bytes():
    sample = b"Date,Open,High,Low,Close,Volume\n2024-01-01,10,11,9,10.5,1000\n"
    df = parse_csv_bytes(sample)
    assert df.shape[0] == 1
    assert df.loc[0, "close"] == 10.5
