"""
sudo apt-get install graphviz graphviz-dev
pip install graphviz pygraphviz
"""

from transitions.extensions import GraphMachine

from src.state_manager import StateManager

sm = StateManager(machine_cls=GraphMachine)
sm.get_graph().draw("my_state_diagram.png", prog="dot")
