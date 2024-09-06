from .encode import encode
from .decode import decode
from .util import to_binary_string
from .util import get_pgn_games

###
### As the different methods are stored in separate files,
### this file is a wrapper for both.
### Using this, you have to call chessencryption.encode()
### instead of chessencryption.encode.encode()
###