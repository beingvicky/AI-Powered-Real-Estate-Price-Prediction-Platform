from train_model import generate_dataset


def test_dataset_includes_mysuru_and_market_reference_rates():
    df = generate_dataset(100)
    assert 'Mysuru' in set(df['location'])
    assert 'Bengaluru' in set(df['location'])
    mysuru_rows = df[df['location'] == 'Mysuru']
    assert not mysuru_rows.empty
    assert mysuru_rows['price_lakhs'].max() > 80
