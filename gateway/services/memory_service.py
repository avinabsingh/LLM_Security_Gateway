from typing import List, Dict

class SessionMemory:
    def __init__(self):
        self.sessions: Dict[str, List[float]] = {}
        self.window_size = 3 

    def add_turn(self, session_id: str, risk_score: float) -> List[float]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        self.sessions[session_id].append(risk_score)
        
        # Keep only the most recent N turns
        if len(self.sessions[session_id]) > self.window_size:
            self.sessions[session_id].pop(0)
            
        return self.sessions[session_id]