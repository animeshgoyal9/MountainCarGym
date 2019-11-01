import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='MountainCar-v1',
    entry_point='MountainCar.envs:MountainCarenv',
)
