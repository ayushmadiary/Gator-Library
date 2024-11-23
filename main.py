# Import necessary modules
import time
import sys

# Define a class for Red-Black Tree nodes
class RedBlackNode:
    def __init__(self, key, value): # Initialize a node with key, value, color, and pointers to left, right children, and parent
        self.key = key
        self.value = value
        self.node_color = "RED"  # New nodes are initially set to RED to maintain Red-Black Tree properties.
        self.left_child = None   # Pointer to the left child node.
        self.right_child = None  # Pointer to the right child node.
        self.parent = None

# Define a class for Red-Black Trees
class RedBlackTree:
    def __init__(self): # Initialize a Red-Black Tree with a nil node, root, and color flip count
        self.nil_node = RedBlackNode(None, None)
        self.nil_node.node_color = "BLACK"
        self.root = self.nil_node
        self.color_flip_count = 0

# Perform a left rotation operation to maintain Red-Black Tree properties
    def left_rotate(self, p):
        q = p.right_child
        p.right_child = q.left_child
        if q.left_child != self.nil_node:
            q.left_child.parent = p
        q.parent = p.parent
        if p.parent == self.nil_node:
            self.root = q
        elif p == p.parent.left_child:
            p.parent.left_child = q
        else:
            p.parent.right_child = q
        q.left_child = p
        p.parent = q

# Perform a right rotation operation to maintain Red-Black Tree properties
    def right_rotate(self, q):
        p = q.left_child
        q.left_child = p.right_child
        if p.right_child != self.nil_node:
            p.right_child.parent = q
        p.parent = q.parent
        if q.parent == self.nil_node:
            self.root = p
        elif q == q.parent.left_child:
            q.parent.left_child = p
        else:
            q.parent.right_child = p
        p.right_child = q
        q.parent = p

 # Insert a new node with key and value into the Red-Black Tree
    def insert(self, key, value):
        new_node = RedBlackNode(key, value)
        q = self.nil_node
        p = self.root
        while p != self.nil_node:
            q = p
            if new_node.key < p.key:
                p = p.left_child
            else:
                p = p.right_child
        new_node.parent = q
        if q == self.nil_node:
            self.root = new_node
        elif new_node.key < q.key:
            q.left_child = new_node
        else:
            q.right_child = new_node
        new_node.left_child = self.nil_node
        new_node.right_child = self.nil_node
        self.insert_fixup(new_node)

# Fix any Red-Black Tree property violations after insertion
    def insert_fixup(self, q):
        while q.parent.node_color == "RED":
             # If the parent is the left child of its parent.
            if q.parent == q.parent.parent.left_child:
                 # Set 'p' as the sibling of the parent.
                p = q.parent.parent.right_child
                # If the sibling is also RED, perform color adjustments to restore the properties.
                if p.node_color == "RED":
                    q.parent.node_color = "BLACK"
                    p.node_color = "BLACK"
                    q.parent.parent.node_color = "RED"
                    q = q.parent.parent
                    self.color_flip_count += 3 # Increase the color flip count.
                else:
                    # If the current node is a right child, perform a left rotation.
                    if q == q.parent.right_child:
                        q = q.parent
                        self.left_rotate(q)
                        # Adjust colors and perform a right rotation to restore properties.
                    q.parent.node_color = "BLACK"
                    q.parent.parent.node_color = "RED"
                    self.right_rotate(q.parent.parent)
                    # Increase color flip count if the parent's parent is not the nil node.
                    if q.parent.parent != self.nil_node:
                        self.color_flip_count += 2
            else:
                 # If the parent is the right child of its parent.
                p = q.parent.parent.left_child
                if p.node_color == "RED":
                    q.parent.node_color = "BLACK"
                    p.node_color = "BLACK"
                    q.parent.parent.node_color = "RED"
                    q = q.parent.parent
                    self.color_flip_count += 3
                else:
                    # If the current node is a left child, perform a right rotation.
                    if q == q.parent.left_child:
                        q = q.parent
                        self.right_rotate(q)
                    q.parent.node_color = "BLACK"
                    q.parent.parent.node_color = "RED"
                    self.left_rotate(q.parent.parent)
                    if q.parent.parent != self.nil_node:
                        self.color_flip_count += 2
                        # Set the color of the root to BLACK to maintain Red-Black Tree properties.
        self.root.node_color = "BLACK"

# Transplant a subtree in the Red-Black Tree
    def transplant(self, u, v):
        if u.parent == self.nil_node:
            self.root = v
        elif u == u.parent.left_child:
            u.parent.left_child = v
        else:
            u.parent.right_child = v
        v.parent = u.parent

    # Find the minimum node in a subtree
    def tree_minimum(self, p):
        while p.left_child != self.nil_node:
            p = p.left_child
        return p
    
# Delete a node with the given key from the Red-Black Tree
    def delete(self, key):
        # Search for the node with the specified key.
        q = self.search(key)
        # If the node is not found, print a message and return.
        if q == self.nil_node:
            print(f"Key {key} not found in the tree.")
            return
        # Store the node to be deleted and its original color.
        p = q
        p_original_color = p.node_color
        print(f"Deleting node with key {key}, original color: {p_original_color}")
# Determine the replacement node 'r' based on the number of children of the node to be deleted.
        if q.left_child == self.nil_node:
            r = q.right_child
            self.transplant(q, q.right_child)
        elif q.right_child == self.nil_node:
            r = q.left_child
            self.transplant(q, q.left_child)
        else:  # If the node to be deleted has two children, find its successor 'p'.
            p = self.tree_minimum(q.right_child)
            p_original_color = p.node_color
            r = p.right_child
            # If 'p' is not the right child of 'q', adjust pointers and replace 'q' with 'p'.
            if p.parent != q:
                self.transplant(p, p.right_child)
                p.right_child = q.right_child
                p.right_child.parent = p
            self.transplant(q, p)
            p.left_child = q.left_child
            p.left_child.parent = p
            p.node_color = q.node_color
# Print information about the replacement node.
        print(f"Node replaced, r key: {r.key if r != self.nil_node else 'NIL'}, r color: {r.node_color if r != self.nil_node else 'NIL'}, p_original_color: {p_original_color}")
# If the original color of the replaced node is BLACK, fix any violations in Red-Black Tree properties.
        if p_original_color == "BLACK":
            print("Calling delete_fixup")
            self.delete_fixup(r)
        else:
            print("No need for delete_fixup")
    def delete_fixup(self, p):

    # Fix any violations of Red-Black Tree properties after deletion.
        while p != self.root and p.node_color == "BLACK":
             # Check if 'p' is the left child of its parent.
            if p == p.parent.left_child:
                q = p.parent.right_child
                if q.node_color == "RED":# Case 1: Sibling 'q' is RED.
                    print("Delete Fixup: Case 1 (Left) - Sibling RED")
                    q.node_color = "BLACK"   # Flip colors to balance the tree.
                    self.color_flip_count += 1
                    p.parent.node_color = "RED"
                    self.color_flip_count += 1
                    self.left_rotate(p.parent)  # Rotate left to maintain the Red-Black Tree properties.
                    q = p.parent.right_child
# Case 2: Both children of 'q' are BLACK.
                if q.left_child.node_color == "BLACK" and q.right_child.node_color == "BLACK":
                    print("Delete Fixup: Case 2 (Left) - Both Children BLACK")
                    q.node_color = "RED" # Flip colors and move up the tree.
                    self.color_flip_count += 1
                    p = p.parent
                else:
# Case 3: Right child of 'q' is BLACK.
                    if q.right_child.node_color == "BLACK":
                        print("Delete Fixup: Case 3 (Left) - Right Child BLACK")
                        q.left_child.node_color = "BLACK" # Adjust colors and perform a right rotation.
                        self.color_flip_count += 1
                        q.node_color = "RED"
                        self.color_flip_count += 1
                        self.right_rotate(q)
                        q = p.parent.right_child
# Case 4: Right child of 'q' is RED.
                    print("Delete Fixup: Case 4 (Left) - Right Child RED")
                    q.node_color = p.parent.node_color   # Transfer colors from 'p' to 'q' and perform left rotation.
                    if q.node_color != "BLACK":
                        self.color_flip_count += 1
                    p.parent.node_color = "BLACK"
                    self.color_flip_count += 1
                    q.right_child.node_color = "BLACK"
                    self.color_flip_count += 1
                    self.left_rotate(p.parent)
                    p = self.root
            else: # Similar cases for the right child of 'p'.
                q = p.parent.left_child
 # Case 1: Sibling 'q' is RED.
                if q.node_color == "RED":
                    print("Delete Fixup: Case 1 (Right) - Sibling RED")
                    q.node_color = "BLACK"
                    self.color_flip_count += 1
                    p.parent.node_color = "RED"
                    self.color_flip_count += 1
                    self.right_rotate(p.parent)  # Rotate right to maintain the Red-Black Tree properties.
                    q = p.parent.left_child
# Case 2: Both children of 'q' are BLACK.
                if q.right_child.node_color == "BLACK" and q.left_child.node_color == "BLACK":
                    print("Delete Fixup: Case 2 (Right) - Both Children BLACK")
                    q.node_color = "RED"
                    self.color_flip_count += 1
                    p = p.parent
                else:
 # Case 3: Left child of 'q' is BLACK.
                    if q.left_child.node_color == "BLACK":
                        print("Delete Fixup: Case 3 (Right) - Left Child BLACK")
                        q.right_child.node_color = "BLACK" # Adjust colors and perform a left rotation.
                        self.color_flip_count += 1
                        q.node_color = "RED"
                        self.color_flip_count += 1
                        self.left_rotate(q)
                        q = p.parent.left_child
# Case 4: Left child of 'q' is RED.
                    print("Delete Fixup: Case 4 (Right) - Left Child RED")
                    q.node_color = p.parent.node_color # Transfer colors from 'p' to 'q' and perform right rotation.
                    if q.node_color != "BLACK":
                     self.color_flip_count += 1
                    p.parent.node_color = "BLACK"
                    self.color_flip_count += 1
                    q.left_child.node_color = "BLACK"
                    self.color_flip_count += 1
                    self.right_rotate(p.parent)
                    p = self.root
# Set the color of the final node 'p' to BLACK.
        p.node_color = "BLACK"

    # Search for a node with the given key in the Red-Black Tree
    def search(self, key):
        q = self.root
        while q != self.nil_node and key != q.key:
            if key < q.key:
                q = q.left_child
            else:
                q = q.right_child
        return q

    def preorder_walk(self, q, indent="", last=True):
        # Perform a preorder traversal of the tree, printing each node.
        if q != self.nil_node:
            print(f"{indent}{'|-- ' if last else '|-- '}Key: {q.key}, Color: {q.node_color}, Value: {q.value}")
            indent += "   " if last else "|  "
            self.preorder_walk(q.left_child, indent, False)
            self.preorder_walk(q.right_child, indent, True)

 # Define a class for managing book reservation queues   
class BookReservationQueue:
 # Methods for swapping items, heapifying up, heapifying down, and comparing items
    def __init__(self):
        self.heap = []  # Initialize an empty list to represent the heap.
 # Swap the items at indices i and j in the heap.
    def swap_items(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
# Restore the heap property by moving the item at the given index up the heap.
    def heapify_up(self, index):
        while index > 0: 
            # Calculate the index of the parent node.
            parent_index = (index - 1) // 2
            # Compare the current item with its parent and swap if necessary.
            if self.compare_items(self.heap[index], self.heap[parent_index]) < 0:
                self.swap_items(index, parent_index)
                index = parent_index
            else:
                break
 # Restore the heap property by moving the item at the given index down the heap.
    def heapify_down(self, index):
        # Calculate the indices of the left and right children.
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index
# Compare the current item with its left child, if exists.
        if left_child_index < len(self.heap) and self.compare_items(self.heap[left_child_index], self.heap[smallest]) < 0:
            smallest = left_child_index
# Compare the current item with its right child, if exists.
        if right_child_index < len(self.heap) and self.compare_items(self.heap[right_child_index], self.heap[smallest]) < 0:
            smallest = right_child_index
# Swap with the smallest child if necessary and continue heapifying down.
        if smallest != index:
            self.swap_items(index, smallest)
            self.heapify_down(smallest)
 # Compare two items based on their priority values.
    def compare_items(self, item1, item2):
        if item1[1] < item2[1]:
            return -1
        elif item1[1] > item2[1]:
            return 1
        else:
             # If priority values are equal, compare based on secondary values.
            if item1[2] < item2[2]:
                return -1
            elif item1[2] > item2[2]:
                return 1
            else:
                return 0
 # Method to add a reservation to the queue
    def add_reservation(self, patron_id, priority):
        timestamp = time.time()
        reservation = (patron_id, priority, timestamp)
        self.heap.append(reservation)
        self.heapify_up(len(self.heap) - 1)
 # Method to remove a reservation from the queue
    def remove_reservation(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        last_item = self.heap.pop()
        self.heap[0] = last_item
        self.heapify_down(0)

        return root
    # Method to print the current queue
    def print_queue(self):
        print("Current Queue:", self.heap)

    def remove_specific_patron(self, patron_id):
        # Find the index of the reservation to remove
        index_to_remove = None
        for i, reservation in enumerate(self.heap):
            if reservation[0] == patron_id:
                index_to_remove = i
                break

        # If the patronID is not found, return None
        if index_to_remove is None:
            return None

        # Swap the reservation with the last one and pop it
        self.swap_items(
            index_to_remove, len(self.heap) - 1
        )  # Fixed indentation here
        removed_reservation = self.heap.pop()

        # Heapify up or down based on the new placement of the swapped reservation
        if index_to_remove < len(self.heap):
            parent_index = (index_to_remove - 1) // 2
        if index_to_remove > 0 and self.compare_items(
            self.heap[index_to_remove], self.heap[parent_index]
        ) < 0:
            self.heapify_up(index_to_remove)
        else:
            self.heapify_down(index_to_remove)

        return removed_reservation
   
# Define a class for representing books
class Book:
    def __init__(self, bookID, bookName, authorName, availabilityStatus, borrowedBy=None): # Initialize a Book with book ID, name, author, availability status, and borrower information
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = borrowedBy
        self.reservationHeap = BookReservationQueue()

class GatorLibrary: # Define a class for the Gator Library
    
    def __init__(self):
        self.book_dict = {}
        self.red_black_tree = RedBlackTree()
 # Method to insert a new book into the library
    def InsertBook(self, bookID, bookName, authorName, availabilityStatus, filename, borrowedBy=None):
        if bookID in self.book_dict:
            with open(filename, 'a') as file:
                file.write(f"Book with ID {bookID} already exists.\n")
            # print(f"Book with ID {bookID} already exists.")
            return

        new_book = Book(bookID, bookName, authorName, availabilityStatus, borrowedBy)
        self.book_dict[bookID] = new_book
        self.red_black_tree.insert(bookID, new_book)
  # Method to borrow a book by a patron
    def BorrowBook(self, patronID, bookID, patronPriority, filename):
        if bookID not in self.book_dict:
            with open(filename, 'a') as file:
                file.write(f"Book {bookID} not found in the Library.\n")
            return

        book = self.book_dict[bookID]

        if book.borrowedBy == patronID:
            with open(filename, 'a') as file:
                file.write(f"Patron {patronID} has already borrowed Book {bookID}.\n")
            return

        if book.availabilityStatus:
            book.availabilityStatus = False
            book.borrowedBy = patronID
            with open(filename, 'a') as file:
                file.write(f"Book {bookID} Borrowed by Patron {patronID}\n")
        else:
            if len(book.reservationHeap.heap) < 20:
                book.reservationHeap.add_reservation(patronID, patronPriority)
                with open(filename, 'a') as file:
                    file.write(f"Book {bookID} Reserved by Patron {patronID}\n")
            else:
                with open(filename, 'a') as file:
                    file.write(f"Reservation list for Book {bookID} is full.\n")
 # Method to delete a book from the library
    def DeleteBook(self, bookID, filename):
        if bookID not in self.book_dict:
            with open(filename, 'a') as file:
                file.write(f"Book {bookID} not found in the Library.\n")
            return

        book = self.book_dict[bookID]

        # Check if there are reservations for the book
        if book.reservationHeap.heap:
            reservation_ids = ['Patron ' + str(reservation[0]) for reservation in book.reservationHeap.heap]
            reservation_notification = ', '.join(reservation_ids)
            if len(reservation_ids) > 1:
                with open(filename, 'a') as file:
                    file.write(f"Book {bookID} is no longer available. Reservations made by {reservation_notification} have been cancelled!\n")
            else:
                with open(filename, 'a') as file:
                    file.write(f"Book {bookID} is no longer available. Reservation made by {reservation_notification} has been cancelled!\n")
        else:
            with open(filename, 'a') as file:
                file.write(f"Book {bookID} is no longer available.\n")

        # Remove the book from the library
        del self.book_dict[bookID]
        self.red_black_tree.delete(bookID)

    
    # Method to print details of a book
    def PrintBook(self, bookID, filename):
        if bookID in self.book_dict:
            book = self.book_dict[bookID]
            availability = "Yes" if book.availabilityStatus else "No"
            borrowedBy = book.borrowedBy if book.borrowedBy is not None else "None"
            reservations = [reservation[0] for reservation in book.reservationHeap.heap]

            with open(filename, 'a') as file:
                file.write(f"BookID = {book.bookID}\n")
                file.write(f"Title = {book.bookName}\n")
                file.write(f"Author = {book.authorName}\n")
                file.write(f"Availability = {availability}\n")
                file.write(f"BorrowedBy = {borrowedBy}\n")
                file.write(f"Reservations = {reservations}\n")
        else:
            with open(filename, 'a') as file:
                file.write(f"Book {bookID} not found in the Library.\n")
         # Method to print details of books within a specified range
    def print_books_in_range(self, node, bookID1, bookID2, filename):
        if node is not None and node != self.red_black_tree.nil_node:
            # Traverse the left subtree if the current node's key is greater than bookID1
            if node.key > bookID1:
                self.print_books_in_range(node.left_child, bookID1, bookID2, filename)

            # Check if the current node's key is within the range and print details if it is
            if bookID1 <= node.key <= bookID2:
                self.PrintBook(node.key, filename)

            # Traverse the right subtree if the current node's key is less than bookID2
            if node.key < bookID2:
                self.print_books_in_range(node.right_child, bookID1, bookID2, filename)
 # Method to print details of books within a specified range
    def PrintBooks(self, bookID1, bookID2, filename):
        self.print_books_in_range(self.red_black_tree.root, bookID1, bookID2, filename)
    
     # Method to return a borrowed book to the library
    def ReturnBook(self, patronID, bookID, filename):
        if bookID not in self.book_dict:
            with open(filename, 'a') as file:
                file.write(f"Book {bookID} not found in the Library.\n")
            return

        book = self.book_dict[bookID]

        if book.borrowedBy != patronID:
            with open(filename, 'a') as file:
                file.write(f"Book {bookID} is not borrowed by Patron {patronID}.\n")
            return

        # Book is returned by the patron
        book.availabilityStatus = True
        book.borrowedBy = None
        with open(filename, 'a') as file:
            file.write(f"Book {bookID} Returned by Patron {patronID}\n")

        # Check if there are any reservations
        if book.reservationHeap.heap:
            next_patron = book.reservationHeap.remove_reservation()
            book.borrowedBy = next_patron[0]  # Assigning the book to the next patron in the reservation heap
            book.availabilityStatus = False
            with open(filename, 'a') as file:
                file.write(f"Book {bookID} Allotted to Patron {next_patron[0]}\n")
             
    def FindClosestBook(self, targetID, filename):
    # Initialize variables to store the closest books
        closest_lower = None
        closest_higher = None
        closest_lower_diff = float('inf')
        closest_higher_diff = float('inf')

    # Start from the root of the Red-Black tree
        current_node = self.red_black_tree.root

        while current_node is not None and current_node != self.red_black_tree.nil_node:
            current_key_diff = abs(current_node.key - targetID)

            if current_node.key < targetID:
                if current_key_diff <= closest_lower_diff:
                    closest_lower_diff = current_key_diff
                    closest_lower = current_node
                current_node = current_node.right_child
            else:
                if current_key_diff <= closest_higher_diff:
                    closest_higher_diff = current_key_diff
                    closest_higher = current_node
                current_node = current_node.left_child

        # Determine which book(s) to print based on closeness
        def print_book_details(book):
            if book:
                availability = "Yes" if book.value.availabilityStatus else "No"
                borrowed_by = book.value.borrowedBy if book.value.borrowedBy is not None else "None"
                reservations = [reservation[0] for reservation in book.value.reservationHeap.heap]
                with open(filename, 'a') as file:
                    file.write(f"BookID = {book.key}\n")
                    file.write(f"Title = {book.value.bookName}\n")
                    file.write(f"Author = {book.value.authorName}\n")
                    file.write(f"Availability = {availability}\n")
                    file.write(f"BorrowedBy = {borrowed_by}\n")
                    file.write(f"Reservations = {reservations}\n")
            else:
                with open(filename, 'a') as file:
                    file.write(f"No book found.\n")

        if closest_lower_diff == closest_higher_diff:
        # Print both books in case of a tie
            if closest_lower:
                print_book_details(closest_lower)
            if closest_higher:
                print_book_details(closest_higher)
        elif closest_lower_diff < closest_higher_diff:
            # Print closest lower book
            print_book_details(closest_lower)
        else:
        # Print closest higher book
            print_book_details(closest_higher)

    
    def ColorFlipCount(self):
        # Access the color_flip_count from the Red-Black tree
        return self.red_black_tree.color_flip_count

    
# Assuming the GatorLibrary class and its methods are already defined as per your specifications

# Create an instance of GatorLibrary

# def process_string(s):
#     return [chunk for chunk in s.replace('(', ' ').replace(',', ' ').replace(')', ' ').split() if chunk]

def process_string(s):
    vec = [""]
    for c in s:
        if c == '(' or c == ',' or c == ')':
            vec.append("")
        else:
            vec[-1] += c
    vec.pop()
    return vec

if len(sys.argv) != 2:
    print("Usage: python main.py filename")
    sys.exit(1)

filename = sys.argv[1]

library = GatorLibrary()

with open(filename, 'r') as file:
    output = f'{filename}_output_file.txt'
    for line in file:
        x = line.strip()
        X = process_string(x)
        print(X)
        if X[0] == 'InsertBook':
            library.InsertBook(int(X[1]), X[2], X[3],output, X[4].strip()[1: 4] == "Yes")
        elif X[0] == 'PrintBook':
            library.PrintBook(int(X[1]), output)
        elif X[0] == 'BorrowBook':
            library.BorrowBook(int(X[1]), int(X[2]), int(X[3]), output)
        elif X[0] == 'PrintBooks':
            library.PrintBooks(int(X[1]), int(X[2]), output)
        elif X[0] == 'FindClosestBook':
            library.FindClosestBook(int(X[1]), output)
        elif X[0] == 'ColorFlipCount':
            with open(output, 'a') as file:
                file.write(f'Color Flip Count: {library.ColorFlipCount()}\n')
        elif X[0] == 'DeleteBook':
            library.DeleteBook(int(X[1]), output)
        elif X[0] == 'Quit':
            with open(output, 'a') as file:
                file.write(f'Program Terminated!!\n')
        elif X[0] == 'ReturnBook':
            library.ReturnBook(int(X[1]), int(X[2]), output)
