import sys

# to import required functions from other files into our file
from ride_model import Ride
from min_heap import MinHeap
from min_heap import MinHeapNode
from reb_black_tree import RedBlackTree, RBTNode

# for insert command
def insert_ride(ride, heap, rbtree):
    if rbtree.get_ride(ride.rideNumber) is not None:
        write_to_output(None, "Duplicate RideNumber", False)
        sys.exit(0)
        return
    rbt_node = RBTNode(None, None)
    min_heap_node = MinHeapNode(ride, rbt_node, heap.curr_size + 1)
    heap.insert(min_heap_node)
    rbtree.insert(ride, min_heap_node)

# to update a ride
def update_ride(rideNumber, new_duration, heap, rbtree):
    rbt_node = rbtree.get_ride(rideNumber)
    if rbt_node is None:
        print("")
    elif new_duration <= rbt_node.ride.tripDuration:
        heap.update_element(rbt_node.min_heap_node.min_heap_index, new_duration)
    elif rbt_node.ride.tripDuration < new_duration <= (2 * rbt_node.ride.tripDuration):
        cancel_ride(rbt_node.ride.rideNumber, heap, rbtree)
        insert_ride(Ride(rbt_node.ride.rideNumber, rbt_node.ride.rideCost + 10, new_duration), heap, rbtree)
    else:
        cancel_ride(rbt_node.ride.rideNumber, heap, rbtree)
# to get the next ride
def get_next_ride(heap, rbtree):
    if heap.curr_size != 0:
        popped_node = heap.pop()
        rbtree.delete_node(popped_node.ride.rideNumber)
        write_to_output(popped_node.ride, "", False)
    else:
        write_to_output(None, "No active ride requests", False)
# to print the triplet
def print_ride(rideNumber, rbtree):
    res = rbtree.get_ride(rideNumber)
    if res is None:
        write_to_output(Ride(0, 0, 0), "", False)
    else:
        write_to_output(res.ride, "", False)

# to print all the triplets
def print_rides(l, h, rbtree):
    list = rbtree.get_rides_in_range(l, h)
    write_to_output(list, "", True)

# to cancel a ride
def cancel_ride(ride_number, heap, rbtree):
    heap_node = rbtree.delete_node(ride_number)
    if heap_node is not None:
        heap.delete_element(heap_node.min_heap_index)

# to write the output to the output_file
def write_to_output(ride, mssg, list):
    file = open("output_file.txt", "a")
    if ride is None:
        file.write(mssg + "\n")
    else:
        mssg = ""
        if not list:
            mssg += ("(" + str(ride.rideNumber) + "," + str(ride.rideCost) + "," + str(ride.tripDuration) + ")\n")
        else:
            if len(ride) == 0:
                mssg += "(0,0,0)\n"
            for i in range(len(ride)):
                if i != len(ride) - 1:
                    mssg = mssg + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + "),")
                else:
                    mssg = mssg + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + ")\n")

        file.write(mssg)
    file.close()

if __name__ == "__main__":
    heap = MinHeap()
    rbtree = RedBlackTree()
    file = open("output_file.txt", "w")
    file.close()
    file = open("input.txt", "r")
    for s in file.readlines():
        array_toStore = []
        for num in s[s.index("(") + 1:s.index(")")].split(","):
            if num != '':
                array_toStore.append(int(num))
        if "Insert" in s:
            insert_ride(Ride(array_toStore[0], array_toStore[1], array_toStore[2]), heap, rbtree)
        elif "Print" in s:
            if len(array_toStore) == 1:
                print_ride(array_toStore[0], rbtree)
            elif len(array_toStore) == 2:
                print_rides(array_toStore[0], array_toStore[1], rbtree)
        elif "UpdateTrip" in s:
            update_ride(array_toStore[0], array_toStore[1], heap, rbtree)
        elif "GetNextRide" in s:
            get_next_ride(heap, rbtree)
        elif "CancelRide" in s:
            cancel_ride(array_toStore[0], heap, rbtree)

