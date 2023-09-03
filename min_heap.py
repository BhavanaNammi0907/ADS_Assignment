class MinHeap:
    def __init__(self):
        self.heap_list = [0]
        self.curr_size = 0
    def insert(self, ele):
        self.heap_list.append(ele)
        self.curr_size += 1
        self.heapify_up(self.curr_size)
    def heapify_up(self, p):
        while (p // 2) > 0:
            if self.heap_list[p].ride.less_than(self.heap_list[p // 2].ride):
                self.swap(p, (p // 2))
            else:
                break
            p = p // 2
    def swap(self, ind1, ind2):
        temp = self.heap_list[ind1]
        self.heap_list[ind1] = self.heap_list[ind2]
        self.heap_list[ind2] = temp
        self.heap_list[ind1].min_heap_index = ind1
        self.heap_list[ind2].min_heap_index = ind2
    def heapify_down(self, p):
        while (p * 2) <= self.curr_size:
            ind = self.get_min_child_index(p)
            if not self.heap_list[p].ride.less_than(self.heap_list[ind].ride):
                self.swap(p, ind)
            p = ind
    def get_min_child_index(self, p):
        if (p * 2) + 1 > self.curr_size:
            return p * 2
        else:
            if self.heap_list[p * 2].ride.less_than(self.heap_list[(p * 2) + 1].ride):
                return p * 2
            else:
                return (p * 2) + 1
    def update_element(self, p, new_key):
        node = self.heap_list[p]
        node.ride.tripDuration = new_key
        if p == 1:
            self.heapify_down(p)
        elif self.heap_list[p // 2].ride.less_than(self.heap_list[p].ride):
            self.heapify_down(p)
        else:
            self.heapify_up(p)
    def delete_element(self, p):

        self.swap(p, self.curr_size)
        # self.heap_list[1] = self.heap_list[self.curr_size]
        self.curr_size -= 1
        *self.heap_list, _ = self.heap_list

        self.heapify_down(p)
    def pop(self):

        if len(self.heap_list) == 1:
            return 'No Rides Available'

        root = self.heap_list[1]

        self.swap(1, self.curr_size)
        # self.heap_list[1] = self.heap_list[self.curr_size]
        self.curr_size -= 1
        *self.heap_list, _ = self.heap_list

        self.heapify_down(1)

        return root

class MinHeapNode:
    def __init__(self, ride, rbt, min_heap_index):
        self.ride = ride
        self.rbTree = rbt
        self.min_heap_index = min_heap_index
