'''
Reference implementation of SDNE

Author: Xuanrong Yao, Daixin Wang

for more detail, refer to the paper:
SDNE : structral deep network embedding
Wang, Daixin and Cui, Peng and Zhu, Wenwu
Knowledge Discovery and Data Mining (KDD), 2016
'''

#!/usr/bin/python2
# -*- coding: utf-8 -*-



from config import Config
from graph import Graph
from sdne import SDNE
import time

if __name__ == "__main__":
    config = Config()
    
    graph_data = Graph(config.file_path, config.ng_sample_ratio)
    config.struct[0] = graph_data.N
    
    model = SDNE(config)    
    model.do_variables_init(config.DBN_init)

    last_Loss = 0
    time_consumed = 0
    epochs = 0
    while (True):
        mini_batch = graph_data.sample(config.batch_size)
        st_time = time.time()
        model.fit(mini_batch)
        time_consumed += time.time() - st_time
        
        if graph_data.is_epoch_end:
            epochs += 1
            loss = 0
            while (True):
                mini_batch = graph_data.sample(config.batch_size)
                loss += model.get_loss(mini_batch)
                if graph_data.is_epoch_end:
                    break
            
            print "Epoch : %d Loss : %.3f, Train time_consumed : %.3fs" % (epochs, loss, time_consumed)
            #TODO
            # if (last_Loss - Loss) < :
                # print "model converge terminating"
        if epochs > config.epochs_limit:
            print "exceed epochs limit terminating"
        
    
    ##embedding = model.getEmbedding(graph_data.get_all())
    ##sio.savemat('embedding.mat',{'embedding':embedding})
