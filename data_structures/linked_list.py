# Linked List Data Structures for IntruWatch

class LoginNode:
    """Linked list node for admin login credentials"""
    def __init__(self, username: str, password_hash: str):
        self.username = username
        self.password_hash = password_hash
        self.next = None


class LoginLinkedList:
    """Linked list to manage admin logins"""
    def __init__(self):
        self.head = None
    
    def insert(self, username: str, password_hash: str) -> None:
        new_node = LoginNode(username, password_hash)
        new_node.next = self.head
        self.head = new_node
    
    def find(self, username: str, password_hash: str) -> bool:
        current = self.head
        while current:
            if current.username == username and current.password_hash == password_hash:
                return True
            current = current.next
        return False
    
    def username_exists(self, username: str) -> bool:
        current = self.head
        while current:
            if current.username == username:
                return True
            current = current.next
        return False


class CheckInNode:
    """Linked list node for resident check-ins"""
    def __init__(self, username: str, reg_no: str, designation: str, 
                 gender: str, room_no: str = None, employee_no: str = None):
        self.username = username
        self.reg_no = reg_no
        self.designation = designation
        self.gender = gender
        self.room_no = room_no
        self.employee_no = employee_no
        self.next = None


class CheckInLinkedList:
    """Linked list to manage resident check-ins"""
    def __init__(self):
        self.head = None
        self.student_count = 0
        self.faculty_count = 0
        self.other_count = 0
    
    def insert(self, username: str, reg_no: str, designation: str,
               gender: str, room_no: str = None, employee_no: str = None) -> None:
        new_node = CheckInNode(username, reg_no, designation, gender, room_no, employee_no)
        new_node.next = self.head
        self.head = new_node
        
        # Update counters
        if designation == "Student":
            self.student_count += 1
        elif designation == "Faculty":
            self.faculty_count += 1
        else:
            self.other_count += 1
    
    def remove(self, username: str, identifier: str, designation: str, location: str) -> bool:
        current = self.head
        previous = None
        
        while current:
            identifier_match = (current.reg_no == identifier) or (current.employee_no == identifier)
            location_match = (current.room_no == location) or (current.employee_no == location)
            
            if (current.username == username and 
                current.designation == designation and 
                identifier_match and location_match):
                
                # Update counters
                if designation == "Student":
                    self.student_count -= 1
                elif designation == "Faculty":
                    self.faculty_count -= 1
                else:
                    self.other_count -= 1
                
                # Remove node
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            
            previous = current
            current = current.next
        return False
    
    def to_list(self) -> list:
        data_list = []
        current = self.head
        while current:
            data_list.append({
                "Username": current.username,
                "Designation": current.designation,
                "Gender": current.gender,
                "Reg/Emp No": current.reg_no if current.designation == "Student" else current.employee_no,
                "Hostel No": current.room_no
            })
            current = current.next
        return data_list
    
    def get_student_reg_numbers(self) -> list:
        regs = []
        current = self.head
        while current:
            if current.designation == "Student":
                regs.append(current.reg_no)
            current = current.next
        return regs
    
    def get_counts(self) -> tuple:
        return self.student_count, self.faculty_count, self.other_count


class EventNode:
    """Linked list node for event logging"""
    def __init__(self, data: str):
        self.data = data
        self.next = None


class EventLinkedList:
    """Fixed-size linked list for recent events (FIFO behavior)"""
    def __init__(self, max_size: int = 10):
        self.head = None
        self.size = 0
        self.max_size = max_size
    
    def add_event(self, event_data: str) -> None:
        new_node = EventNode(event_data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        
        # Trim if exceeds max size
        if self.size > self.max_size:
            current = self.head
            for _ in range(self.max_size - 1):
                current = current.next
            current.next = None
            self.size = self.max_size
    
    def get_all_events(self) -> list:
        events = []
        current = self.head
        while current:
            events.append(current.data)
            current = current.next
        return events
