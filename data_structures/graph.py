# Graph Data Structure for Campus Map with Dijkstra's Algorithm

import heapq
from typing import Dict, List, Tuple, Optional


class CampusGraph:
    """Weighted undirected graph for GIKI campus locations
    
    Used for:
    - Finding shortest path between locations
    - Finding nearest guard to alert location
    - Visualizing campus connectivity
    """
    
    def __init__(self):
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {}
        self.locations: Dict[str, Tuple[float, float]] = {}  # GPS coordinates
    
    def add_location(self, name: str, lat: float = 0, lon: float = 0) -> None:
        """Add a location node to the graph"""
        if name not in self.adjacency:
            self.adjacency[name] = []
            self.locations[name] = (lat, lon)
    
    def add_path(self, loc1: str, loc2: str, distance: float) -> None:
        """Add undirected edge (path) between two locations"""
        if loc1 not in self.adjacency:
            self.add_location(loc1)
        if loc2 not in self.adjacency:
            self.add_location(loc2)
        
        self.adjacency[loc1].append((loc2, distance))
        self.adjacency[loc2].append((loc1, distance))
    
    def get_neighbors(self, location: str) -> List[Tuple[str, float]]:
        """Get all connected locations with distances"""
        return self.adjacency.get(location, [])
    
    def dijkstra(self, start: str, end: str) -> Tuple[float, List[str]]:
        """Find shortest path using Dijkstra's algorithm - O((V+E) log V)
        
        Returns:
            Tuple of (distance, path_list)
        """
        if start not in self.adjacency or end not in self.adjacency:
            return float('inf'), []
        
        # Distance from start to each node
        distances = {loc: float('inf') for loc in self.adjacency}
        distances[start] = 0
        
        # Track previous node for path reconstruction
        previous = {loc: None for loc in self.adjacency}
        
        # Priority queue: (distance, node)
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            visited.add(current_node)
            
            if current_node == end:
                break
            
            for neighbor, weight in self.adjacency[current_node]:
                if neighbor in visited:
                    continue
                
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_dist, neighbor))
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        if path[0] != start:
            return float('inf'), []
        
        return distances[end], path
    
    def find_nearest_location(self, start: str, targets: List[str]) -> Tuple[str, float, List[str]]:
        """Find nearest location from a list of targets
        
        Useful for finding nearest guard to an alert location
        """
        nearest = None
        min_distance = float('inf')
        best_path = []
        
        for target in targets:
            distance, path = self.dijkstra(start, target)
            if distance < min_distance:
                min_distance = distance
                nearest = target
                best_path = path
        
        return nearest, min_distance, best_path
    
    def bfs_traversal(self, start: str) -> List[str]:
        """Breadth-First Search traversal - O(V + E)"""
        if start not in self.adjacency:
            return []
        
        visited = set()
        queue = [start]
        result = []
        
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                result.append(node)
                for neighbor, _ in self.adjacency[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    def dfs_traversal(self, start: str, visited: set = None) -> List[str]:
        """Depth-First Search traversal - O(V + E)"""
        if visited is None:
            visited = set()
        
        if start not in self.adjacency or start in visited:
            return []
        
        visited.add(start)
        result = [start]
        
        for neighbor, _ in self.adjacency[start]:
            result.extend(self.dfs_traversal(neighbor, visited))
        
        return result
    
    def get_all_locations(self) -> List[str]:
        """Get list of all locations"""
        return list(self.adjacency.keys())
    
    def get_edge_count(self) -> int:
        """Get total number of paths (edges)"""
        return sum(len(neighbors) for neighbors in self.adjacency.values()) // 2


def create_giki_campus_graph() -> CampusGraph:
    """Create pre-configured GIKI campus graph with actual locations"""
    campus = CampusGraph()
    
    # Add locations with approximate coordinates
    locations = [
        ("Main Gate", 34.0691, 72.6441),
        ("Ayaan Gate", 34.0685, 72.6450),
        ("FCSE", 34.0695, 72.6445),
        ("FME", 34.0700, 72.6440),
        ("FBS", 34.0698, 72.6448),
        ("Library", 34.0693, 72.6438),
        ("TUC", 34.0688, 72.6442),
        ("Sports Complex", 34.0682, 72.6435),
        ("Admin Block", 34.0690, 72.6455),
        ("H1", 34.0678, 72.6448),
        ("H2", 34.0676, 72.6445),
        ("H3", 34.0674, 72.6442),
        ("H4", 34.0672, 72.6440),
        ("H5", 34.0670, 72.6438),
        ("H6", 34.0668, 72.6435),
        ("H7", 34.0666, 72.6432),
        ("GH", 34.0680, 72.6455),
        ("NGH", 34.0682, 72.6458),
        ("Faculty Residence D", 34.0685, 72.6460),
        ("Faculty Residence E", 34.0687, 72.6462),
        ("Faculty Residence F", 34.0689, 72.6464),
    ]
    
    for name, lat, lon in locations:
        campus.add_location(name, lat, lon)
    
    # Add paths with distances (in meters, approximate)
    paths = [
        ("Main Gate", "TUC", 150),
        ("Main Gate", "Admin Block", 200),
        ("Ayaan Gate", "GH", 100),
        ("Ayaan Gate", "NGH", 120),
        ("TUC", "FCSE", 100),
        ("TUC", "Library", 80),
        ("TUC", "FBS", 120),
        ("FCSE", "FME", 150),
        ("FCSE", "Library", 100),
        ("FME", "FBS", 100),
        ("Library", "Sports Complex", 200),
        ("TUC", "H1", 250),
        ("H1", "H2", 50),
        ("H2", "H3", 50),
        ("H3", "H4", 50),
        ("H4", "H5", 50),
        ("H5", "H6", 50),
        ("H6", "H7", 50),
        ("GH", "NGH", 100),
        ("NGH", "Faculty Residence D", 150),
        ("Faculty Residence D", "Faculty Residence E", 50),
        ("Faculty Residence E", "Faculty Residence F", 50),
        ("Admin Block", "Faculty Residence D", 200),
    ]
    
    for loc1, loc2, distance in paths:
        campus.add_path(loc1, loc2, distance)
    
    return campus
