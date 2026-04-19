INSERT INTO investments (fund_name, risk_level, returns, min_investment, category)
VALUES
    ('HDFC Corporate Bond Fund', 'low', 7.2, 5000, 'bonds'),
    ('ICICI Prudential Savings Fund', 'low', 6.8, 1000, 'mutual_fund'),
    ('SBI Magnum Gilt Fund', 'low', 7.0, 5000, 'bonds'),
    ('Axis Bluechip Fund', 'medium', 11.5, 5000, 'mutual_fund'),
    ('Mirae Asset Large Cap Fund', 'medium', 12.1, 5000, 'SIP'),
    ('UTI Flexi Cap Fund', 'medium', 13.0, 1000, 'mutual_fund'),
    ('Parag Parikh Flexi Cap Fund', 'high', 15.8, 1000, 'stocks'),
    ('Nippon India Small Cap Fund', 'high', 18.2, 5000, 'SIP'),
    ('Kotak Emerging Equity Fund', 'high', 16.9, 5000, 'stocks'),
    ('Aditya Birla Sun Life Frontline Equity Fund', 'medium', 11.9, 1000, 'mutual_fund')
ON CONFLICT (fund_name) DO NOTHING;
