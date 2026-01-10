# Binary Search Tree for Guard Management

from typing import Optional, List, Tuple


class GuardNode:
    """BST node for guard management"""
    def __init__(self, name: str = None, guard_id: int = None, duty: str = None):
        self.name = name
        self.guard_id = guard_id
        self.duty = duty
        self.left: Optional[GuardNode] = None
        self.right: Optional[GuardNode] = None
    
    def insert(self, name: str, guard_id: int, duty: str) -> None:
        """Insert a new guard into the BST"""
        if self.guard_id is None:
            self.name = name
            self.guard_id = guard_id
            self.duty = duty
            return
        
        if guard_id < self.guard_id:
            if self.left is None:
                self.left = GuardNode(name, guard_id, duty)
            else:
                self.left.insert(name, guard_id, duty)
        elif guard_id > self.guard_id:
            if self.right is None:
                self.right = GuardNode(name, guard_id, duty)
            else:
                self.right.insert(name, guard_id, duty)
    
    def inorder(self) -> List[Tuple[str, int, str]]:
        """Inorder traversal - returns sorted list of guards"""
        result = []
        if self.left:
            result.extend(self.left.inorder())
        if self.name is not None:
            result.append((self.name, self.guard_id, self.duty))
        if self.right:
            result.extend(self.right.inorder())
        return result
    
    def preorder(self) -> List[Tuple[str, int, str]]:
        """Preorder traversal"""
        result = []
        if self.name is not None:
            result.append((self.name, self.guard_id, self.duty))
        if self.left:
            result.extend(self.left.preorder())
        if self.right:
            result.extend(self.right.preorder())
        return result
    
    def postorder(self) -> List[Tuple[str, int, str]]:
        """Postorder traversal"""
        result = []
        if self.left:
            result.extend(self.left.postorder())
        if self.right:
            result.extend(self.right.postorder())
        if self.name is not None:
            result.append((self.name, self.guard_id, self.duty))
        return result
    
    def find(self, target_id: int) -> Optional['GuardNode']:
        """Binary search for a guard by ID - O(log n)"""
        if self.guard_id is None:
            return None
        if target_id == self.guard_id:
            return self
        if target_id < self.guard_id and self.left:
            return self.left.find(target_id)
        if target_id > self.guard_id and self.right:
            return self.right.find(target_id)
        return None
    
    def get_min(self) -> Optional['GuardNode']:
        """Get guard with minimum ID"""
        if self.left is None:
            return self
        return self.left.get_min()
    
    def get_max(self) -> Optional['GuardNode']:
        """Get guard with maximum ID"""
        if self.right is None:
            return self
        return self.right.get_max()
    
    def count_nodes(self) -> int:
        """Count total guards in BST"""
        count = 1 if self.name is not None else 0
        if self.left:
            count += self.left.count_nodes()
        if self.right:
            count += self.right.count_nodes()
        return count


def flatten_bst_bfs(root: Optional[GuardNode]) -> List[GuardNode]:
    """BFS traversal - flatten BST to list (level order)"""
    if not root or root.guard_id is None:
        return []
    
    queue = [root]
    result = []
    
    while queue:
        node = queue.pop(0)  # Dequeue
        if node and node.name is not None:
            result.append(node)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result


def assign_guards_to_locations(root: GuardNode, locations: dict) -> dict:
    """Assign guards from BST to campus locations"""
    assigned = {}
    all_guards = flatten_bst_bfs(root)
    index = 0
    
    for location, count in locations.items():
        assigned[location] = []
        for _ in range(count):
            if index < len(all_guards):
                assigned[location].append(all_guards[index].name)
                index += 1
    
    return assigned
