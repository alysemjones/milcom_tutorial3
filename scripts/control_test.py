import flowgraphs.control_test as test
import matplotlib.pyplot as plt
import numpy as np

data = []
total_data = []
tb = test.control_test()
for i in range(2):
    data = []
    tb.run()
    data = tb.blocks_vector_sink_x_0.data()
    #data = tb.data_out.level()
    total_data.extend(data)

t = np.linspace(0,0.002,32)
#print(np.linspace(0,0.002,32))
#print(len(total_data))
plt.plot(t,np.array(total_data).real)
plt.show()
