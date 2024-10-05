from enum import Enum


class Region(Enum):
    """
    Region is an Enum for the regions of Ohio that can be queried from the OHGO API.

    Attributes:
    AKRON: Akron region
    CINCINNATI: Cincinnati region
    CLEVELAND: Cleveland region
    COLUMBUS: Columbus region
    DAYTON: Dayton region
    TOLEDO: Toledo region
    CENTRAL_OHIO: Central Ohio region
    NE_OHIO: Northeast Ohio region
    NW_OHIO: Northwest Ohio region
    SE_OHIO: Southeast Ohio region
    SW_OHIO: Southwest Ohio region

    """
    AKRON = "akron"
    CINCINNATI = "cincinnati"
    CLEVELAND = "cleveland"
    COLUMBUS = "columbus"
    DAYTON = "dayton"
    TOLEDO = "toledo"
    CENTRAL_OHIO = "central-ohio"
    NE_OHIO = "ne-ohio"
    NW_OHIO = "nw-ohio"
    SE_OHIO = "se-ohio"
    SW_OHIO = "sw-ohio"


class SignType(Enum):
    """
    SignType is an Enum for the types of digital signs that can be queried from the OHGO API.

    Attributes:
    DMS: Dynamic Message Sign
    MESSAGE_BOARD: Message Board
    DDMS: Dynamic Digital Message Sign
    TRAVEL_TIME: Travel Time
    SIGN_QUEUE: Sign Queue
    SLOW_TRAFFIC: Slow Traffic
    VSL: Variable Speed Limit

    """
    DMS = "dms"
    MESSAGE_BOARD = "message-board"
    DDMS = "ddms"
    TRAVEL_TIME = "travel-time"
    SIGN_QUEUE = "sign-queue"
    SLOW_TRAFFIC = "slow-traffic"
    VSL = "vsl"
