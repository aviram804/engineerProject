import numpy as np
from Chunks import Chunk


class ChunksBase:

    def __init__(self, time_to_throw):
        """
        init of database that holds all chuncks
        """
        self.throw_time = time_to_throw
        self.chunks = np.zeros((0,))

    def add(self, chunks):
        """
        adding a new chunk to the chunksbase
        :param chunks: np array of Chunk objects
        :return:
        """
        self.chunks = np.append(self.chunks, chunks)
        is_anomaly = self.detect_anomaly()
        self.delete_old()
        return is_anomaly

    def detect_anomaly(self):
        """
        try to detect anomaly behavior of a packet that coming from some ip
        :return:
        """
        prices = [x.size for x in self.chunks if x is not None]
        mean_size = np.mean(prices)
        var_size = np.var(prices)

        mean_test = 0
        var_test = 0
        for chunk in self.chunks:
            mean_test += chunk.size
            var_test += chunk.size**2

        mean = mean_test / len(self.chunks)
        var = var_test / len(self.chunks) - mean**2

        print("my mean is ", mean)
        print("their mean is ", mean_size)

        print("my var is ", var)
        print("their var is ", var_size)
        return True

    def should_throw(self, idx):
        """
        should chunks[idx be deleted out of the data base
        :param idx: int index to throw
        :return: boolean
        """
        return self.chunks[-1].time - self.chunks[idx].time > self.throw_time

    def delete_old(self):
        """
        delete old data chunks
        :return:
        """
        old_idx = 0
        while self.should_throw(old_idx):
            old_idx += 1
        self.chunks = np.delete(self.chunks, np.arange(old_idx))


chks = np.array([Chunk(40, "gg", "gg", 0), Chunk(32, "gg", "gg", 0), Chunk(35, "gg", "gg", 0), Chunk(56, "gg", "gg", 0),
                 Chunk(45, "gg", "gg", 0), Chunk(48, "gg", "gg", 0), Chunk(39, "gg", "gg", 0), Chunk(31, "gg", "gg", 0),
                 Chunk(35, "gg", "gg", 0), Chunk(46, "gg", "gg", 0), Chunk(40, "gg", "gg", 0), Chunk(33, "gg", "gg", 0)])

bas = ChunksBase(10)
bas.add(chks)
bas.detect_anomaly()