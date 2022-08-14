import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5, 6, 7, 8 ]
y = [1776.1, 1717.8, 1713.7, 1747.7, 1746.3, 2013.4, 4638.8, 32343.5]

plt.ylabel(
    'Speed in milliseconds'
)
plt.xlabel('Step')
plt.title('File transfer speed')
plt.plot(x, y)
plt.savefig('/content/speed')