import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set the style of the plot
# plt.style.use('seaborn-darkgrid')

def animate(i):
    # Fetch the latest data for the S&P 500 index
    data = yf.download(tickers='^GSPC', period='1d', interval='1m')
    
    # Clear the current plot
    plt.cla()
    
    # Plot the closing prices
    plt.plot(data.index, data['Close'], label='S&P 500')
    
    # Formatting the plot
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('S&P 500 Index Real-Time Price')
    plt.legend(loc='upper left')
    plt.tight_layout()

# Create the figure and animate
fig = plt.figure()
ani = FuncAnimation(fig, animate, interval=60000)  # Update every 60 seconds

# Display the plot
plt.show()