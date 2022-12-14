from . import ExplorationTechnique
import random

class DFS(ExplorationTechnique):
    """
    Depth-first search.

    Will only keep one path active at a time, any others will be stashed in the 'deferred' stash.
    When we run out of active paths to step, we take the longest one from deferred and continue.
    """

    def __init__(self, deferred_stash='deferred'):
        super(DFS, self).__init__()
        self._random = random.Random()
        self._random.seed(10)
        self.deferred_stash = deferred_stash
        self.active_path_length = 0
        self.deferred_path_length = []

    def setup(self, simgr):
        if self.deferred_stash not in simgr.stashes:
            simgr.stashes[self.deferred_stash] = []

    def step(self, simgr, stash='active', **kwargs):
        simgr = simgr.step(stash=stash, **kwargs)
        layer_difference = 0
        self.active_path_length += 1
        if len(simgr.stashes[stash]) > 1:
            self._random.shuffle(simgr.stashes[stash])
            simgr.split(from_stash=stash, to_stash=self.deferred_stash, limit=1)
            self.deferred_path_length.append(self.active_path_length)

        if len(simgr.stashes[stash]) == 0:
            if len(simgr.stashes[self.deferred_stash]) == 0:
                return simgr
            simgr.stashes[stash].append(simgr.stashes[self.deferred_stash].pop())
            layer_difference = self.active_path_length - self.deferred_path_length[-1]
            self.deferred_path_length.pop()

        return simgr, layer_difference
