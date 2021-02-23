
This project made for counting volatility of securities.
I used simple formula fo this:
deviation as a percentage of the half-sum of extreme price values for a trading session.
Example:
half_sum = (12 + 11) / 2 = 11.5
volatility = ((12 - 11) / half_sum) * 100 = 8.7%
etc.
There are three scripts using regular countings, threads and processes.