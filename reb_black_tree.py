class RBTNode:
    def __init__(self, ride, min_heap_node):
        self.ride = ride
        self.parent = None  # parent node
        self.left = None  # left node
        self.right = None  # right node
        self.color = 1  # 1=red , 0 = black
        self.min_heap_node = min_heap_node
class RedBlackTree:
    def __init__(self):
        self.null_node = RBTNode(None, None)
        self.null_node.left = None
        self.null_node.right = None
        self.null_node.color = 0
        self.root = self.null_node
    # To retrieve the ride with the rideNumber equal to the key
    def get_ride(self, key):
        temp = self.root

        # Iterating through the tree to find the node with rideNumber equal to the key
        while temp != self.null_node:
            if temp.ride.rideNumber == key:
                return temp
            if temp.ride.rideNumber < key:
                temp = temp.right
            else:
                temp = temp.left

        return None
    # Balancing the tree after deletion
    def balance_tree_after_delete(self, node):
        #
        while node != self.root and node.color == 0:
            if node == node.parent.right:
                parent_sibling = node.parent.left
                if parent_sibling.color != 0:
                    node.parent.color = 1
                    parent_sibling.color = 0
                    self.r_rotation(node.parent)
                    parent_sibling = node.parent.left

                if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                    parent_sibling.color = 1
                    node = node.parent
                else:
                    if parent_sibling.left.color != 1:
                        parent_sibling.right.color = 0
                        parent_sibling.color = 1
                        self.l_rotation(parent_sibling)
                        parent_sibling = node.parent.left

                    parent_sibling.color = node.parent.color
                    node.parent.color = 0
                    parent_sibling.left.color = 0
                    self.r_rotation(node.parent)
                    node = self.root
            else:
                parent_sibling = node.parent.right
                if parent_sibling.color != 0:
                    node.parent.color = 1
                    parent_sibling.color = 0
                    self.l_rotation(node.parent)
                    parent_sibling = node.parent.right

                if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                    parent_sibling.color = 1
                    node = node.parent
                else:
                    if parent_sibling.right.color != 1:
                        parent_sibling.left.color = 0
                        parent_sibling.color = 1
                        self.r_rotation(parent_sibling)
                        parent_sibling = node.parent.right

                    parent_sibling.color = node.parent.color
                    node.parent.color = 0
                    parent_sibling.right.color = 0
                    self.l_rotation(node.parent)
                    node = self.root

        node.color = 0
    def __rb_transplant(self, node, child_node):
        if node.parent is None:
            self.root = child_node
        elif node == node.parent.right:
            node.parent.right = child_node
        else:
            node.parent.left = child_node
        child_node.parent = node.parent
    def delete_node_helper(self, node, key):
        delete_node = self.null_node
        while node != self.null_node:
            if node.ride.rideNumber == key:
                delete_node = node
            if node.ride.rideNumber >= key:
                node = node.left
            else:
                node = node.right

        if delete_node == self.null_node:
            return
        heap_node = delete_node.min_heap_node
        y = delete_node
        y_original_color = y.color
        if delete_node.left == self.null_node:
            x = delete_node.right
            self.__rb_transplant(delete_node, delete_node.right)
        elif (delete_node.right == self.null_node):
            x = delete_node.left
            self.__rb_transplant(delete_node, delete_node.left)
        else:
            y = self.minimum(delete_node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == delete_node:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = delete_node.right
                y.right.parent = y

            self.__rb_transplant(delete_node, y)
            y.left = delete_node.left
            y.left.parent = y
            y.color = delete_node.color
        if y_original_color == 0:
            self.balance_tree_after_delete(x)

        return heap_node
    def balance_after_insert(self, curr_node):
        while curr_node.parent.color == 1:
            if curr_node.parent == curr_node.parent.parent.left:
                parent_sibling = curr_node.parent.parent.right

                if parent_sibling.color == 0:
                    if curr_node == curr_node.parent.right:
                        curr_node = curr_node.parent
                        self.l_rotation(curr_node)
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    self.r_rotation(curr_node.parent.parent)
                else:
                    parent_sibling.color = 0
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    curr_node = curr_node.parent.parent

            else:
                parent_sibling = curr_node.parent.parent.left
                if parent_sibling.color == 0:
                    if curr_node == curr_node.parent.left:
                        curr_node = curr_node.parent
                        self.r_rotation(curr_node)
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    self.l_rotation(curr_node.parent.parent)
                else:
                    parent_sibling.color = 0
                    curr_node.parent.color = 0
                    curr_node.parent.parent.color = 1
                    curr_node = curr_node.parent.parent

            if curr_node == self.root:
                break
        self.root.color = 0
    def find_ride_in_range(self, node, low, high, res):
        if node == self.null_node:
            return

        if low < node.ride.rideNumber:
            self.find_ride_in_range(node.left, low, high, res)
        if low <= node.ride.rideNumber <= high:
            res.append(node.ride)
        self.find_ride_in_range(node.right, low, high, res)
    def get_rides_in_range(self, low, high):
        res = []
        self.find_ride_in_range(self.root, low, high, res)
        return res
    def minimum(self, node):
        while node.left != self.null_node:
            node = node.left
        return node
    def l_rotation(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.null_node:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    def r_rotation(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.null_node:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    def insert(self, ride, min_heap):
        node = RBTNode(ride, min_heap)
        node.parent = None
        node.left = self.null_node
        node.right = self.null_node
        node.color = 1

        insertion_node = None
        temp_node = self.root

        while temp_node != self.null_node:
            insertion_node = temp_node
            if node.ride.rideNumber < temp_node.ride.rideNumber:
                temp_node = temp_node.left
            else:
                temp_node = temp_node.right

        node.parent = insertion_node
        if insertion_node is None:
            self.root = node
        elif node.ride.rideNumber > insertion_node.ride.rideNumber:
            insertion_node.right = node
        else:
            insertion_node.left = node

        if node.parent is None:
            node.color = 0
            return

        if node.parent.parent is None:
            return

        self.balance_after_insert(node)
    def delete_node(self, rideNumber):
        return self.delete_node_helper(self.root, rideNumber)
